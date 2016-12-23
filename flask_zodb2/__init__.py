from typing import Any

import ZODB
from ZODB.Connection import Connection
from flask import current_app
from flask import g
from transaction import TransactionManager

from flask_zodb2.exceptions import FlaskAppNotFound

__all__ = ['Zodb']


class Zodb:
    def __init__(self, app=None):
        super().__init__()

        if app is not None:
            self.init_app(app)

    def init_app(self, app) -> None:
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['zodb2'] = _ZodbState()

        @app.teardown_request
        def teardown_request(exc):
            self._state.close()
            return exc

    def commit(self) -> None:
        return self._state.commit()

    @property
    def root(self) -> Any:
        return self._state.root

    @property
    def _state(self) -> '_ZodbState':
        if not current_app:
            raise FlaskAppNotFound()

        state = getattr(current_app, 'extensions', {}).get('zodb2')
        if not state:
            raise FlaskAppNotFound()
        return state


class _ZodbState:
    def __init__(self):
        self.db = ZODB.DB(None)

    def commit(self):
        self._global.tm.commit()

    @property
    def root(self) -> Any:
        return self._global.connection.root

    @property
    def _global(self) -> '_ZodbGlobal':
        if not hasattr(g, '_zodb2'):
            g._zodb2 = _ZodbGlobal(self.db)
        return g._zodb2

    def close(self):
        self._global.connection.close()


class _ZodbGlobal:
    def __init__(self, db: ZODB.DB):
        self.tm = TransactionManager()
        self.connection = db.open(transaction_manager=self.tm)  # type: Connection
