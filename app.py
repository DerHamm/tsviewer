# Ensure proper logging by always importing logger.py first in app.py
from tsviewer.logger import logger
import random
import typing
from uuid import uuid4

from flask import Flask, render_template, session, redirect, url_for, request, Response, make_response
from functools import wraps

from tsviewer.channel_uploads import ChannelUploads
from tsviewer.user import User
from tsviewer.ts_viewer_client import TsViewerClient
from tsviewer.user import build_fake_user
from tsviewer.ts_viewer_utils import get_application_name, is_admin, is_authenticated
from tsviewer.configuration import Configuration
from tsviewer.session_interface import TsViewerSecureCookieSessionInterface
from tsviewer.ts_file import File

configuration = Configuration.get_instance()

DISABLE_USER_PASSWORD = configuration.disable_user_password_protection
DISABLE_ADMIN_PASSWORD = configuration.disable_admin_password_protection


def get_user_list(ts_client: TsViewerClient) -> list[User]:
    if ts_client.connection is None or configuration.debug:
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
    client = TsViewerClient()
    uploads = ChannelUploads(client)
    client.uploads = uploads
    if configuration.clean_up_upload_channel:
        def execute_clean_up() -> None:
            uploads.clean_up()
            uploads.download_avatars_to_static_folder()

        from threading import Thread

        thread = Thread(target=execute_clean_up)
        logger.info('clean_up_upload_channel is set to True. The cleanup process will now be executed.')
        thread.start()

    # TODO: Add a configuration field for the port of the Flask server (must be done with the flask command, so the port
    # TODO: should probably be in the dockerfile

    app = Flask(get_application_name(), template_folder='template')

    logger.info('Flask application setup and running')
    app.session_interface = TsViewerSecureCookieSessionInterface(configuration.cookie_signing_salt)
    app.secret_key = configuration.cookie_secret_key


    @app.route("/", methods=['GET', 'POST'])
    @check_password
    def index():
        users = get_user_list(client)
        # avatars.update_avatars(users)

        # multiply users times 10 for testing purposes
        return render_template('index.html', users=users,
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


    @app.route('/files', methods=['GET'])
    @check_password
    def files():
        uploaded_files = uploads.get_files()
        file_list = list()
        for uploaded_file in uploaded_files[0]:
            file_list.append(File(**uploaded_file))
        return render_template('files.html', files=file_list)


    @app.route('/kick_from_server/<client_id>', methods=['GET'])
    @check_password
    def kick_from_server(client_id: str):
        # TODO: The site should refresh after a kick or the kicked user should be removed from DOM
        try:
            client.connection.clientkick(reasonid=5, reasonmsg='Go away', clid=client_id)
        except Exception as error:
            logger.error(error)
        response = make_response('User kicked!')
        response.status_code = 200
        response.headers['Content-Type'] = 'text/plain'
        return response
