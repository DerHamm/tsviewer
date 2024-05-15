import dataclasses
from typing import Optional


@dataclasses.dataclass
class File(object):
    cid: str
    path: str
    name: str
    size: str
    datetime: str
    type: str

    def __init__(self, cid: str = '', path: str = '', name: str = '', size: str = '', datetime: str = '',
                 type: str = '') -> None:
        """
        File object for the files returned by the FTGETFILELIST command
        :param cid: The channel id (optional)
        :param path: The path (optional)
        :param name: The file name
        :param size: Size in bytes
        :param datetime: Unix timestamp
        :param type: TODO: What even is this? Do we need it?
        """
        self.cid = cid
        self.path = path
        self.name = name
        self.size = size
        self.datetime = datetime
        self.type = type
