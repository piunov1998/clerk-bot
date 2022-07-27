import logging

import aiohttp_jinja2
from aiohttp import web
from discord.ext.commands import Bot
from pydantic import ValidationError

from injectors import ActivitiesInj, auth
from models import RequestDataValidator

routes = web.RouteTableDef()
auth = auth()


@routes.get('')
async def main(request: web.Request):
    return web.Response(text='Напиши боту в ЛС для регистрации', status=200)


@routes.get('/registration/{user_id}')
async def registration_page(request: web.Request):
    bot: Bot = request.app['bot']
    user_id = request.match_info['user_id']
    try:
        user = bot.get_user(int(user_id))
        if user is None:
            raise TypeError
    except TypeError:
        return web.Response(text='Bad request', status=400)
    response = aiohttp_jinja2.render_template(
        template_name='registration.html',
        request=request,
        context={}
    )
    return response


@routes.post('/registration/{user_id}')
async def registration(request: web.Request):
    user_id = request.match_info['user_id']
    if user_id.isdigit():
        user_id = int(user_id)
    else:
        return web.Response(text='Not found', status=404)
    data = await request.json()
    logging.info(data)
    try:
        data = RequestDataValidator(**data)
    except ValidationError as e:
        logging.error(e)
        return web.Response(text='Invalid data', status=400)

    act = ActivitiesInj(request.app['bot'])
    await act.registration().registration(user_id, data)
    return web.Response(status=201)


@routes.get('/login')
async def login_page(request: web.Request):
    response = aiohttp_jinja2.render_template(
        template_name='login.html',
        request=request,
        context={}
    )
    return response


@routes.post('/login')
async def authorization(request: web.Request):
    body = await request.json()
    login, passwd = body.get('login'), body.get('password')

    if login is None or passwd is None:
        return web.Response(text='Invalid credentials', status=403)

    act = ActivitiesInj(request.app['bot'])
    user = act.registration().get_user_by_login(login)

    if not user.password == passwd:
        return web.Response(text='Invalid credentials', status=403)

    token = auth.generate_token(login, 0)
    resp = web.Response(
        text='ok',
        status=201,
        headers={'Set-Cookie': f'token=Bearer {token}'}
    )
    return resp


@routes.get('/adminka')
@auth.check_auth
def adminka(request: web.Request):
    """Временная затычка"""

    response = aiohttp_jinja2.render_template(
        template_name='hidden.html',
        request=request,
        context={'username': auth.session.user}
    )
    return response
