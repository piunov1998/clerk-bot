import dataclasses as dc
import typing as t

import yaml
from dataclass_factory import Factory


@dc.dataclass
class PGConfig:

    host: str = dc.field()
    port: int = dc.field()
    user: str = dc.field()
    password: str = dc.field()
    database: str = dc.field()


@dc.dataclass
class DiscordServer:

    info_channel: int = dc.field()
    guild_id: int = dc.field()
    admins_ids: t.List[int] = dc.field()


@dc.dataclass
class DiscordConfig:

    token: str = dc.field()
    prefix: str = dc.field()
    server_info: DiscordServer = dc.field()
    locale: t.Literal['ru-RU', 'en_EN'] = dc.field(default='ru-RU')


@dc.dataclass
class Config:

    pg: PGConfig = dc.field()
    discord: DiscordConfig = dc.field()


with open('../config.yaml', 'r') as file:
    yaml_config = yaml.safe_load(file)

factory = Factory()
config = factory.load(yaml_config, Config)
