from tsviewer.clientinfo import ClientInfo
from abc import ABC, abstractmethod


class BaseUser(ABC):
    """
    Base user objects. This only exists for polymorphism between `User` and `FakeUser`
    """

    @abstractmethod
    def idle_time(self) -> str:
        raise NotImplementedError('This is an Interface')

    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError('This is an Interface')

    @abstractmethod
    def avatar_file_name(self) -> str:
        raise NotImplementedError('This is an Interface')

    @abstractmethod
    def microphone_status(self) -> str:
        raise NotImplementedError('This is an Interface')

    @abstractmethod
    def sound_status(self) -> str:
        raise NotImplementedError('This is an Interface')


class FakeUser(BaseUser):
    """ Faked users Object for displaying purposes """

    def __init__(self, idle_time: str = None, name: str = None, avatar_file_name: str = None,
                 microphone_status: str = None, sound_status: str = None) -> None:
        self.avatar_file_name = avatar_file_name
        self.name = name
        self.idle_time = idle_time
        self.microphone_status = microphone_status
        self.sound_status = sound_status

    def idle_time(self) -> str:
        pass

    def name(self) -> str:
        pass

    def avatar_file_name(self) -> str:
        pass

    def microphone_status(self) -> str:
        pass

    def sound_status(self) -> str:
        pass


class User(BaseUser):
    """ User is a representation of a client's information for displaying purposes.
     You have to provide a ``ClientInfo`` object to instantiate it"""

    def __init__(self, client_info: ClientInfo = None) -> None:
        """
        :param client_info: Instance of a ``Clientinfo`` returned by ``TsViewerClient.get_client_info()``
        """
        self.client_info = client_info

    @property
    def idle_time(self) -> str:
        """
        Create a string that contains an approximation of how long afk a client has been
        :return: Formatted Client AFK time
        """
        idle_time_in_seconds = int(self.client_info.client_idle_time) / 1000
        if idle_time_in_seconds <= 10:
            return '-'
        elif idle_time_in_seconds <= 60:
            return f'{int(idle_time_in_seconds)} seconds'
        elif idle_time_in_seconds <= 3600:
            return f'{int(idle_time_in_seconds / 60)} minutes'
        elif idle_time_in_seconds <= 86400:
            return f'{int(idle_time_in_seconds) / 60 / 60} hours'
        else:
            return f'More than 24 hours'

    @property
    def name(self) -> str:
        """
        :return: The Clients Nickname
        """
        return self.client_info.client_nickname

    @property
    def avatar_file_name(self) -> str:
        """
        Shorthand for the `ClientInfo.client_base64HashClientUID`
        :return: Clients avatar filename
        """
        return self.client_info.client_base64HashClientUID

    @property
    def microphone_status(self) -> str:
        """
        Return an icon key for display purposes
        :return: `mic-mute` or `mic` depending on the clients mic-status
        """
        return 'mic-mute' if self.client_info.client_input_muted == '1' else 'mic'

    @property
    def sound_status(self) -> str:
        """
        Return an icon key for display purposes
        :return: `volume-mute` or `volume-up` depending on the clients sound-status
        """
        return 'volume-mute' if self.client_info.client_output_muted == '1' else 'volume-up'


def build_fake_user(idle_time: str = '~10 minutes',
                    name: str = 'dev',
                    avatar_file_name: str = 'unnamed.jpg',
                    microphone_status: str = 'mic',
                    sound_status: str = 'volume-mute') -> BaseUser:
    """
    Create a faked user for displaying purposes
    :param idle_time: Formatted idle time string
    :param name: Client nickname to be displayed
    :param avatar_file_name: This is the client's avatar file name
    :param sound_status: Client's volume output status
    :param microphone_status: Client's microphone output status
    :return: a faked user object
    """
    return FakeUser(idle_time=idle_time, name=name, avatar_file_name=avatar_file_name,
                    microphone_status=microphone_status, sound_status=sound_status)
