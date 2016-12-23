from flask import Flask

from flask_zodb2 import Zodb


def test_root():
    app = Flask(__name__)
    db = Zodb(app)
    with app.app_context():
        db.root.life = 42
        db.commit()
    with app.app_context():
        assert db.root.life == 42


def test_multiple_commit():
    app = Flask(__name__)
    db = Zodb(app)

    with app.app_context():
        db.root.life = 0
        db.commit()
        db.root.life = 42
        db.commit()

    with app.app_context():
        assert db.root.life == 42
