import random
from tsviewer.ts_viewer_client import TsViewerClient
from flask import Flask, render_template
from tsviewer.avatars import Avatars
from tsviewer.user import build_fake_user, User
from tsviewer.ts_viewer_utils import get_application_name
import os
from tsviewer.configuration import load_configuration

FLASK_APPLICATION_NAME = f'{get_application_name()}.app'


def read_config_path_from_environment_variables(default_path: str = 'config/config.json') -> str:
    return os.environ.get('TSVIEWER_CONFIGURATION_FILE', default_path)


if __name__ in ['__main__', FLASK_APPLICATION_NAME]:
    client = TsViewerClient(load_configuration(read_config_path_from_environment_variables()))
    app = Flask(FLASK_APPLICATION_NAME, template_folder='template')
    avatars = Avatars(client.configuration.teamspeak_install_path)


    @app.route("/")
    def index():
        # users = client.get_user_list()
        users = [build_fake_user()] * 10

        if users and isinstance(users[0], User):
            avatars.update_avatars(users)

        # mulitply users times 10 for testing purposes
        return render_template('index.html', users=users, avatars=avatars,
                               f=lambda: random.choice(['/static/unnamed1.png', '/static/unnamed.jpg ']))
