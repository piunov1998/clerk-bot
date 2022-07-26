from aiohttp import web

from formatters.json_fmt import json_dumps
from injectors import ActivitiesInj

prefix = '/bot/api'
routes = web.RouteTableDef()


@routes.post(f'{prefix}/announce')
async def announce(request: web.Request):
    msg = request.query.get('msg')
    if msg is None:
        return web.Response(text='Не перередан текст объявления', status=400)
    await ActivitiesInj(request.app.get('bot')).messaging().announce(msg)
    return web.Response(text='ok', status=200)


@routes.get(f'{prefix}/roles')
async def get_roles(request: web.Request):
    roles = ActivitiesInj(request.app.get('bot')).roles().get_roles()
    return web.json_response(data=roles, status=200, dumps=json_dumps)



