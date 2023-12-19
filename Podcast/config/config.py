from pydantic_settings import BaseSettings, SettingsConfigDict
import logging.config

class Settings(BaseSettings):
    MONGODB_HOST : str
    MONGODB_PORT : str
    MONGODB_DATABASE : str

    AUTH_POD_KEY1 : str

    NTF_POD_KEY1 : str

    ACC_POD_KEY1 : str

    POD_AUTH_SHARED_KEY : str
    POD_ACC_SHARED_KEY : str
    NTF_POD_SHARED_KEY : str

    AUTHENTICATION_SERVICE_URL : str
    ACCOUNT_SERVICE_URL : str
    NOTIFICATION_SERVICE_URL : str
    DJANGO_PODCAST_SERVICE_URL : str
    
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


LOGGING_CONFIG = {
    "version": 1,
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "http",
            "stream": "ext://sys.stderr"
        }
    },
    "formatters": {
        "http": {
            "format": "%(levelname)s [%(asctime)s] %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    'loggers': {
        'httpx': {
            'handlers': ['default'],
            'level': 'DEBUG',
        },
        'httpcore': {
            'handlers': ['default'],
            'level': 'DEBUG',
        },
    }
}

logging.config.dictConfig(LOGGING_CONFIG)