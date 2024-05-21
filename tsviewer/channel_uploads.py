# Beware: This class ignores sub-folders within the channels
from typing import Optional

from tsviewer.configuration import Configuration
from tsviewer.ts_viewer_client import TsViewerClient
from tsviewer.logger import logger
from urllib.parse import quote

from tsviewer.file_transfers import download_file


class ChannelUploads(object):
    """
    This class provides an interface to all uploaded files on the connected Teamspeak server.
    """
    AVATAR_CHANNEL_ID = '0'

    def __init__(self, client: 'TsViewerClient') -> None:
        """
        `ChannelUploads` requires a designated upload channel for it`s functionalities.
        :param client: Instance of `TsViewerClient`
        """
        self.upload_channel_id = Configuration.get_instance().upload_channel_id
        self.client = client
        self.files = None
        self.channel_to_file_map = dict()

    def clean_up(self) -> None:
        """
        Moves all files that were uploaded to the server into the designated upload-channel
        """
        self.get_files()
        self._move_files_to_upload_channel()
        self.update_upload_channel_description()

    def update_upload_channel_description(self) -> None:
        """
        Create a new description string for the upload channel that lists and links all files located in that channel
        """
        server_uid = self.client.who_am_i()[0]['virtualserver_unique_identifier']
        upload_channel_files = self._get_files_from_upload_channel()
        configuration = Configuration.get_instance()
        tag_list = list()
        for file in upload_channel_files:
            tag = ChannelUploads._format_url_as_bb_code_link_for_channel_description(configuration.server_query_host,
                                                                                     str(configuration.server_voice_port),
                                                                                     server_uid,
                                                                                     self.upload_channel_id,
                                                                                     file['name'],
                                                                                     file['size'],
                                                                                     file['datetime'])
            tag_list.append(tag)
        self.client.edit_channel_description(configuration.upload_channel_id, '\n\n'.join(tag_list))

    def get_files(self) -> list[list[dict[str: str]]]:
        """
        Get a list of all files and updates the attribute `files` and `channel_to_file_map`
        :return: list of file paths
        """
        files = list()
        channel_to_file_map = dict()
        for cid in self.client.get_channel_id_list():
            raw_files = self.client.get_file_list(cid)
            if raw_files is not None:
                raw_files = raw_files.parsed
            else:
                continue
            files.append(raw_files)
            channel_to_file_map[cid] = list()
            for file_list in raw_files:
                channel_to_file_map[cid].append(file_list)

        self.files = files
        self.channel_to_file_map = channel_to_file_map
        return files

    def download_avatars_to_static_folder(self) -> None:
        """
        Downloads all avatars to the static folder
        """
        from multiprocessing.pool import ThreadPool

        raw_files = self.client.get_file_list(ChannelUploads.AVATAR_CHANNEL_ID).parsed
        downloaded_files = 0
        response_file_name_list = list()

        for file in raw_files:
            if file.get('name') == 'icons':
                continue
            #downloaded_files += self.download_avatar(file['name']) is not None
            download_response = self.client.init_file_download(file['name'], ChannelUploads.AVATAR_CHANNEL_ID)

            response_file_name_list.append((file['name'], download_response))

        #with ThreadPool(processes=6) as pool:
        #    pool.map(download_file, response_file_name_list)
        logger.info(f'Downloaded {downloaded_files} out of {len(raw_files) - 1} requested avatar images')

    def download_avatar(self, file_name: str) -> Optional[str]:
        """
        Download an avatar specified by the file name / client uid
        :param file_name: The file name / client uid
        :return: The response of `download_file`
        """
        download_response = self.client.init_file_download(file_name, ChannelUploads.AVATAR_CHANNEL_ID)
        return download_file(download_response, file_name)

    def _get_files_from_channel(self, channel_id: str) -> list[str]:
        return self.channel_to_file_map.get(channel_id)

    def _get_files_from_upload_channel(self) -> list[dict[str: str]]:
        return self._get_files_from_channel(self.upload_channel_id)

    def _move_files_to_upload_channel(self) -> None:
        for cid, files in self.channel_to_file_map.items():
            if cid == self.upload_channel_id:
                continue
            for file in files:
                self.client.move_file(cid, self.upload_channel_id, file['name'])

    @staticmethod
    def _format_url_as_bb_code_link_for_channel_description(host: str, port: str, server_uid: str, channel_id: str,
                                                            file_name: str,
                                                            size: str,
                                                            file_date_time: str) -> str:
        return ChannelUploads._wrap_as_url_tag(
            ChannelUploads.format_url_as_link_in_channel_description(host, port, server_uid, channel_id, file_name,
                                                                     size,
                                                                     file_date_time),
            file_name)

    @staticmethod

    # TODO: Document those methods
    def format_url_as_link_in_channel_description(host: str, port: str, server_uid: str, channel_id: str,
                                                  file_name: str,
                                                  size: str,
                                                  file_date_time: str) -> str:
        url = f'ts3file://{host}?port={port}&serverUID={quote(server_uid)}&channel={channel_id}' \
              f'&path=%2F&filename={quote(file_name)}&isDir=0&size={size}&fileDateTime={file_date_time}'
        return url

    @staticmethod
    def _wrap_as_url_tag(url: str, file_name: str) -> str:
        return f'[URL={url}]{file_name}[/URL]'
