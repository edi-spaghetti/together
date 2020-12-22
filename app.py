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
from game import Game

app = Flask(__name__)
socketio = SocketIO(app)
login_manager = LoginManager()
game = Game()


def create_app():

    app.secret_key = os.urandom(16)
    print(f'key: {app.secret_key}')

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    @app.route('/')
    def landing_page():
        print('Rendering page')
        try:
            current_user = escape(session['username'])
        except KeyError:
            current_user = None
        return render_template('home.html', user=current_user)

    @app.route('/sign_in.html')
    def sign_in_page():
        print('signing in')
        return render_template('sign_in.html')

    @app.route('/api/register', methods=['POST'])
    def register():
        # req = request.get_json()
        # email = str(req.get('email'))
        # password = str(req.get('password')).encode('utf-8')
        #
        # hp = hashlib.md5()
        # hp.update(password)
        # hashed_password = hp.hexdigest()
        print('pressed register')

    @app.route('/api/sign_in', methods=['POST'])
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

    @app.route("/enter_lobby", methods=['GET'])
    def load_lobby():
        print('loading game lobby')
        return render_template('lobby.html')

    @app.route("/game")
    def play_game():
        global game
        game.add_random_thing()
        # if isinstance(game, Game):
        #     print(f'Game has these things: {game.things}')
        return render_template('game.html')

    @socketio.event
    def add_thrall(data):
        print(f'New Data {data}')
        if isinstance(game, Game):
            game.add_thing(
                data['x'], data['y'], data['size'],
                autonomous=False
            )
            print(f'Game has these things: {game.things}')
            return True

    @socketio.event
    def start_game(data):
        print('got event data ' + str(data))

        if isinstance(game, Game):
            print(f'Game has these things: {game.things}')
        return True

    return socketio, app, login_manager


if __name__ == '__main__':

    socketio_, app_, login_manager_ = create_app()
    login_manager_.init_app(app_)
    print(
        "Running. "
        "Game at http://localhost:5001/game"
        " - (CTRL+C to quit - but it's super slow)"
    )
    socketio_.run(app_, host='0.0.0.0', port=5001)
