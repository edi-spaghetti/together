import os
import uuid
import datetime
import hashlib

from flask import (
    Flask,
    request,
    make_response,
    jsonify,
    session,
    render_template,
)
from flask_socketio import SocketIO
from markupsafe import escape
from flask_login import LoginManager

from dummy_db import db
from user import User


def create_app():

    _app = Flask(__name__)
    socketio = SocketIO(_app)

    _app.secret_key = os.urandom(16)
    print(f'key: {_app.secret_key}')

    login_manager = LoginManager()

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    @_app.route('/')
    def landing_page():
        print('Rendering page')
        try:
            current_user = escape(session['username'])
        except KeyError:
            current_user = None
        return render_template('home.html', user=current_user)

    @_app.route('/sign_in.html')
    def sign_in_page():
        print('signing in')
        return render_template('sign_in.html')

    @_app.route('/api/register', methods=['POST'])
    def register():
        # req = request.get_json()
        # email = str(req.get('email'))
        # password = str(req.get('password')).encode('utf-8')
        #
        # hp = hashlib.md5()
        # hp.update(password)
        # hashed_password = hp.hexdigest()
        print('pressed register')

    @_app.route('/api/sign_in', methods=['POST'])
    def sign_in():

        req = request.get_json()
        email = str(req.get('email'))
        password = str(req.get('password')).encode('utf-8')

        print(f'testing {email} and {password}')

        hp = hashlib.md5()
        hp.update(password)
        hashed_password = hp.hexdigest()

        try:
            assert db['user'][email]['hashed_password'] == hashed_password
        except (KeyError, AssertionError):
            print('Authentication failed')
            res = make_response(jsonify({
                'token': None,
                'message': 'Incorrect email or password',
            }), 200)
            return res

        print('Authentication passed')
        session_token = uuid.uuid4().hex
        utc_now = datetime.datetime.utcnow()
        db['user'][email]['token'] = session_token
        db['user'][email]['auth_at'] = utc_now

        res = make_response(jsonify({
            'token': session_token,
            'message': 'OK',
        }), 200)
        return res

    @_app.route("/enter_lobby", methods=['GET'])
    def load_lobby():
        print('loading game lobby')
        return render_template('lobby.html')

    @socketio.event
    def entered_lobby(data):
        print('got event data ' + str(data))
        return True

    return socketio, _app, login_manager


if __name__ == '__main__':
    try:
        socketio, app, login_manager = create_app()
        login_manager.init_app(app)
        print('Running on http://localhost:5001/ - (Press CTRL+C to quit)')
        socketio.run(app, host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        print('Quitting')
