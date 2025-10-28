import json
import logging

from common import commonService
from common.locales import t
from common.config import getConfig
from common.ecp import Ecp
from service.system import userService

cfg = getConfig()
cookieName = cfg['server']['cookie_name']


def checkSelf(self):
    cUser = json.loads(self.get_signed_cookie(cookieName))
    lang = self.request.headers.get("Accept-Language", None)
    trueUser = userService.getUser(cUser['id'], lang=lang)
    if ('passwd' not in cUser
            or 'role' not in cUser
            or trueUser['passwd'] != cUser['passwd']
            or trueUser['role'] != cUser['role']):
        msg = commonService.result_map(t('login.expired', lang), 401)
        self.clear_cookie(cookieName)
        self.write(msg)
        return False
    return trueUser


def handle_request(func):
    def wrapper(self):
        uri = self.request.uri
        lang = self.request.headers.get("Accept-Language", None)
        user = self.get_signed_cookie(cookieName)
        if not uri.startswith('/svr/noAuth') and user is None:
            self.clear_cookie(cookieName)
            msg = commonService.result_map(t('login.no_login', lang), 401)
        else:
            try:
                req = commonService.get_post_data(self)
                if not uri.startswith('/svr/noAuth') and user:
                    trueUser = checkSelf(self)
                    if trueUser is False:
                        return
                    req['__user'] = trueUser.copy()
                    del req['__user']['passwd']
                req['__lang'] = lang
                msg = commonService.result_map(func(self, req))
            except Ecp as e:
                msg = commonService.result_map(e)
                logger = logging.getLogger()
                logger.exception(e)
            except Exception as e:
                msg = commonService.result_map(str(e), 500)
                logger = logging.getLogger()
                logger.exception(e)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(msg)

    return wrapper


def handle_export(func):
    def wrapper(self):
        lang = self.request.headers.get("Accept-Language", None)
        trueUser = checkSelf(self)
        if trueUser is False:
            return
        req = commonService.get_post_data(self)
        req['__user'] = trueUser.copy()
        del req['__user']['passwd']
        req['__lang'] = lang
        try:
            output = func(self, req)
            self.set_header('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            self.set_header('Content-Disposition', 'attachment; filename="export.xlsx"')
            self.write(output)
            return
        except Ecp as e:
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            msg = commonService.result_map(e)
            logger = logging.getLogger()
            logger.exception(e)
        except Exception as e:
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            msg = commonService.result_map(str(e), 500)
            logger = logging.getLogger()
            logger.exception(e)
        self.write(msg)

    return wrapper
