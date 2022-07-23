import logging
import asyncio

import discord
from aiohttp import web
from discord.ext import commands

from injectors import ActivitiesInj
from config import config
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
    app.add_routes(api_routes)
    app.add_routes(open_routes)

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


@bot.event
async def on_message(message: discord.Message):
    if isinstance(message.channel, discord.DMChannel):
        if not message.author.bot:
            await message.channel.send('Обожди, скоро все будет')
    else:
        await bot.process_commands(message)


if __name__ == '__main__':
    setup_logging()
    logging.info('Connecting to gateway')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
