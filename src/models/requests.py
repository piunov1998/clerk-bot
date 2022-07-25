import dataclasses as dc
import enum
import typing as t
from datetime import datetime

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import JSONB

from .orm import BaseOrm


class RequestStatus(enum.auto):
    accepted = 'принята'
    pending = 'в обработке'
    in_write = 'не подана'


class RequestDataValidator(BaseModel):
    """Параметры заявки"""

    firstname: str | None
    lastname: str | None
    middlename: str | None
    religion: str | None
    nation: str | None
    wonder_nick: str | None
    wonder_role: int | None
    sex: t.Literal['male', 'female']
    birth_date: int | None


class RequestData(t.TypedDict):
    """Параметры заявки"""

    firstname: str | None
    lastname: str | None
    middlename: str | None
    religion: str | None
    nation: str | None
    wonder_nick: str | None
    wonder_role: int | None
    sex: t.Literal['male', 'female']
    birth_date: int | None


@dc.dataclass
class User(BaseOrm):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'userdata'}

    id: int = dc.field(metadata={
        'sa': sa.Column(sa.BIGINT, primary_key=True, unique=True)
    })

    nickname: t.Optional[str] = dc.field(default=None, metadata={
        'sa': sa.Column(sa.VARCHAR(256), unique=True)
    })

    login: t.Optional[str] = dc.field(default=None, metadata={
        'sa': sa.Column(sa.VARCHAR(128), unique=True)
    })

    password: t.Optional[str] = dc.field(default=None, metadata={
        'sa': sa.Column(sa.VARCHAR(256))
    })


@dc.dataclass
class Request(BaseOrm):
    __tablename__ = 'requests'
    __table_args__ = {'schema': 'userdata'}

    user: int = dc.field(metadata={
        'sa': sa.Column(
            sa.BIGINT, sa.ForeignKey(
                'userdata.users.id', onupdate='CASCADE', ondelete='CASCADE'))
    })

    data: t.Optional[RequestData] = dc.field(default=None, metadata={
        'sa': sa.Column(JSONB)
    })

    date: datetime = dc.field(default_factory=datetime, metadata={
        'sa': sa.Column(sa.TIMESTAMP)
    })

    sign_date: t.Optional[datetime] = dc.field(default=None, metadata={
        'sa': sa.Column(sa.TIMESTAMP)
    })

    id: t.Optional[int] = dc.field(default=None, metadata={
        'sa': sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    })


BaseOrm.REGISTRY.mapped(User)
BaseOrm.REGISTRY.mapped(Request)
