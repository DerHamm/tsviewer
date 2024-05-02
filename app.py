import random
from tsviewer.ts_viewer_client import TsViewerClient
from flask import Flask, render_template, session, redirect, url_for, request
from functools import wraps
from tsviewer.avatars import Avatars
from tsviewer.user import build_fake_user
from tsviewer.ts_viewer_utils import get_application_name
from tsviewer.configuration import load_configuration, read_config_path_from_environment_variables
from tsviewer.session_interface import TsViewerSecureCookieSessionInterface

def check_password(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        """
        Check if the password supplied by `/login.html` is the user- or the admin password.
        """
        role = session.get('role')
        if role not in ['user', 'admin']:
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    return decorated_function


if __name__ in ['__main__', get_application_name()]:
    client = TsViewerClient(load_configuration(read_config_path_from_environment_variables()))
    avatars = Avatars(client.configuration.teamspeak_install_path)
    # TODO: Add a configuration field for the port of the Flask server
    app = Flask(get_application_name(), template_folder='template')
    app.session_interface = TsViewerSecureCookieSessionInterface(client.configuration.cookie_signing_salt)
    app.secret_key = client.configuration.cookie_secret_key


    @app.route("/", methods=['GET', 'POST'])
    @check_password
    def index():
        users = [build_fake_user()] * 10  # client.get_user_list()
        # avatars.update_avatars(users)

        # multiply users times 10 for testing purposes
        return render_template('index.html', users=users, avatars=avatars,
                               random_image=lambda: random.choice(['/static/unnamed1.png', '/static/unnamed.jpg ']),
                               is_admin=session.get('role') == 'admin')

    @app.route('/logout', methods=['POST'])
    def logout():
        session['role'] = None
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            password = request.form.get('password', str())
            if password not in [client.configuration.website_password, client.configuration.admin_password]:
                return redirect(request.url)
            role = {client.configuration.website_password: 'user',
                    client.configuration.admin_password: 'admin'}.get(password)
            session['role'] = role
            return redirect(url_for('index'))
        if session.get('role') is not None:
            return redirect(url_for('index'))
        return render_template('login.html')
