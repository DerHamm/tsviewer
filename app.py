import random
from tsviewer.ts_viewer_client import TsViewerClient
from flask import Flask, render_template
from tsviewer.avatars import Avatars
from tsviewer.user import build_fake_user, User
from tsviewer.ts_viewer_utils import get_application_name

FLASK_APPLICATION_NAME = f'{get_application_name()}.app'

if __name__ in ['__main__', FLASK_APPLICATION_NAME]:
    client = TsViewerClient(path_to_configuration='config/config.json')
    app = Flask(FLASK_APPLICATION_NAME, template_folder='template')
    avatars = Avatars(client.configuration.TEAMSPEAK_INSTALL_PATH)

    @app.route("/")
    def index():
        # users = client.get_user_list()
        users = [build_fake_user()] * 10

        if users and isinstance(users[0], User):
            avatars.update_avatars(users)

        # mulitply users times 10 for testing purposes
        return render_template('index.html', users=users, avatars=avatars,
                               f=lambda: random.choice(['/static/unnamed1.png', '/static/unnamed.jpg ']))
