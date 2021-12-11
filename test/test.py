from flask import Flask
import os


app = Flask(__name__, static_url_path='/static', static_folder='./static')

if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))
    print(app.config)
    print(basedir)