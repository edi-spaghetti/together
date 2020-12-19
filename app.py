import hashlib

from flask import Flask, request
from flask import render_template

# dummy db for users
db = {
    'admin@admin.com': {
        'hashed_password': hashlib.md5(b'admin').hexdigest(),
        'session_token': None
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
        email = str(request.form.get('email'))
        password = str(request.form.get('password')).encode('utf-8')

        # print(f'testing {email} and {password}')
        # print(f'GOT: {request.form}')

        hp = hashlib.md5()
        hp.update(password)
        hashed_password = hp.hexdigest()

        try:
            assert db[email]['hashed_password'] == hashed_password
        except (KeyError, AssertionError):
            print('Authentication failed')
            return render_template('sign_in.html', failure=True, email=email)

        print('Authentication passed')
        return render_template('load_game.html')

    return _app


if __name__ == '__main__':
    app = create_app()
    app.run()
