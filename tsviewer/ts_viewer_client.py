import ts3
import random
from tsviewer.ts_viewer_utils import MoverDecorator, TimeCounter
from tsviewer.clientinfo import Clientinfo
from tsviewer.configuration import load_configuration, authorize
from tsviewer.user import User


class TsViewerClient(object):
    def __init__(self, path_to_configuration='config/example_config.json') -> None:
        self.configuration = load_configuration(path=path_to_configuration)
        self.connection = ts3.query.TS3Connection(self.configuration.HOST, self.configuration.PORT)
        authorize(self.configuration, self.connection)

        self.channel_ids = list()
        self.counter = TimeCounter()
        self.image_tags = dict()
        self.muted_tags = dict()

    def setup(self) -> None:
        self.get_client_id_list()
        self.get_channel_id_list()

    def update(self) -> None:
        if self.counter.add():
            self.setup()

    def clientinfo(self, clid: str) -> Clientinfo:
        return Clientinfo(**self.connection.clientinfo(clid=clid)._parsed[0])

    def keep_away(self, client_id: str, channel_id: str) -> None:
        client_channel_id = self.clientinfo(clid=client_id).cid
        if channel_id == client_channel_id:
            try:
                self.connection.clientmove(clid=client_id, cid=random.choice(self.channel_ids))
            except:
                print("Clientmove failed")
        self.update()

    @MoverDecorator.do_update
    def follow(self, follower_id: str, chased_id: str) -> None:
        chased = self.clientinfo(chased_id)
        follower = self.clientinfo(follower_id)
        if chased.cid == follower.cid:
            self.update()
            return None
        try:
            self.connection.clientmove(clid=follower_id, cid=int(chased.cid))
        except:
            print("Clientmove failed")

    @MoverDecorator.wait
    def move_around(self) -> None:
        for client_id in self.get_client_id_list():
            try:
                self.move(client_id, random.choice(self.channel_ids))
            except:
                print("Clientmove failed")

    @MoverDecorator.do_update
    def move(self, clid: str, cid: str) -> None:
        self.connection.clientmove(clid=clid, cid=cid)

    def get_client_id_list(self) -> list[str]:
        clients = self.connection.clientlist()
        return list(
                map(lambda x: x['clid'],
                    filter(lambda client: client['client_nickname'] != 'serveradmin', clients)))

    def get_channel_id_list(self) -> list[str]:
        channels = self.connection.channellist()
        self.channel_ids = list(map(lambda channel: channel['cid'], channels))
        return self.channel_ids

    def get_client_id_by_nickname(self, nickname: str) -> str:
        clients = self.connection.clientlist()
        searched_client = next(filter(lambda client: client['client_nickname'] == nickname, clients), dict())
        if searched_client.get('clid') is not None:
            return searched_client['clid']
        return str()

    def get_channel_id_by_name(self, name: str) -> str:
        channels = self.connection.channellist()
        searched_channel = next(filter(lambda channel: channel['channel_name'] == name, channels), dict())
        if searched_channel.get('cid') is not None:
            return searched_channel['cid']
        return str()

    def get_user_list(self) -> list[User]:
        users = list()
        for client_id in self.get_client_id_list():
            users.append(User(self.clientinfo(client_id)))
        return users
