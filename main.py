import asyncio
import logging

from tornado.web import Application, RequestHandler, StaticFileHandler

from common.locales import t
from common.config import getConfig
from controller import systemController
from service.system import onStartService


class MainIndex(RequestHandler):
    def get(self):
        self.render("front/index.html")


def make_app():
    return Application([
        (r"/svr/noAuth/login", systemController.Login),
        (r"/svr/user", systemController.User),
        (r"/svr/users/export", systemController.UsersExport),
        (r"/svr/users", systemController.Users),
        (r"/", MainIndex),
        (r"/(.*)", StaticFileHandler, {"path": "front"})
    ], cookie_secret=server['key'])


async def main():
    app = make_app()
    logger = logging.getLogger()
    app.listen(server['port'])
    runUrl = f"http://127.0.0.1:{server['port']}/"
    logger.critical(t('system.running_success').format(url=runUrl))
    await asyncio.Event().wait()


if __name__ == "__main__":
    cfg = getConfig()
    try:
        onStartService.init()
    except Exception as e:
        print(e, flush=True)
    else:
        # 后端配置
        server = cfg['server']
        asyncio.run(main())
