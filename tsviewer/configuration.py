from tsviewer.ts_viewer_utils import resolve_with_project_path
from dataclasses import dataclass
from json import load, dump
import ts3.query
from os import environ

_CONFIGURATION = None
ENVIRONMENT_VARIABLE_PREFIX = 'TSVIEWER_CONFIGURATION'


@dataclass(repr=True)
class Configuration(object):
    """
    Represents the configuration file
    Attributes
        server_query_host: The host used for the Teamspeak Server Query.\n
        server_query_port: The port used for the Teamspeak Server Query.\n
        server_query_user: The username of the Teamspeak Server Query user.\n
        server_query_password: The password the Teamspeak Server Query user.\n
        server_id: Teamspeak virtual server id. Usually only one virtual server with id=1 exists.\n
        teamspeak_install_path: The path to the Teamspeak Server installation. Needed for avatars.\n
        website_password: The user password for website read access.\n
        admin_password: The admin password for the website.\n
        cookie_secret_key: Key used for signing cookies.\n
        cookie_signing_salt: Salt used for cookie signing.\n
        disable_user_password_protection: Flag for disabling user password protection.\n
        disable_admin_password_protection: Flag for disabling admin password protection.\n
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
    Session-Cookie that is authenticated as user or admin. If ever used in production, wipe all cookies.
    """
    disable_user_password_protection: bool
    disable_admin_password_protection: bool

    @staticmethod
    def get_instance() -> 'Configuration':
        global _CONFIGURATION
        if _CONFIGURATION is None:
            _CONFIGURATION = load_configuration(_CONFIGURATION_PATH)
        return _CONFIGURATION


def read_config_path_from_environment_variables(path: str = 'config/example_config.json') -> str:
    """
    Read the file path from the environment variable TSVIEWER_CONFIGURATION_FILE if configured
    :param path: Path to the configuration file
    :return: The value of the environment variable
    """
    return environ.get(f'{ENVIRONMENT_VARIABLE_PREFIX}_FILE', path)


_CONFIGURATION_PATH = read_config_path_from_environment_variables()


def load_configuration(path: str) -> Configuration:
    """
    Loads the `Configuration` object from the config-file. If the configuration is already loaded, that instance is
    returned instead.
    :param path: Path to the configuration file
    :return: A `Configuration` file object
    """
    with resolve_with_project_path(path).open('r') as configuration_file:
        configuration = Configuration(**load(configuration_file))
    return configuration


def save_configuration(configuration: Configuration) -> None:
    """
    Saves a modified `Configuration` to the given path
    :param configuration: `Configuration` object
    """
    with resolve_with_project_path(_CONFIGURATION_PATH).open('w') as configuration_file:
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
