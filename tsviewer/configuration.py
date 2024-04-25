from tsviewer.ts_viewer_utils import resolve_with_project_path
from dataclasses import dataclass
from json import load, dump
import ts3.query


@dataclass
class Configuration(object):
    HOST: str
    PORT: int
    USER: str
    PASS: str
    SERVER_ID: int
    TEAMSPEAK_INSTALL_PATH: str


def load_configuration(path='config/example_config.json') -> Configuration:
    with resolve_with_project_path(path).open('r') as configuration_file:
        return Configuration(**load(configuration_file))


def save_configuration(configuration: Configuration, path='config/example_config.json') -> None:
    with resolve_with_project_path(path).open('w') as configuration_file:
        dump(configuration.__dict__, configuration_file)


def authorize(configuration: Configuration, connection: ts3.query.TS3Connection) -> None:
    connection.login(client_login_name=configuration.USER, client_login_password=configuration.PASS)
    connection.use(sid=configuration.SERVER_ID)
