from pathlib import Path
from typing import Optional


def get_project_base_path() -> Path:
    """
    Return the projects base path
    :return: Path object to the project base path
    """
    return Path('.')


def resolve_with_project_path(path: str) -> Path:
    """
    Resolve a given path to the project's base path
    :param path: Path as string
    :return: Path object to the resolved path
    """
    return (get_project_base_path() / path).resolve()


def get_application_name() -> str:
    """
    Get the application name
    :return: A string representing the application's name
    """
    return f'{get_project_base_path().resolve().name}.app'


def create_directories() -> Optional[str]:
    """
    Create all non-existent directories that are being used by the TsViewer
    Currently, there are `2` directories not included in the project structure:
    /static/avatars
    /log
    """
    paths = ['static/avatars']
    for path_string in paths:
        path = Path(path_string)
        if path.is_dir():
            continue
        try:
            path.mkdir()
        except (FileNotFoundError, OSError) as exception:
            return f'Could not create directory {path} because of {exception}'
