from aiohttp import web
from discord.ext.commands import Bot

from injectors import ActivitiesInj
from formatters.json_fmt import json_dumps


routes = web.RouteTableDef()


@routes.get('')
async def main(request: web.Request):
    with open('static/templates/main.html', 'r', encoding='utf-8') as file:
        return web.Response(
            text=file.read(),
            content_type='text/html',
            status=200
        )


@routes.get('/registration/{user_id}')
async def registration(request: web.Request):
    bot: Bot = request.app['bot']
    user_id = request.match_info['user_id']
    try:
        user = bot.get_user(int(user_id))
        if user is None:
            raise TypeError
    except TypeError:
        return web.Response(text='Bad request', status=400)
    with open('static/templates/main.html', 'r', encoding='utf-8') as file:
        return web.Response(
            text=file.read(),
            content_type='text/html',
            status=200
        )


@routes.post('/registration/{user_id}')
async def registration(request: web.Request):
    data = await request.json()
    await ActivitiesInj(
        request.app.get('bot')
    ).registration().registration(data)
    return web.Response(status=201)
