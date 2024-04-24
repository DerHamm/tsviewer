import typing
from tsviewer.ts_viewer_client import TsViewerClient
from flask import Flask
from pathlib import Path
from flask import render_template_string
from tsviewer.ts_viewer_utils import resolve_with_project_path, Avatars

# TODO: Maybe replace the dependency ts3 or at least try to make it more usable
# TODO: Add frontend (Flask)
# TODO: Split up classes into files and create a module
# TODO: add logging
# TODO: catch exceptions and log them

TEMPLATE_CACHE = dict()
# Jinja cant find the template with Flasks' render_template methode, so we use our own one for now
def render_template(path: typing.Union[Path, str], **kwargs) -> str:
    absolute_path = Path(path).resolve()
    content = TEMPLATE_CACHE.get(absolute_path)
    if content is None:
        with absolute_path.open('r') as template_file:
            content = template_file.read()
        TEMPLATE_CACHE[absolute_path] = content
    return render_template_string(content, **kwargs)


if __name__:
    client = TsViewerClient(path_to_configuration='config/config.json')
    client.setup()
    app = Flask(__name__)

    @app.route("/")
    def index():
        users = client.get_user_list()
        avatars = Avatars(client.configuration.TEAMSPEAK_INSTALL_PATH)
        # mulitply users times 10 for testing purposes
        users *= 10
        return render_template(resolve_with_project_path('template/index.html'), users=users, avatars=avatars)
