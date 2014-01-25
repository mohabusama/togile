import os

from fabric.api import task, cd, run
from fabric.context_managers import prefix
from fabric.context_managers import settings as fsettings

from fabtools import require
from fabtools.python import virtualenv

import settings


LOCAL_BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Repo Path on remote server!
REPO_PATH = os.path.join(settings.TOGILE_PATH, 'togile')


@task
def deploy():
    _add_users()
    _install_pkgs()

    venv = os.path.join(settings.TOGILE_PATH, 'venv')

    tg_user, tg_pass = settings.TOGILE_USER

    with fsettings(user=tg_user, password=tg_pass):
        _add_env(venv)

        with virtualenv(venv), prefix('export TOGILE_PRODUCTION=True'):
            _install_requirements()
            _adjust_app_settings()
            _prepare_db()


def _install_pkgs():
    require.deb.uptodate_index(max_age={'day': 1})
    for pkg, version in settings.DEB_PKGS:
        require.deb.package(pkg, version=version)


def _add_users():
    for user in settings.USERS:
        username, password = user
        require.user(username, password=password)
        require.sudoer(username)


def _add_env(venv):
    # Add TOGILE path
    require.directory(settings.TOGILE_PATH)

    # Add venv
    require.python.virtualenv(venv)

    # Pull/Update GIT Repo
    with cd(settings.TOGILE_PATH):
        require.git.working_copy(settings.TOGILE_REPO)


def _install_requirements():
    req_file = os.path.join(REPO_PATH, 'requirements.txt')
    require.python.requirements(req_file)


def _adjust_app_settings():
    local_settings_path = os.path.join(LOCAL_BASE_DIR, 'deploy',
                                       'prod_settings.py')
    if not os.path.exists(local_settings_path):
        raise Exception('Cannot Find Production Settings File: %s' %
                        local_settings_path)

    remote_settings_path = os.path.join(REPO_PATH, 'settings',
                                        'prod_settings.py')

    require.file(remote_settings_path, source=local_settings_path)


def _prepare_db():
    # Create DB and DB Users, from Production settings
    from prod_settings import DATABASES

    require.postgres.server()

    db_user, db_pass = settings.DB_SUPERUSER
    require.postgres.user(db_user, password=db_pass, superuser=True)

    for db in DATABASES.itervalues():
        require.postgres.user(db['USER'], password=db['PASSWORD'],
                              create_role=True)
        require.postgres.database(db['NAME'], owner=db['USER'])

    # Assuming Virtual Env activated!
    with cd(REPO_PATH):
        run('python manage.py syncdb --noinput')
        run('python manage.py migrate')
        # Load fixtures
        fixtures_path = os.path.join(REPO_PATH, 'deploy', 'fixtures')
        for fixture in os.listdir(fixtures_path):
            if fixture.endswith('json'):
                run('python manage.py loaddata deploy/fixtures/%s' % fixture)
    return
