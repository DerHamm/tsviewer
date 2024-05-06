import copy

from tsviewer.clientinfo import ClientInfo, fake_user_base_client_info
from abc import ABC, abstractmethod


class BaseUser(ABC):
    """
    Base user objects. This only exists for polymorphism between `User` and `FakeUser`
    """

    client_info: ClientInfo

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

    def __init__(self, client_info: ClientInfo) -> None:
        self.client_info = client_info
        self._idle_time = None
        self._microphone_status = None
        self._sound_status = None
        self._name = None
        self._avatar_file_name = None
        for key, value in client_info.__dict__.items():
            self.__setattr__(key, value)

    @property
    def idle_time(self) -> str:
        return self._idle_time

    @property
    def name(self) -> str:
        return self._name

    @property
    def avatar_file_name(self) -> str:
        return self._avatar_file_name

    @property
    def microphone_status(self) -> str:
        return self._microphone_status

    @property
    def sound_status(self) -> str:
        return self._sound_status


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

    def __repr__(self) -> str:
        return f'User[name={self.name}]'

    def __str__(self) -> str:
        return repr(self)


class UserBuilder(object):
    """
    This class is builder for `User` and `FakeUser` objects. It's not intensively used yet, but it will ease the
    testing process once the test scenarios become more complicated
    """
    def __init__(self, idle_time: str = None, name: str = None, avatar_file_name: str = None,
                 microphone_status: str = None, sound_status: str = None, client_info: ClientInfo = None) -> None:
        self._idle_time = idle_time
        self._name = name
        self._avatar_file_name = avatar_file_name
        self._microphone_status = microphone_status
        self._sound_status = sound_status
        self._client_info = client_info

    def idle_time(self, idle_time: str) -> 'UserBuilder':
        self._idle_time = idle_time
        return self

    def name(self, name: str) -> 'UserBuilder':
        self._name = name
        return self

    def avatar_file_name(self, avatar_file_name: str) -> 'UserBuilder':
        self._avatar_file_name = avatar_file_name
        return self

    def microphone_status(self, microphone_status: str) -> 'UserBuilder':
        self._microphone_status = microphone_status
        return self

    def sound_status(self, sound_status: str) -> 'UserBuilder':
        self._sound_status = sound_status
        return self

    def client_info(self, client_info: ClientInfo) -> 'UserBuilder':
        self._client_info = client_info
        return self

    # TODO: Use the original client info values in the `FakeUser` as well, otherwise this method doesn't make much sense
    def build_as_fake_user(self) -> BaseUser:
        fake_user_client_info = copy.copy(fake_user_base_client_info)

        fake_user_client_info.client_idle_time = self._idle_time
        fake_user_client_info.client_input_muted = self._microphone_status
        fake_user_client_info.client_output_muted = self._sound_status
        fake_user_client_info.client_nickname = self._name
        fake_user_client_info.client_base64HashClientUID = self._avatar_file_name

        fake_user = FakeUser(fake_user_client_info)

        fake_user._idle_time = self._idle_time
        fake_user._microphone_status = self._microphone_status
        fake_user._sound_status = self._sound_status
        fake_user._name = self._name
        fake_user._avatar_file_name = self._avatar_file_name

        return fake_user

    def build(self) -> BaseUser:
        return User(self._client_info)


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
    # If needed, create a copy of `fake_user_base_client_info' and modify it for your purposes
    # With this approach it won't be complicated to add property based testing later on
    return UserBuilder().idle_time(idle_time).name(name).avatar_file_name(avatar_file_name).sound_status(
        sound_status).microphone_status(microphone_status).build_as_fake_user()
