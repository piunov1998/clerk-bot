import asyncio
import logging

import aiohttp_jinja2
import discord
import jinja2
from aiohttp import web
from discord.ext import commands

from config import config
from injectors import ActivitiesInj, connections
from models import RequestStatus
from routes import api_routes, open_routes


def setup_logging():
    dis_logger = logging.getLogger('discord')
    dis_logger.setLevel(logging.ERROR)

    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s]: %(message)s',
        datefmt='%H:%M:%S'
    )


bot = commands.Bot(
    command_prefix=config.discord.prefix,
    intents=discord.Intents().all()
)
activities_ = ActivitiesInj(bot)


async def run():
    app = web.Application()

    app.add_routes([web.static('/static', 'static')])
    app.add_routes(api_routes)
    app.add_routes(open_routes)

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

    runner = web.AppRunner(app)
    await runner.setup()
    endpoint = web.TCPSite(runner, '0.0.0.0', 5555)
    await endpoint.start()

    app['bot'] = bot

    try:
        await bot.start(config.discord.token)
    except Exception:
        await bot.close()
        raise
    finally:
        await runner.cleanup()


@bot.event
async def on_ready():
    logging.info('Connected')
    connections.init_db()
    logging.info('DB inited')


async def process_dm(message: discord.Message):
    if message.author.bot:
        return
    act = ActivitiesInj(bot)
    request = act.registration().get_request(user_id=message.author.id)
    if request is None:
        act.registration().add_user(message.author.id)
        act.registration().create_request(message.author.id)
        await message.channel.send(
            f'Если хочешь присоединиться к нашей ССР, заполни '
            f'небольшую форму по адресу '
            f'http://{config.host}/registration/{message.author.id}'
        )
    else:
        if request.data and request.sign_date:
            status = RequestStatus.accepted
            ps = '\nПроходите и не мешайтесь.'
        elif request.data and request.sign_date is None:
            status = RequestStatus.pending
            ps = '\nПрисядьте, подождите, скоро вас пригласят.'
        else:
            status = RequestStatus.in_write
            ps = f'\nЗаполните регистрационный бланк по ссылке:\n' \
                 f'http://{config.host}/registration/{message.author.id}'
        response = \
            f'Для вас уже была создана заявка **№{request.id:0>4}**.\n' \
            f'**Статус заявки:** "{status}"{ps}'

        await message.channel.send(response)


@bot.event
async def on_message(message: discord.Message):
    if isinstance(message.channel, discord.DMChannel):
        await process_dm(message)
    else:
        await bot.process_commands(message)


if __name__ == '__main__':
    setup_logging()
    logging.info('Connecting to gateway')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
