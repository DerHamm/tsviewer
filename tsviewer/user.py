from tsviewer.clientinfo import ClientInfo
from abc import ABC, abstractmethod


class BaseUser(ABC):
    @abstractmethod
    def idle_time(self) -> str:
        raise NotImplementedError('This is an Interface')

    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError('This is an Interface')

    @abstractmethod
    def avatar_file_name(self) -> str:
        raise NotImplementedError('This is an Interface')


class FakeUser(BaseUser):
    def __init__(self, idle_time: str = None, name: str = None, avatar_file_name: str = None) -> None:
        self.avatar_file_name = avatar_file_name
        self.name = name
        self.idle_time = idle_time

    def idle_time(self) -> str:
        pass

    def name(self) -> str:
        pass

    def avatar_file_name(self) -> str:
        pass


class User(BaseUser):
    """ User is a representation of a clients information for displaying purposes.
     You have to provide a ``Clientinfo`` object to instantiate it"""

    def __init__(self, client_info: ClientInfo = None,
                 idle_time: str = None, name: str = 'dev', avatar_file_name: str = 'unnamed.jpg') -> None:
        """
        :param client_info: Instance of a ``Clientinfo`` returned by ``TsViewerClient.get_client_info()``
        """
        self.client_info = client_info

    @property
    def idle_time(self) -> str:
        idle_time_in_seconds = int(self.client_info.client_idle_time) / 1000
        if idle_time_in_seconds <= 10:
            return '-'
        elif idle_time_in_seconds <= 60:
            return f'{idle_time_in_seconds} seconds'
        elif idle_time_in_seconds <= 3600:
            return f'{int(idle_time_in_seconds / 60)} minutes'
        elif idle_time_in_seconds <= 86400:
            return f'{int(idle_time_in_seconds) / 60 / 60} hours'
        else:
            return f'More than 24 hours'

    @property
    def name(self) -> str:
        return self.client_info.client_nickname

    @property
    def avatar_file_name(self) -> str:
        return self.client_info.client_base64HashClientUID


def build_fake_user(idle_time: str = '~10 minutes', name: str = 'dev',
                    avatar_file_name: str = 'unnamed.jpg') -> BaseUser:
    return FakeUser(idle_time=idle_time, name=name, avatar_file_name=avatar_file_name)
