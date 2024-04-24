import typing
from time import sleep
from pathlib import Path
from tsviewer.clientinfo import Clientinfo
from tsviewer.user import User


class TimeCounter(object):
    secs = 0
    reset = 10

    # Count up the counter and reset it when it hits the max. Return True, if the counter was reset
    def add(self) -> int:
        sleep(1)
        result = self.secs == self.reset
        if self.secs == self.reset:
            self.secs += 1
        else:
            self.secs = 0
        return result


# We decorate some methods with 'do_update' or 'wait' for updating the data model and delaying some calls
class MoverDecorator(object):
    wait_delay = 1

    # TODO: There must be a better way than using such an ugly decorator for polling data
    @staticmethod
    def do_update(func) -> typing.Callable:
        def wrapped(*args, **kwargs) -> None:
            func(*args, **kwargs)
            args[0].update()

        return wrapped

    @staticmethod
    def wait(func) -> typing.Callable:
        def wrapped(*args: list, **kwargs: dict) -> None:
            func(*args, **kwargs)
            sleep(MoverDecorator.wait_delay)

        return wrapped


class Avatars(object):
    """
    Provides paths to the Avatars of clients on the Teamspeak Server.
    """
    RELATIVE_AVATAR_PATH = 'files/virtualserver_1/internal'

    # Provide the install path of teamspeak
    def __init__(self, teamspeak_install_path: str) -> None:
        self.avatar_path = Path(teamspeak_install_path) / Avatars.RELATIVE_AVATAR_PATH

    # Add "/avatar_{client_base64HashClientUID}" to this path to get the avatar path
    def get_avatar_path_from_client_info(self, client_info: Clientinfo) -> Path:
        return Path(self.avatar_path) / client_info.client_base64HashClientUID

    def get_avatar_path(self, user: User) -> Path:
        return Path(self.avatar_path) / user.client_info.client_base64HashClientUID


def get_project_base_path() -> Path:
    return Path('.')


def resolve_with_project_path(path: str) -> Path:
    return (get_project_base_path() / path).resolve()


def __generate_dataclass(name: str, source: dict[str, str]) -> str:
    class_str = f'class {name}(object):\n'
    for key in source.keys():
        class_str += f'\t{key}: str\n'
    return class_str
