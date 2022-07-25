import dataclasses as dc

from sqlalchemy.orm import registry


@dc.dataclass
class BaseOrm:

    __tablename__ = ''
    __table_args__ = {'schema': 'public'}
    __sa_dataclass_metadata_key__ = 'sa'

    REGISTRY = registry()
