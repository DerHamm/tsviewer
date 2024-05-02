from tsviewer.ts_viewer_utils import resolve_with_project_path
from dataclasses import dataclass
from json import load, dump
import ts3.query
from os import environ

ENVIRONMENT_VARIABLE_PREFIX = 'TSVIEWER_CONFIGURATION'


@dataclass
class Configuration(object):
    """
    Represents the configuration file
    """
    server_query_host: str
    server_query_port: int
    server_query_user: str
    server_query_password: str
    server_id: int
    teamspeak_install_path: str
    website_password: str
    admin_password: str
    cookie_secret_key: str
    cookie_signing_salt: str
    """
    Those are dangerous settings, do not use them in production! Everyone accessing the website will obtain a
    Session-Cookie that is authenticated as user or admin. If ever used in production, wipe all cookies on next 
    """
    disable_user_password_protection: bool
    disable_admin_password_protection: bool


def load_configuration(path: str = 'config/config.json') -> Configuration:
    """
    Loads the `Configuration` object from the config-file
    :param path: Path to the configuration file
    :return: A `Configuration` file object
    """
    with resolve_with_project_path(path).open('r') as configuration_file:
        return Configuration(**load(configuration_file))


def save_configuration(configuration: Configuration, path: str = 'config/config.json') -> None:
    """
    Saves a modified `Configuration` to the given path
    :param configuration: `Configuration` object
    :param path: Path to the configuration file
    """
    with resolve_with_project_path(path).open('w') as configuration_file:
        dump(configuration.__dict__, configuration_file)


def authorize(configuration: Configuration, connection: ts3.query.TS3Connection) -> None:
    """
    :param configuration: `Configuration` object
    :param connection: A reference to the `ts3.query.TS3Connection` object
    """
    connection.login(client_login_name=configuration.server_query_user,
                     client_login_password=configuration.server_query_password)
    connection.use(sid=configuration.server_id)


def read_environment_variables(configuration: Configuration) -> None:
    """
    Overwrite all configuration fields when there are configured environment variables for those fields.
    The pattern for those variables is TSVIEWER_CONFIGURATION_FIELD_NAME. E.g.: TSVIEWER_CONFIGURATION_PASSWORD
    :param configuration: configuration object
    """
    for name in configuration.__dict__.keys():
        value = environ.get(f'{ENVIRONMENT_VARIABLE_PREFIX}_{name.upper()}')
        if value:
            configuration.__setattr__(name, value)


def read_config_path_from_environment_variables(default_path: str = 'config/config.json') -> str:
    """
    Read the file path from the environment variable TSVIEWER_CONFIGURATION_FILE if configured
    :param default_path:
    :return:
    """
    return environ.get(f'{ENVIRONMENT_VARIABLE_PREFIX}_FILE', default_path)
