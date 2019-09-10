CONFIG = {
    'test': {
        'default': False,
        'action': 'store_true',
        'help': 'Help, I need sombody!'
        },
    'stuff_dir': {
        'default': '/tmp/tests.conf1/stuff',
        'help': 'A directory dedicated to stuff',
        },
    }


GLOBAL = {
    'cache_dir': {
        'default': '/var/cache',
        'help': 'A cachedir',
        },
    }


CLI_CONFIG = {
    'someone': {
        'default': 'Not just anybody!',
        'help': 'Oh yes I need someone',
        },
    }
