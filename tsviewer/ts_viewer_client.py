import typing

import ts3
import random

from tsviewer.clientinfo import ClientInfo
from tsviewer.configuration import authorize, Configuration
from tsviewer.logger import logger
from tsviewer.user import User
from tsviewer.ts_viewer_utils import CLIENT_ID, CHANNEL_ID, CLIENT_NICKNAME, CHANNEL_NAME, display_error


# TODO: Error handling with msg=ok and statuscode check where needed
class TsViewerClient(object):
    """
    This class is essentially a wrapper around the `ts3`-API.
    It provides some extra methods and uses the configuration to acquire a connection to the Teamspeak Server.
    """

    def __init__(self, configuration: Configuration = None) -> None:
        """
        Connects and authorizes against the configurated Teamspeak Server.
        Exit the application if not connection could be build
        :param configuration: Configuration File object
        """
        self.configuration = configuration
        try:

            self.connection = ts3.query.TS3Connection(self.configuration.server_query_host,
                                                      self.configuration.server_query_port)
            authorize(self.configuration, self.connection)
            # TODO: Update the channel ids at some point
            self.channel_ids = self.get_channel_id_list()

        except (ts3.TS3Error, ConnectionRefusedError) as connection_error:
            message = f'Could not connect to host at: ' \
                      f'{configuration.server_query_host}:{configuration.server_query_port}\n'
            display_error(message, connection_error)
            logger.error(message, connection_error)
            self.connection = None

    def get_client_info(self, clid: str) -> ClientInfo:
        """
        Return a representation of the Teamspeak `clientinfo` command. The `ClientInfo` type exists to make development
        easier as the `ts3` library only returns a dict-representation of the issued command.
        :param clid: Client ID
        :return: A `Clientinfo` object containing detailed information about the client
        """
        # noinspection PyProtectedMember
        return ClientInfo(**self.connection.clientinfo(clid=clid)._parsed[0])

    """
    The following methods `keep_away`, `follow`, and `move_around` are all funny little utilities, that can be used
    in loops or events to cause some havoc on the Teamspeak.
    """

    def keep_away(self, client_id: str, channel_id: str) -> None:
        """
        Remove a client from a given channel, if he currently is in that channel.
        :param client_id: Client ID
        :param channel_id: Channel ID
        """
        client_channel_id = self.get_client_info(clid=client_id).cid
        if channel_id == client_channel_id:
            try:
                self.move(client_id, random.choice(self.channel_ids))
            except (ts3.TS3Error, Exception) as error:
                print(f'Clientmove failed: {error}')

    def follow(self, follower_client_id: str, chased_client_id: str) -> None:
        """
        Let a client follow another client
        :param follower_client_id: Client ID of the following client
        :param chased_client_id: Client ID of the client being chased
        """
        chased = self.get_client_info(chased_client_id)
        follower = self.get_client_info(follower_client_id)
        if chased.cid == follower.cid:
            return None
        try:
            self.move(follower_client_id, chased.cid)
        except (ts3.TS3Error, Exception) as error:
            print(f'Clientmove failed: {error}')

    def move_around(self) -> None:
        """
        Move all clients into random channels.
        """
        for client_id in self.get_client_id_list():
            try:
                self.move(client_id, random.choice(self.channel_ids))
            except (ts3.TS3Error, Exception) as error:
                print(f'Clientmove failed: {error}')

    def move(self, client_id: str, channel_id: str) -> None:
        """
        Wrapper around the `clientmove` method of `ts3`.
        """
        self.connection.clientmove(clid=client_id, cid=channel_id)

    def get_client_id_list(self) -> list[str]:
        """
        Get a list of all client IDs besides the Query user client
        :return: A list of all client IDs
        """
        clients = self.connection.clientlist()
        return list(
            map(lambda client: client[CLIENT_ID],
                filter(lambda client: client[CLIENT_NICKNAME] != self.configuration.server_query_user, clients)))

    def get_channel_id_list(self, filter_by: typing.Callable = None) -> list[str]:
        """
        Get a list of all channel IDs
        :param filter_by: A callable that can filter out certain channel IDs
        :return: A list of all channel IDs
        """
        channels = self.connection.channellist()
        if filter_by is not None:
            self.channel_ids = filter(channels, list(map(lambda channel: channel[CHANNEL_ID], channels)))
        else:
            self.channel_ids = list(map(lambda channel: channel[CHANNEL_ID], channels))
        return self.channel_ids

    def get_client_id_by_nickname(self, nickname: str) -> str:
        """
        Finds a client by its nickname
        :param nickname: The clients nickname
        :return: The clients ID
        """
        clients = self.connection.clientlist()
        searched_client = next(filter(lambda client: client[CLIENT_NICKNAME] == nickname, clients), dict())
        return searched_client.get(CLIENT_ID, str())

    def get_channel_id_by_name(self, name: str) -> str:
        """
        Finds a channel by its name
        :param name: The channel name
        :return: The channel ID
        """
        channels = self.connection.channellist()
        searched_channel = next(filter(lambda channel: channel[CHANNEL_NAME] == name, channels), dict())
        return searched_channel.get(CHANNEL_ID, str())

    def get_user_list(self) -> list[User]:
        """
        Get a list of all users represented as the `User` object. This class is a Frontend-Representation of a client
        :return:
        """
        users = list()
        for client_id in self.get_client_id_list():
            users.append(User(self.get_client_info(client_id)))
        return users

    def init_file_download(self, file_name: str, channel_id: str) -> ts3.query.TS3QueryResponse:
        """
        Initialize a file download and return the response
        :param file_name: File name of the file to be downloaded
        :param channel_id: The target channel id
        :return: The response object
        """
        download_response = self.connection.ftinitdownload(clientftfid=random.randint(1, 64000),
                                                           name=f"/{file_name}",
                                                           cid=channel_id,
                                                           seekpos=0)

        return download_response

    def get_file_list(self, channel_id: str) -> typing.Optional[ts3.query.TS3QueryResponse]:
        """
        Get a list of all files in a channel
        :param channel_id: The target channel id
        :return: The response or None if an exception was raised
        """
        response = None
        try:
            response = self.connection.ftgetfilelist(cid=channel_id, path='/')
        except ts3.query.TS3QueryError as exception:
            # We use debug here, because usually an exception is thrown when the channel is just empty
            logger.debug(exception)
        return response

    def edit_channel_description(self, channel_id: str, text: str) -> None:
        """
        Edit a channels' description
        :param channel_id: Target channel id
        :param text: New channel description
        """
        self.connection.channeledit(cid=channel_id, channel_description=text)

    def move_file(self, channel_id: str, target_channel_id: str, file_name: str, new_file_name: str = None) -> None:
        """
        Moves (or renames) a file
        :param channel_id: The channel id where the file currently is located at
        :param target_channel_id: The target channel id
        :param file_name: The file name of the file
        :param new_file_name: The new name for the file after moving it (optional)
        """
        if new_file_name is None:
            new_file_name = file_name
        try:
            self.connection.ftrenamefile(cid=channel_id,
                                         tcid=target_channel_id,
                                         oldname=f'/{file_name}', newname=f'/{new_file_name}',
                                         tcpw=str(), cpw=str())
            logger.info(f'File successfully moved from cid={channel_id} to tcid={target_channel_id}')
        except ts3.query.TS3QueryError as exception:
            logger.error(exception)
            quit()

    def who_am_i(self) -> ts3.query.TS3QueryResponse:
        """
        :return: Teamspeak `whoami` command response
        """
        return self.connection.whoami()
