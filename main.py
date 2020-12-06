from sanic import Sanic
from jinja2_sanic import setup as setup_jinja2
from jinja2 import FileSystemLoader
import aioredis
from sanic_session import Session, AIORedisSessionInterface

from routes import setup_routes
from sio import setup_socketio

app = Sanic(__name__)

# sanic_session initialization
@app.listener('before_server_start')
async def session_init(app, loop):
  app.redis = await aioredis.create_redis_pool('redis://localhost')
  Session().init_app(app, interface=AIORedisSessionInterface(app.redis))


#setup
app.static('/static', './static')
setup_routes(app)
setup_socketio(app)
setup_jinja2(app, loader=FileSystemLoader('templates/'))

#run
if __name__ == '__main__':
  # TODO: 게임서버와 웹서버 분리
  app.run(host='localhost', port=8080)
