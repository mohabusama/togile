"""
Deployment Settings

Used by fabfile
"""

# Username, Password and SSH Key file path
TOGILE_USER = ('togile', 'tgpass')

DEB_PKGS = (
    ('nginx', ''),
    ('postgresql-9.1', ''),
    ('python-dev', ''),
    ('memcached', ''),
    ('g++', ''),
    ('make', ''),
    ('libpq-dev', ''),
)

USERS = ()

TOGILE_REPO = 'https://github.com/mohabusama/togile'

NGINX = {
    'server_name': 'togile.local'
}

# Override by local deploy settings
try:
    from deploy_settings import *  # NOQA
    print 'Local Deployment Settings found...'
except ImportError:
    pass

TOGILE_PATH = '/home/%s/togile' % TOGILE_USER[0]

# Tuples of Usernames and Passwords
# e.g USERS = (('user', 'userPass'),)
USERS += (TOGILE_USER,)
