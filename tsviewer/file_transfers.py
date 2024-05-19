import os
import socket
from typing import Optional

import ts3
from time import sleep
from pathlib import Path
from imghdr import what
from io import BytesIO
from tsviewer.configuration import Configuration
from tsviewer.logger import logger
from tsviewer.ts_viewer_utils import TimeUtil, DownloadResponseWrapper

__all__ = ['download_file', 'upload_file']


def download_file(file_transfer_init_download_response: ts3.query.TS3QueryResponse, file_name: str) \
        -> tuple[Optional[str], bytes]:
    """
    This starts the file transfer initiated by the `FTINITDOWNLOADFILE` command
    :param file_transfer_init_download_response: The response object of the `FTINITDOWNLOADFILE`
    :param file_name: The file name for the file that is written to the `static` folder
    :return: The file path of the created file as string or `None`
    """
    configuration = Configuration.get_instance()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(file_transfer_init_download_response.parsed[0].get('port', 30033))
    address = (configuration.server_query_host, port)
    image = b''
    try:
        sock.connect(address)
        print("Connected to socket")
        sock.sendall(file_transfer_init_download_response.parsed[0]['ftkey'].encode())
        print("Sent ftkey")
        size = int(file_transfer_init_download_response.parsed[0]['size'])
        print("Got size")
        while True:
            response_bytes = sock.recv(size)
            print("Obtaining data..")
            image += response_bytes
            sleep(TimeUtil.to_milliseconds(250))
            if response_bytes == b'':
                break

        logger.info(f'File successfully downloaded')
    except (socket.error, OSError, ts3.query.TS3QueryError, Exception) as exception:
        error_message = f'Due to the exception {exception} the download of file {file_name} did not succeed'
        logger.error(error_message)
    finally:
        sock.close()
    return file_name, image


def write_to_disk(path_and_bytes: tuple[Optional[str], bytes]) -> None:
    file_name, image = path_and_bytes
    file_extension = what(BytesIO(image))
    file_path = f'static/avatars/{file_name}.{file_extension}'
    with Path(file_path).open('wb') as avatar_file:
        avatar_file.write(image)
        logger.info(f'File successfully written to {file_path}')


def download_file_from_wrapper(download_response_wrapper: DownloadResponseWrapper) \
        -> tuple[Optional[str], bytes]:
    return download_file(download_response_wrapper.file_transfer_init_download_response,
                         download_response_wrapper.file_name)


def upload_file(file_transfer_init_upload_response: ts3.query.TS3QueryResponse, file_name: os.PathLike) -> None:
    # TODO: Test this
    """
    This starts the file transfer initiated by the `FTINITUPLOADFILE` command
    :param file_transfer_init_upload_response: The response object of the `FTINITUPLOADFILE`
    :param file_name: The file name for the file that is uploaded to the channel specified prior
    """

    with Path(file_name).open('rb') as file:
        content = file.read()

    configuration = Configuration.get_instance()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(file_transfer_init_upload_response.parsed[0].get('port', 30033))
    address = (configuration.server_query_host, port)
    try:
        sock.connect(address)
        sock.sendall(file_transfer_init_upload_response.parsed[0]['ftkey'].encode())
        sleep(TimeUtil.to_milliseconds(400))
        sock.sendall(content)
        logger.info(f'File successfully uploaded')
    except (socket.error, OSError, ts3.query.TS3QueryError, Exception) as exception:
        error_message = f'Due to the exception {exception} the upload of file {file_name} did not succeed'
        logger.error(error_message)
    finally:
        sock.close()
