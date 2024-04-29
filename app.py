import random
from tsviewer.ts_viewer_client import TsViewerClient
from flask import Flask, render_template
from tsviewer.avatars import Avatars
from tsviewer.user import build_fake_user, User
from tsviewer.ts_viewer_utils import get_application_name
from tsviewer.configuration import load_configuration, read_config_path_from_environment_variables

FLASK_APPLICATION_NAME = f'{get_application_name()}.app'


if __name__ in ['__main__', FLASK_APPLICATION_NAME]:
    client = TsViewerClient(load_configuration(read_config_path_from_environment_variables()))
    # TODO: Add a configuration field for the port of the Flask server
    app = Flask(FLASK_APPLICATION_NAME, template_folder='template')
    avatars = Avatars(client.configuration.teamspeak_install_path)


    @app.route("/")
    def index():
        # users = client.get_user_list()
        users = [build_fake_user()] * 10

        if users and isinstance(users[0], User):
            # noinspection PyTypeChecker
            avatars.update_avatars(users)

        # multiply users times 10 for testing purposes
        return render_template('index.html', users=users, avatars=avatars,
                               f=lambda: random.choice(['/static/unnamed1.png', '/static/unnamed.jpg ']))
