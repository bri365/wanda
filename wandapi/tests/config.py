
import os

# Server Specific Configurations
server = {
    'port': '8084',
    'host': '0.0.0.0'
}

wanda = {
    'base_dir': '/home/wandapi'
}

logging = {
    'version': 1,
    'loggers': {
        'wandapi': {'level': 'DEBUG', 'handlers': []},
        'py.warnings': {'handlers': ['console']}
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)-5.5s [%(name)s] [%(threadName)s] %(message)s'
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
            logging['loggers'][logger_name]['handlers'].append('console')
