import random
from tsviewer.ts_viewer_client import TsViewerClient
from flask import Flask
from flask import render_template
from tsviewer.ts_viewer_utils import Avatars
from tsviewer.user import build_fake_user

if __name__:
    client = TsViewerClient(path_to_configuration='config/config.json')
    app = Flask(__name__, template_folder='template')

    @app.route("/")
    def index():
        # users = client.get_user_list()
        users = [build_fake_user()]
        avatars = Avatars(client.configuration.TEAMSPEAK_INSTALL_PATH)
        f = lambda: random.choice(['/static/unnamed1.png', '/static/unnamed.jpg '])
        # mulitply users times 10 for testing purposes
        users *= 10
        return render_template('index.html', users=users, avatars=avatars, f=f)
