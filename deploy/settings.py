"""
Deployment Settings

Used by fabfile
"""

# User name and password
TOGILE_USER = ('togile', 'tgpass')

DB_SUPERUSER = ('togile', 'tgpostgress3kret')

DEB_PKGS = (
    ('nginx', ''),
    ('postgresql-9.1', ''),
    ('python-dev', ''),
    ('memcached', ''),
)

# Tuples of Usernames and Passwords
# e.g USERS = (('user', 'userPass'),)
USERS = (TOGILE_USER,)

TOGILE_PATH = '/home/%s/togile' % TOGILE_USER[0]

TOGILE_REPO = 'https://github.com/mohabusama/togile'
