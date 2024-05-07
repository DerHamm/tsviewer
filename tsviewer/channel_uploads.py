
# Beware: This class ignores sub-folders within the channels
import ts3

from tsviewer.ts_viewer_client import TsViewerClient


class ChannelUploads(object):

    """
    This class provides an interface to all uploaded files on the connected Teamspeak server.
    """

    def __init__(self, upload_channel_id: str, client: 'TsViewerClient') -> None:
        """
        `ChannelUploads` requires a designated upload channel for it`s functionalities.
        :param upload_channel_id: ID of the designated upload channel.
        """
        self.upload_channel_id = upload_channel_id
        self.client = client
        self.all_files = self.get_files()

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

    def get_files(self) -> list[dict[str: str]]:
        """
        Get a list of all files
        :return: list of file paths
        """
        files = list()
        for cid in self.client.get_channel_id_list():
            try:
                files.append(list(self.client.connection.ftgetfilelist(cid=cid, path='/')))
            except ts3.query.TS3QueryError as exception:
                # TODO: Log the exception, but don't print it
                print(f'Error for channel id {cid}. Assuming channel is empty')
        return files

    def _get_files_from_channel(self, channel_id: str) -> list[str]:
        return self.all_files.get()

    def _get_files_from_upload_channel(self) -> list[str]:
        return self._get_files_from_channel(self.upload_channel_id)

    def _move_files_to_upload_channel(self, files: list[str]) -> None:
        pass
