import copy
from tsviewer.clientinfo import ClientInfo, fake_user_base_client_info
import random
import string

from tsviewer.ts_viewer_utils import TimeUtil


class User(object):
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
        milliseconds = int(self.client_info.client_idle_time)
        if idle_time_in_seconds <= 10:
            return '-'
        elif idle_time_in_seconds <= 60:
            seconds = TimeUtil.to_seconds(milliseconds)
            plural = 's' if seconds > 1 else ''
            return f'{seconds} second' + plural
        elif idle_time_in_seconds <= 3600:
            minutes = TimeUtil.to_minutes(milliseconds)
            plural = 's' if minutes > 1 else ''
            return f'{minutes} minutes' + plural
        elif idle_time_in_seconds <= 86400:
            hours = TimeUtil.to_hours(milliseconds)
            plural = 's' if hours > 1 else ''
            return f'{hours} hour' + plural
        else:
            days = TimeUtil.to_days(milliseconds)
            plural = 's' if days > 1 else ''
            return f'{days} day' + plural

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

    def build_as_fake_user(self) -> User:
        fake_user_client_info = copy.copy(fake_user_base_client_info)

        fake_user_client_info.client_idle_time = self._idle_time
        fake_user_client_info.client_input_muted = self._microphone_status
        fake_user_client_info.client_output_muted = self._sound_status
        fake_user_client_info.client_nickname = self._name
        fake_user_client_info.client_base64HashClientUID = self._avatar_file_name

        return User(fake_user_client_info)

    def build(self) -> User:
        return User(self._client_info)


def build_fake_user(idle_time: str = None,
                    name: str = None,
                    avatar_file_name: str = None,
                    microphone_status: str = None,
                    sound_status: str = None) -> User:
    """
    Create a faked user for displaying purposes
    :param idle_time: Formatted idle time string
    :param name: Client nickname to be displayed
    :param avatar_file_name: This is the client's avatar file name
    :param sound_status: Client's volume output status
    :param microphone_status: Client's microphone output status
    :return: a faked user object
    """
    if idle_time is None:
        unit = random.choice([TimeUtil.from_seconds,
                              TimeUtil.from_minutes,
                              TimeUtil.from_hours,
                              TimeUtil.from_days,
                              lambda noop: noop])
        idle_time = unit(random.randint(1, 25))
    if name is None:
        name = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(4, 26)))
    if avatar_file_name is None:
        avatar_file_name = 'unnamed.jpg'
    if microphone_status is None:
        microphone_status = str(random.randint(0, 1))
    if sound_status is None:
        sound_status = str(random.randint(0, 1))

    # If needed, create a copy of `fake_user_base_client_info' and modify it for your purposes
    # With this approach it won't be complicated to add property based testing later on
    return UserBuilder().idle_time(idle_time).name(name).avatar_file_name(avatar_file_name).sound_status(
        sound_status).microphone_status(microphone_status).build_as_fake_user()
