import json
from concurrent.futures import ThreadPoolExecutor

from tornado.concurrent import run_on_executor
from tornado.web import RequestHandler

from common.config import getConfig
from controller.baseController import handle_request, cookieName, handle_export
from service.system import userService

cfg = getConfig()


class Login(RequestHandler):
    executor = ThreadPoolExecutor(8)

    @run_on_executor
    @handle_request
    def post(self, req):
        # 登录
        username = req['username'].strip()
        passwd = req['passwd'].strip()
        user = userService.checkPwd(None, passwd, username, req['__lang'])
        self.set_signed_cookie(cookieName, json.dumps(user, ensure_ascii=False),
                               expires_days=int(cfg['server']['cookie_expires_days']))
        userReturn = user.copy()
        del userReturn['passwd']
        return userReturn

    @run_on_executor
    @handle_request
    def delete(self, req):
        # 登出
        self.clear_cookie(cookieName)

    @handle_request
    def put(self, req):
        # 注册
        username = req['username'].strip()
        name = req['name'].strip()
        passwd = req['passwd'].strip()
        user = userService.addUser(username, name, passwd, req['__lang'])
        self.set_signed_cookie(cookieName, json.dumps(user, ensure_ascii=False),
                               expires_days=int(cfg['server']['cookie_expires_days']))
        return user


class User(RequestHandler):
    executor = ThreadPoolExecutor(8)

    @run_on_executor
    @handle_request
    def get(self, req):
        user = req['__user']
        return user

    @run_on_executor
    @handle_request
    def put(self, req):
        passwd = req['passwd'].strip()
        oldPasswd = req['oldPasswd'].strip()
        user = json.loads(self.get_signed_cookie(cookieName))
        userService.resetPasswd(user['id'], passwd, oldPasswd, req['__lang'])

    @run_on_executor
    @handle_request
    def post(self, req):
        return userService.updateUser(req)


class UsersExport(RequestHandler):
    executor = ThreadPoolExecutor(8)

    @run_on_executor
    @handle_export
    def get(self, req):
        return userService.exportUserList(req)



class Users(RequestHandler):
    executor = ThreadPoolExecutor(8)

    @run_on_executor
    @handle_request
    def get(self, req):
        return userService.getUserList(req)

    @run_on_executor
    @handle_request
    def post(self, req):
        userService.updateUserByAdmin(req)

    @run_on_executor
    @handle_request
    def put(self, req):
        userService.resetPwdByAdmin(req)
