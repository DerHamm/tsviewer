from pathlib import Path
from tsviewer.clientinfo import ClientInfo
from tsviewer.user import User, BaseUser
from shutil import copy2


class Avatars(object):
    """
    Provides paths to the Avatars of clients on the Teamspeak Server.
    """
    RELATIVE_AVATAR_PATH = 'files/virtualserver_1/internal'

    # Provide the install path of teamspeak
    def __init__(self, teamspeak_install_path: str) -> None:
        self.avatar_path = Path(teamspeak_install_path) / Avatars.RELATIVE_AVATAR_PATH

    # Add "/avatar_{client_base64HashClientUID}" to this path to get the avatar path
    def get_avatar_path_from_client_info(self, client_info: ClientInfo) -> Path:
        return Path(self.avatar_path) / client_info.client_base64HashClientUID

    def get_avatar_path(self, user: User) -> Path:
        return Path(self.avatar_path) / user.client_info.client_base64HashClientUID

    def update_avatars(self, user_list: list[User]) -> None:
        """ Check which users are online and update their avatar images inside `static/uploads` """
        path_map = {self.get_avatar_path(user): f'static/uploads/{user.avatar_file_name}' for user in user_list}
        # TODO: We can use an exist check and a timestamp check, so that we really only update the necessary avatars
        for src_path, dest_path in path_map.items():
            copy2(src_path, dest_path)


