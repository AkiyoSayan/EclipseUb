import os
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

def get_config_value(config, key, section, fallback=None, cast_func=str):
    value = os.getenv(key)
    if value is not None:
        return cast_func(value)

    if config.has_option(section, key):
        return cast_func(config.get(section, key))

    return fallback

API_ID = get_config_value(config, "API_ID", "eclipse_Main", fallback=123456, cast_func=int)
API_HASH = get_config_value(config, "API_HASH", "eclipse_Main", fallback="")
SESSION = get_config_value(config, "SESSION", "eclipse_Main", fallback="")

REDIS_URI = get_config_value(config, "REDIS_URI", "eclipse_Main", fallback="")
LOG_GROUP = get_config_value(config, "LOG_GROUP", "eclipse_Main", fallback=1, cast_func=int)
LANG = get_config_value(config, "LANG", "eclipse_Other", fallback="en")
PREFIX = get_config_value(config, "PREFIX", "eclipse_Other", fallback=".")
BOT_TOKEN = get_config_value(config, "BOT_TOKEN", "eclipse_Other", fallback="")

REPO_URL = get_config_value(config, "REPO_URL", "eclipse_Other", 
                            fallback="https://github.com/EclipseUserbot/Eclipse.git")
GIT_TOKEN = get_config_value(config, "GIT_TOKEN", "eclipse_Other", fallback="")

SUDO_PREFIX = get_config_value(config, "SUDO_PREFIX", "eclipse_Other", fallback="")
SUDO_USERS = {int(x) for x in get_config_value(
    config, "SUDO_USERS", "eclipse_Other", fallback="").split(',') if x.strip()}
