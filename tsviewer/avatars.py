from pathlib import Path
from tsviewer.clientinfo import ClientInfo
from tsviewer.user import User
from shutil import copy2
from datetime import datetime, timezone


class Avatars(object):
    """
    Provides paths to the Avatars of clients on the Teamspeak Server.
    """
    RELATIVE_AVATAR_PATH_TEMPLATE = 'files/virtualserver_{server_id}/internal'

    def __init__(self, teamspeak_install_path: str, server_id: str = '1') -> None:
        """
        :param teamspeak_install_path: The path to the local Teamspeak installation
        """
        self.server_id = server_id
        self.avatar_path = Path(teamspeak_install_path) / self._get_relative_avatar_path()

    # Add "/avatar_{client_base64HashClientUID}" to this path to get the avatar path
    def get_avatar_path_from_client_info(self, client_info: ClientInfo) -> Path:
        """
        :param client_info: Clientinfo object of the client the avatar path is needed for
        :return: Path object to the avatar path
        """
        return Path(self.avatar_path) / client_info.client_base64HashClientUID

    def get_avatar_path(self, user: User) -> Path:
        """
        :param user: User object of the client the avatar path is needed for
        :return: Path object to the avatar path
        """
        return Path(self.avatar_path) / user.client_info.client_base64HashClientUID

    def update_avatars(self, user_list: list[User]) -> None:
        """
        Check which users are online and update their avatar images inside `static/uploads`
        :param: List of users that need an avatar update
        """
        path_map: dict[str: str]
        path_map = {self.get_avatar_path(user): f'static/uploads/{user.avatar_file_name}' for user in user_list}
        for src_path, dest_path in path_map.items():
            # Get the last modified timestamp of both avatar files
            last_modified_src = datetime.fromtimestamp(Path(src_path).stat().st_mtime, tz=timezone.utc)
            last_modified_dest = datetime.fromtimestamp(Path(dest_path).stat().st_mtime, tz=timezone.utc)
            # Check if more than seconds difference exists in between these timestamps, skip the copy if not
            if abs((last_modified_dest - last_modified_src).total_seconds()) <= 10:
                continue
            copy2(src_path, dest_path)

    def _get_relative_avatar_path(self) -> str:
        return Avatars.RELATIVE_AVATAR_PATH_TEMPLATE.format(server_id=self.server_id)
