from typing import Optional


class File(object):
    # Fields from Teamspeak Server Query Result
    cid: Optional[str]
    path: Optional[str]
    name: Optional[str]
    size: Optional[str]
    datetime: Optional[str]
    type: Optional[str]

    # TODO: Maybe we just implement it ourselves and map the kwargs to their correct names or something
    # The name `type` is already in outer scope, but this is needed for the dataclass to work
    # noinspection PyShadowingBuiltins
    def __init__(self, cid: str = None, path: str = None, name: str = None, size: str = None, datetime: str = None,
                 type: str = None, url: str = None) -> None:
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
        self.url = url

    def __repr__(self) -> str:
        return f'File[cid={self.cid}, path={self.path}, size={self.size}, datetime={self.datetime}]'

    def __str__(self) -> str:
        return repr(self)
