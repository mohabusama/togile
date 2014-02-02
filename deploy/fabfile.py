import os
from time import sleep

from fabric.api import task, cd, sudo
from fabric.context_managers import prefix
from fabric.context_managers import settings

from fabtools import require, files
from fabtools.python import virtualenv

import settings as tg
from prod_settings import DATABASES

LOCAL_BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Repo Path on remote server!
REPO_PATH = os.path.join(tg.TOGILE_PATH, 'togile')

USER, PASSWORD = tg.TOGILE_USER


@task
def deploy():
    _add_users()
    _install_pkgs()

    venv = os.path.join(tg.TOGILE_PATH, 'venv')

    tg_user, tg_pass = tg.TOGILE_USER

    _add_env(venv)

    with virtualenv(venv), prefix('export TOGILE_PRODUCTION=True'):
        _install_requirements()
        _adjust_app_settings(venv)
        _prepare_db()
        _prepare_static(venv)
        _prepare_service(venv)


def _install_pkgs():
    require.deb.uptodate_index(max_age={'day': 7})
    for pkg, version in tg.DEB_PKGS:
        require.deb.package(pkg, version=version)


def _add_users():
    for user in tg.USERS:
        username, password = user
        require.user(username, password=password, shell='/bin/bash')
        require.sudoer(username)


def _add_env(venv):
    # Add TOGILE path
    require.directory(tg.TOGILE_PATH, owner=USER, use_sudo=True)

    # Add venv
    require.python.virtualenv(venv, user=USER, use_sudo=True)

    # Pull/Update GIT Repo
    with cd(tg.TOGILE_PATH):
        require.git.working_copy(tg.TOGILE_REPO, user=USER, use_sudo=True)


def _install_requirements():
    req_file = os.path.join(REPO_PATH, 'requirements.txt')
    require.python.requirements(req_file, user=USER, use_sudo=True)


def _adjust_app_settings(venv):
    local_settings_path = os.path.join(LOCAL_BASE_DIR, 'deploy',
                                       'prod_settings.py')
    if not os.path.exists(local_settings_path):
        raise Exception('Cannot Find Production Settings File: %s' %
                        local_settings_path)

    remote_settings_path = os.path.join(REPO_PATH, 'togile', 'settings',
                                        'prod_settings.py')

    require.files.file(remote_settings_path, source=local_settings_path,
                       owner=USER, use_sudo=True)
    static_dir = os.path.join(venv, 'www')
    context = {
        'static': static_dir
    }
    files.upload_template(local_settings_path, remote_settings_path,
                          context=context, user=USER, use_sudo=True)


def _prepare_db():
    # Create DB and DB Users, from Production settings
    require.postgres.server()

    for db in DATABASES.itervalues():
        require.postgres.user(db['USER'], password=db['PASSWORD'],
                              createrole=True)
        require.postgres.database(db['NAME'], owner=db['USER'])

    # Assuming Virtual Env activated!
    with cd(REPO_PATH):
        sudo('python manage.py syncdb --noinput', user=USER)
        sudo('python manage.py migrate', user=USER)
        # Load fixtures
        fixtures_path = os.path.join(REPO_PATH, 'deploy', 'fixtures')
        fixtures = sudo('ls %s' % fixtures_path).split()
        for fixture in fixtures:
            if fixture.endswith('json'):
                sudo('python manage.py loaddata deploy/fixtures/%s' % fixture,
                     user=USER)


def _prepare_static(venv):
    static_dir = os.path.join(venv, 'www')
    require.directory(static_dir, owner=USER, use_sudo=True)

    with cd(REPO_PATH):
        sudo('python manage.py collectstatic --noinput', user=USER)

        # Virual-Node and Angular App
        require.python.package('virtual-node==0.0.4', user=USER, use_sudo=True)

        # Kinda a hack! npm ignored sudo user and used another $HOME
        # Forcing it to use certain $HOME
        with prefix('export HOME=/home/%s' % USER):
            sudo('echo $HOME', user=USER)
            sudo('npm install bower -g', user=USER)

    app_path = os.path.join(REPO_PATH, 'frontend')
    with cd(app_path), prefix('export HOME=/home/%s' % USER):
        sudo('bower install', user=USER)


def _prepare_service(venv):
    # logs
    log_dir = os.path.join(venv, 'log')
    require.directory(log_dir, owner=USER, use_sudo=True)

    # Nginx
    require.nginx.disabled('default')

    conf = 'nginx/togile.conf'
    nginx_log = os.path.join(log_dir, 'nginx.log')
    app = os.path.join(REPO_PATH, 'frontend', 'app')
    static = os.path.join(venv, 'www')
    require.nginx.site(tg.NGINX['server_name'], template_source=conf,
                       nginx_log=nginx_log, static=static, togile_app=app)

    # Ensure running ...
    require.nginx.server()

    # CIRCUS

    # Upstart Conf
    circus_dir = os.path.join(venv, 'circus')
    require.directory(circus_dir, owner=USER, use_sudo=True)

    context = {
        'venv': venv,
        'circus': circus_dir,
        'togile': REPO_PATH,
        'user': tg.TOGILE_USER[0]
    }
    files.upload_template('circus/circus.conf', '/etc/init/circus.conf',
                          context=context, use_sudo=True)
    # Web INI
    web_ini = os.path.join(context['circus'], 'web.ini')
    files.upload_template('circus/circus.ini', web_ini, context=context,
                          user=USER, use_sudo=True)

    # Start Circus
    with settings(warn_only=True):
        # Stop circus if running ... ignore error anyway
        sudo('service circus stop')
        sleep(2)

    sudo('service circus start')
