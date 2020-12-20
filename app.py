import uuid
import datetime
import hashlib

from flask import Flask, request, make_response, jsonify
from flask import render_template

# dummy db for users
db = {
    'admin@admin.com': {
        'hashed_password': hashlib.md5(b'admin').hexdigest(),
        'token': None,
        'auth_at': None
    }
}


def create_app():
    _app = Flask(__name__)

    @_app.route('/')
    def landing_page():
        print('Rendering page')
        return render_template('home.html')

    @_app.route('/sign_in.html')
    def sign_in_page():
        print('signing in')
        return render_template('sign_in.html')

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
            assert db[email]['hashed_password'] == hashed_password
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
        db[email]['token'] = session_token
        db[email]['auth_at'] = utc_now

        res = make_response(jsonify({
            'token': session_token,
            'message': 'OK',
        }), 200)
        return res

    @_app.route("/load_game", methods=['GET'])
    def load_game():
        print('loading game')
        return render_template('load_game.html')

    return _app


if __name__ == '__main__':
    app = create_app()
    app.run()
