import random
import typing
from uuid import uuid4

from flask import Flask, render_template, session, redirect, url_for, request, Response
from functools import wraps

from tsviewer.channel_uploads import ChannelUploads
from tsviewer.user import User
from tsviewer.ts_viewer_client import TsViewerClient
from tsviewer.avatars import Avatars
from tsviewer.user import build_fake_user
from tsviewer.ts_viewer_utils import get_application_name, is_admin, is_authenticated
from tsviewer.configuration import Configuration
from tsviewer.session_interface import TsViewerSecureCookieSessionInterface

DISABLE_USER_PASSWORD = False
DISABLE_ADMIN_PASSWORD = False

DEBUG = True


def get_user_list(ts_client: TsViewerClient) -> list[User]:
    if ts_client.connection is None or DEBUG:
        users = [build_fake_user() for _ in range(10)]
    else:
        users = ts_client.get_user_list()
    return users


def redirect_to_index() -> Response:
    return redirect(url_for('index'))


def redirect_to_login() -> Response:
    return redirect(url_for('login'))


def check_password(func) -> typing.Callable:
    @wraps(func)
    def decorated_function(*args, **kwargs) -> typing.Any:
        """
        Check if the password supplied by `/login.html` is the user- or the admin password.
        """
        if DISABLE_USER_PASSWORD or DISABLE_ADMIN_PASSWORD:
            session['role'] = 'admin' if DISABLE_ADMIN_PASSWORD else 'user'
            session['uid'] = str(uuid4())
        if not is_authenticated(session):
            return redirect_to_login()
        return func(*args, **kwargs)

    return decorated_function


if __name__ in ['__main__', get_application_name()]:

    configuration = Configuration.get_instance()
    DISABLE_USER_PASSWORD = configuration.disable_user_password_protection
    DISABLE_ADMIN_PASSWORD = configuration.disable_admin_password_protection

    client = TsViewerClient(configuration=configuration)

    avatars = Avatars(configuration.teamspeak_install_path, server_id=str(configuration.server_id))

    # TODO: Add a configuration field for the port of the Flask server (must be done with the flask command, so the port
    # TODO: should probably be in the dockerfile
    app = Flask(get_application_name(), template_folder='template')
    app.session_interface = TsViewerSecureCookieSessionInterface(configuration.cookie_signing_salt)
    app.secret_key = configuration.cookie_secret_key


    @app.route("/", methods=['GET', 'POST'])
    @check_password
    def index():
        users = get_user_list(client)
        # avatars.update_avatars(users)

        # multiply users times 10 for testing purposes
        return render_template('index.html', users=users, avatars=avatars,
                               random_image=lambda: random.choice(['/static/unnamed1.png', '/static/unnamed.jpg ']),
                               is_admin=is_admin(session))


    @app.route('/logout', methods=['POST'])
    def logout():
        session.clear()
        return redirect_to_login()


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            password = request.form.get('password', str())
            if password not in [configuration.website_password, configuration.admin_password]:
                return redirect(request.url)
            role = {configuration.website_password: 'user',
                    configuration.admin_password: 'admin'}.get(password)
            session['role'] = role
            session['uid'] = str(uuid4())
            return redirect_to_index()
        if is_authenticated(session):
            return redirect_to_index()
        return render_template('login.html')
