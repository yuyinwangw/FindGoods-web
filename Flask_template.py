import os
# from flask import Flask, request, jsonify, render_template, url_for, redirect
from app.models import Item, Plform
from app import create_app, db


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Item=Item, Plform=Plform)


# @app.cli.command()
# def test():
#     """Run the unit tests."""
#     import unittest
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

