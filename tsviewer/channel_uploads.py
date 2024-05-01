
# Beware: This class ignores sub-folders within the channels
class ChannelUploads(object):

    RELATIVE_AVATAR_PATH = 'files/virtualserver_1/internal'

    """
    This class provides an interface to all uploaded files on the connected Teamspeak server.
    """
    def __init__(self, upload_channel_id: str) -> None:
        """
        `ChannelUploads` requires a designated upload channel for it`s functionalities.
        :param upload_channel_id: ID of the designated upload channel.
        """
        self.upload_channel_id = upload_channel_id

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

