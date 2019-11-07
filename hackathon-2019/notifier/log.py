# log.py
import logging.config

LOG_CONFIG = {
    'version': 1,
    'filters': {
        'request_id': {
            '()': 'utils.RequestIdFilter',
        },
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s.%(module)s.%(funcName)s:%(lineno)d - %(levelname)s - %(request_id)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'filters': ['request_id'],
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level':'DEBUG',
        },
        'app': {
            'handlers': ['console'],
            'level':'DEBUG',
        },
    }
}

logging.config.dictConfig(LOG_CONFIG)