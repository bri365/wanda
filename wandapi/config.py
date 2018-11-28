
import os


# Server Specific Configurations
server = {
    'port': '8000',
    'host': '127.0.0.1'
}

wanda = {
    'base_dir': '/home/wandapi'
}

logging = {
    'version': 1,
    'loggers': {
        'wandapi': {'level': 'INFO', 'handlers': ['file']},
        'wanda_setup': {'level': 'INFO', 'handlers': ['file']},
        'py.warnings': {'handlers': ['file']}
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'filename': '/var/log/wandapi/wandapi.log',
            'mode': 'a',
            'maxBytes': 10485760,
            'backupCount': 5,
        }
    },
    'formatters': {
        'detailed': {
            'format': '%(asctime)s [%(name)s|%(process)d|%(thread)d|%(threadName)s] | %(filename)s:%(funcName)s:%(lineno)d (%(levelname)s) - %(message)s'  # noqa: E501
        }
    }
}

env_loggers = {
    'API_DEBUG_LOG_LEVEL': 'wandapi'
}

logging_levels = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']

for env_var, logger_name in env_loggers.items():
    debug_log_level = os.getenv(env_var, None)
    if debug_log_level:
        debug_log_level = debug_log_level.upper()
        if debug_log_level in logging_levels:
            logging['loggers'][logger_name]['level'] = debug_log_level
            if 'file' not in logging['loggers'][logger_name]['handlers']:
                logging['loggers'][logger_name]['handlers'].append('file')

            # set the file handler's level if it is relevant
            if (logging_levels.index(debug_log_level) >
                    logging_levels.index(logging['handlers']['file']['level'])):
                logging['handlers']['file']['level'] = debug_log_level
