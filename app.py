from flask import Flask
from flask import render_template


def create_app():
    _app = Flask(__name__)

    @_app.route('/')
    def landing_page():
        print('Rendering page')
        return render_template('home.html')

    return _app


if __name__ == '__main__':
    app = create_app()
    app.run(extra_files=['static/sketch.js'])
