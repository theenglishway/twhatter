import logging.config


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(levelname)s:%(name)s: %(message)s ',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

def log_setup(verbosity):
    logging.getLogger('urllib3').setLevel(logging.WARNING)

    if verbosity == 'verbose':
        logging.getLogger('twhatter.client').setLevel(logging.DEBUG)
        logging.getLogger('twhatter.parser').setLevel(logging.DEBUG)
    elif verbosity == 'debug':
        logging.getLogger('twhatter.client').setLevel(logging.DEBUG)
        logging.getLogger('twhatter.parser').setLevel(logging.INFO)
    elif verbosity == 'info':
        logging.getLogger('twhatter.client').setLevel(logging.INFO)
        logging.getLogger('twhatter.parser').setLevel(logging.INFO)
    elif verbosity == 'none':
        logging.getLogger('twhatter.client').setLevel(logging.WARNING)
        logging.getLogger('twhatter.parser').setLevel(logging.WARNING)

    logging.config.dictConfig(LOGGING)
