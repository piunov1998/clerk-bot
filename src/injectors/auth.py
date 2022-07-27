import dataclasses as dc
import typing as t
from datetime import datetime, timedelta

import jwt
from aiohttp.web import Request, Response

from formatters.json_fmt import JsonDump


@dc.dataclass
class Session:
    user: str = dc.field()
    user_id: int = dc.field()
    expire: float = dc.field()


class _Auth:

    def __init__(self):
        self._session = None

    @classmethod
    def _not_authorised(cls):
        return Response(text='Not authorised', status=401)

    @property
    def session(self) -> Session:
        return self._session

    def get_session(self, token) -> Session:
        payload = jwt.decode(token, 'zmeelud', algorithms=['HS256'])
        self._session = Session(**payload)
        return self.session

    def check_auth(self, func: t.Callable) -> t.Callable:

        def wrapper(request: Request, *args, **kwargs) -> Response:
            bearer = request.headers.get('Authorization')
            cookie = request.headers.get('Cookie')
            if cookie is not None:
                for obj in cookie.split('; '):
                    if obj.startswith('token='):
                        cookie_bearer = obj[6:]
                        bearer = bearer or cookie_bearer

            if bearer is None or not bearer.startswith('Bearer'):
                return self._not_authorised()
            try:
                _, token = bearer.split(maxsplit=2)
            except ValueError:
                return self._not_authorised()
            try:
                session = self.get_session(token)
                if datetime.fromtimestamp(session.expire) <= datetime.now():
                    return Response(text='Expired session', status=440)
            except Exception as e:
                resp = Response(text=type(e).__name__, status=500)
            else:
                resp = func(request, *args, **kwargs)
            finally:
                self._session = None

            return resp

        return wrapper

    @classmethod
    def generate_token(cls, user: str, user_id: int) -> str:
        payload = dict(
            user=user,
            user_id=user_id,
            expire=(
                    datetime.now() + timedelta(days=1)
            ).timestamp()
        )
        return jwt.encode(
            payload=payload,
            key='zmeelud',
            algorithm='HS256',
            json_encoder=JsonDump
        )


def auth() -> _Auth:
    return _Auth()
