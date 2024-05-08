# Beware: This class ignores sub-folders within the channels
import ts3

from tsviewer.configuration import Configuration
from tsviewer.ts_viewer_client import TsViewerClient
from urllib.parse import quote


def _format_url(host: str, port: str, server_uid: str, channel_id: str, file_name: str, size: str,
                file_date_time: str) -> str:
    url = f'ts3file://{host}?port={port}&serverUID={quote(server_uid)}&channel={channel_id}&path=%2F&filename={quote(file_name)}&isDir=0&size={size}&fileDateTime={file_date_time} '
    channel_description_line_for_file = f'[URL={url}]{file_name}[/URL]'
    return channel_description_line_for_file


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
        self.files = None
        self.channel_to_file_map = dict()
        self.get_files()

    def clean_up(self) -> None:
        """
        Moves all files that were uploaded to the server into the designated upload-channel
        """
        self.get_files()
        for cid, files in self.channel_to_file_map.items():
            if cid == self.upload_channel_id:
                continue
            for file in files:
                file_name = file['name']
                try:
                    self.move_file_to_upload_channel(cid, file_name)
                except ts3.query.TS3QueryError as exception:
                    print(exception, f'Error while moving files to the upload channel')
                    quit(0)
        # TODO: Channel description

    def move_file_to_upload_channel(self, target_channel_id: str, file_name: str) -> None:
        """
        Move a single file to the configured upload channel.
        :param target_channel_id: The channel id of the file to be moved
        :param file_name: File name of the file to be moved
        """
        self.client.connection.ftrenamefile(cid=target_channel_id,
                                            tcid=self.upload_channel_id,
                                            oldname=f'/{file_name}', newname=f'/{file_name}',
                                            tcpw='', cpw='')

    def update_upload_channel_description(self) -> None:
        """
        Create a new description string for the upload channel that lists and links all files located in that channel
        """
        # TODO: Remove this. Can we get it with a command or do we have to configure it?
        SERVER_UID = '1311ly07mh76Y2IJbhpZL+iRQsY='
        upload_channel_files = self._get_files_from_upload_channel()
        configuration = Configuration.get_instance()
        tag_list = list()
        for file in upload_channel_files:
            tag = _format_url(configuration.server_query_host, str(configuration.server_voice_port), SERVER_UID,
                              self.upload_channel_id, file['name'], file['size'], file['datetime'])
            tag_list.append(tag)
        self.client.connection.channeledit(cid=configuration.upload_channel_id,
                                           channel_description='\n\n'.join(tag_list))

    def get_files(self) -> list[list[dict[str: str]]]:
        """
        Get a list of all files and updates the attribute `files` and `channel_to_file_map`
        :return: list of file paths
        """
        files = list()
        channel_to_file_map = dict()
        for cid in self.client.get_channel_id_list():
            try:
                raw_files = self.client.connection.ftgetfilelist(cid=cid, path='/').parsed
                files.append(raw_files)
                channel_to_file_map[cid] = list()
                for file_list in raw_files:
                    channel_to_file_map[cid].append(file_list)
            except ts3.query.TS3QueryError as exception:
                # TODO: Log the exception, but don't print it
                print(f'Error for channel id {cid}. Assuming channel is empty. Exception: {exception}')
        self.files = files
        self.channel_to_file_map = channel_to_file_map
        return files

    def _get_files_from_channel(self, channel_id: str) -> list[str]:
        return self.channel_to_file_map.get(channel_id)

    def _get_files_from_upload_channel(self) -> list[dict[str: str]]:
        return self._get_files_from_channel(self.upload_channel_id)

    def _move_files_to_upload_channel(self, files: list[str]) -> None:
        pass
