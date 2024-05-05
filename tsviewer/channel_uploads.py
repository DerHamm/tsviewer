from pathlib import Path


# Beware: This class ignores sub-folders within the channels
class ChannelUploads(object):
    RELATIVE_CHANNEL_UPLOAD_PATH_TEMPLATE = 'files/virtualserver_{server_id}/internal'

    """
    This class provides an interface to all uploaded files on the connected Teamspeak server.
    """

    def __init__(self, teamspeak_install_path: str, upload_channel_id: str, server_id: str = '1') -> None:
        """
        `ChannelUploads` requires a designated upload channel for it`s functionalities.
        :param upload_channel_id: ID of the designated upload channel.
        """
        self.server_id = server_id
        self.upload_channel_id = upload_channel_id
        self.avatar_path = Path(teamspeak_install_path) / self._get_relative_channel_upload_path()

    def clean_up(self) -> None:
        """
        Moves all files that were uploaded to the server into the designated upload-channel
        """
        pass

    def update_upload_channel_description(self) -> None:
        """
        Create a new description string for the upload channel that lists and links all files located in that channel
        """
        pass

    def get_files(self) -> list[str]:
        """
        Get a list of all absolute file paths
        :return: list of file paths
        """
        pass

    def _get_files_from_channel(self, channel_id: str) -> list[str]:
        pass

    def _get_files_from_upload_channel(self) -> list[str]:
        return self._get_files_from_channel(self.upload_channel_id)

    def _move_files_to_upload_channel(self, files: list[str]) -> None:
        pass

    def _get_relative_channel_upload_path(self) -> str:
        return ChannelUploads.RELATIVE_CHANNEL_UPLOAD_PATH_TEMPLATE.format(server_id=self.server_id)
