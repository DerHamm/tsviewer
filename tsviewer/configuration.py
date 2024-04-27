from tsviewer.ts_viewer_utils import resolve_with_project_path
from dataclasses import dataclass
from json import load, dump
import ts3.query


@dataclass
class Configuration(object):
    """
    Represents the configuration file
    """
    host: str
    port: int
    user: str
    password: str
    server_id: int
    teamspeak_install_path: str


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
    connection.login(client_login_name=configuration.user, client_login_password=configuration.password)
    connection.use(sid=configuration.server_id)
