from tsviewer.clientinfo import Clientinfo


class User:
    """ User is a representation of a clients information for displaying purposes.
     You have to provide a ``Clientinfo`` object to instantiate it"""

    def __init__(self, client_info: Clientinfo) -> None:
        """
        :param client_info: Instance of a ``Clientinfo`` returned by ``TsViewerClient.clientinfo()``
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