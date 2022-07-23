from aiohttp import web

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


@routes.get('/registration')
async def registration(request: web.Request):
    with open('static/templates/main.html', 'r', encoding='utf-8') as file:
        return web.Response(
            text=file.read(),
            content_type='text/html',
            status=200
        )


@routes.post('/registration')
async def registration(request: web.Request):
    data = await request.json()
    await ActivitiesInj(
        request.app.get('bot')
    ).registration().registration(data)
    return web.Response(status=201)
