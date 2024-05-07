from pathlib import Path

CLIENT_ID = 'clid'
CHANNEL_ID = 'cid'
CLIENT_NICKNAME = 'client_nickname'
CHANNEL_NAME = 'channel_name'


class TimeUtil(object):
    """
    Utility class for converting between milliseconds and seconds, minutes, etc.
    Just uses `int` for rounding (like math.floor)
    """

    @staticmethod
    def to_seconds(milliseconds: int) -> int:
        """
        Convert milliseconds to seconds
        :param milliseconds: the milliseconds to be converted
        :return: the seconds
        """
        return int(milliseconds / 1000)

    @staticmethod
    def to_minutes(milliseconds: int) -> int:
        """
        Convert milliseconds to minutes
        :param milliseconds: the milliseconds to be converted
        :return: the minutes
        """
        return int(milliseconds / 1000 / 60)

    @staticmethod
    def to_hours(milliseconds: int) -> int:
        """
        Convert milliseconds to hours
        :param milliseconds: the milliseconds to be converted
        :return: the hours
        """
        return int(milliseconds / 1000 / 60 / 60)

    @staticmethod
    def to_days(milliseconds: int) -> int:
        """
        Convert milliseconds to seconds
        :param milliseconds: the milliseconds to be converted
        :return: the seconds
        """
        return int(milliseconds / 1000 / 60 / 60 / 24)

    @staticmethod
    def from_seconds(seconds: int) -> int:
        """
        Convert seconds to milliseconds
        :param seconds: the seconds to be converted
        :return: the milliseconds
        """
        return seconds * 1000

    @staticmethod
    def from_minutes(minutes: int) -> int:
        """
        Convert minutes to milliseconds
        :param minutes: the minutes to be converted
        :return: the milliseconds
        """
        return minutes * 60 * 1000

    @staticmethod
    def from_hours(hours: int) -> int:
        """
        Convert hours to milliseconds
        :param hours: the hours to be converted
        :return: the milliseconds
        """
        return hours * 60 * 60 * 1000

    @staticmethod
    def from_days(days: int) -> int:
        """
        Convert days to milliseconds
        :param days: the days to be converted
        :return: the milliseconds
        """
        return days * 24 * 60 * 60 * 1000


def get_project_base_path() -> Path:
    """
    Return the projects base path
    :return: Path object to the project base path
    """
    return Path('.')


def resolve_with_project_path(path: str) -> Path:
    """
    Resolve a given path to the project's base path
    :param path: Path as string
    :return: Path object to the resolved path
    """
    return (get_project_base_path() / path).resolve()


def get_application_name() -> str:
    """
    Get the application name
    :return: A string representing the application's name
    """
    return f'{get_project_base_path().resolve().name}.app'


def is_admin(session: dict[str: str]) -> bool:
    """
    Checks if session contains the `admin` flag
    :param session: Session Dictionary
    :return: True if user is admin
    """
    return session.get('role') == 'admin'


def is_user(session: dict[str: str]) -> bool:
    """
    Checks if session contains the `user` flag
    :param session: Session Dictionary
    :return: True if user is a user
    """
    return session.get('role') == 'user'


def is_authenticated(session: dict[str: str]) -> bool:
    """
    Checks if session contains the `admin` or the `user` flag
    :param session: Session Dictionary
    :return: True if user is an admin or a user
    """
    return session.get('role') in ['user', 'admin']


def __generate_dataclass(name: str, source: dict[str, str]) -> str:
    """
    Generate code for a dataclass like `Clientinfo` by a given dict.
    The dict needed for this is returned by one of the `ts3.query.TS3Connection` commands
    :param name: Name for the class
    :param source: Source `dict` for the class
    :return: The generated code as a string
    """
    class_str = f'class {name}(object):\n'
    for key in source.keys():
        class_str += f'\t{key}: str\n'
    return class_str
