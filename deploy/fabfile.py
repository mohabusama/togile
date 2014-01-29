import os
from time import sleep

from fabric.api import task, cd, run, sudo
from fabric.context_managers import prefix
from fabric.context_managers import settings

from fabtools import require, files
from fabtools.python import virtualenv

import settings as tg
from prod_settings import DATABASES

LOCAL_BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Repo Path on remote server!
REPO_PATH = os.path.join(tg.TOGILE_PATH, 'togile')


@task
def deploy():
    _add_users()
    _install_pkgs()

    venv = os.path.join(tg.TOGILE_PATH, 'venv')

    tg_user, tg_pass = tg.TOGILE_USER

    with settings(user=tg_user, password=tg_pass):
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
        require.user(username, password=password)
        require.sudoer(username)


def _add_env(venv):
    # Add TOGILE path
    require.directory(tg.TOGILE_PATH)

    # Add venv
    require.python.virtualenv(venv)

    # Pull/Update GIT Repo
    with cd(tg.TOGILE_PATH):
        require.git.working_copy(tg.TOGILE_REPO)


def _install_requirements():
    req_file = os.path.join(REPO_PATH, 'requirements.txt')
    require.python.requirements(req_file)


def _adjust_app_settings(venv):
    local_settings_path = os.path.join(LOCAL_BASE_DIR, 'deploy',
                                       'prod_settings.py')
    if not os.path.exists(local_settings_path):
        raise Exception('Cannot Find Production Settings File: %s' %
                        local_settings_path)

    remote_settings_path = os.path.join(REPO_PATH, 'togile', 'settings',
                                        'prod_settings.py')

    require.files.file(remote_settings_path, source=local_settings_path)
    static_dir = os.path.join(venv, 'www')
    context = {
        'static': static_dir
    }
    files.upload_template(local_settings_path, remote_settings_path,
                          context=context)


def _prepare_db():
    # Create DB and DB Users, from Production settings
    require.postgres.server()

    db_user, db_pass = tg.DB_SUPERUSER
    require.postgres.user(db_user, password=db_pass, superuser=True)

    for db in DATABASES.itervalues():
        require.postgres.user(db['USER'], password=db['PASSWORD'],
                              createrole=True)
        require.postgres.database(db['NAME'], owner=db['USER'])

    # Assuming Virtual Env activated!
    with cd(REPO_PATH):
        run('python manage.py syncdb --noinput')
        run('python manage.py migrate')
        # Load fixtures
        fixtures_path = os.path.join(REPO_PATH, 'deploy', 'fixtures')
        fixtures = run('ls %s' % fixtures_path).split()
        for fixture in fixtures:
            if fixture.endswith('json'):
                run('python manage.py loaddata deploy/fixtures/%s' % fixture)


def _prepare_static(venv):
    static_dir = os.path.join(venv, 'www')
    require.directory(static_dir)

    with cd(REPO_PATH):
        run('python manage.py collectstatic --noinput')

        # Virual-Node and Angular App
        require.python.package('virtual-node==0.0.4')
        require.nodejs.package('bower')

    app_path = os.path.join(REPO_PATH, 'frontend')
    with cd(app_path):
        run('bower install')


def _prepare_service(venv):
    # logs
    log_dir = os.path.join(venv, 'log')
    require.directory(log_dir)

    # Nginx
    require.nginx.disabled('default')

    conf = 'nginx/togile.conf'
    nginx_log = os.path.join(log_dir, 'nginx.log')
    app = os.path.join(REPO_PATH, 'frontend', 'app')
    static = os.path.join(venv, 'www')
    require.nginx.site(tg.NGINX['server_name'], template_source=conf,
                       nginx_log=nginx_log, static=static, togile_app=app)

    # CIRCUS

    # Upstart Conf
    circus_dir = os.path.join(venv, 'circus')
    require.directory(circus_dir)
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
    files.upload_template('circus/circus.ini', web_ini, context=context)

    # Start Circus
    with settings(warn_only=True):
        # Stop circus if running ... ignore error anyway
        sudo('service circus stop')
        sleep(2)

    sudo('service circus start')
