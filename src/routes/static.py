from aiohttp import web

routes = web.RouteTableDef()


@routes.static('/static/scripts/{script}')
async def get_script(request: web.Request):
    """Роут для загрузки скриптов"""
