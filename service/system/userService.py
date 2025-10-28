import time
from datetime import datetime

from common import commonUtils
from common.locales import t
from mapper import userMapper


def getUser(userId, userName=None, raiseFail=True, lang=None):
    """
    通过用户名获取用户信息
    :param userId: 用户id
    :param userName: 用户名
    :param raiseFail: 用户不存在则抛出异常
    :param lang: 语言
    :return: 用户信息
    """
    user = userMapper.getUserByName(userName) if not userId else userMapper.getUserById(userId)
    if user:
        if user['enable'] == 0:
            raise Exception(t('permission.not_enabled', lang))
    else:
        if raiseFail:
            raise Exception(t('login.user_not_found', lang))
    return user


def getUserList(req):
    """
    超级管理员查看用户列表
    :param req:
    :return:
    """
    commonUtils.onlySuperAdmin(req)
    del req['__user']
    return userMapper.getUserList(req)


def exportUserList(req):
    if 'pageNum' in req:
        del req['pageNum']
    if 'pageSize' in req:
        del req['pageSize']
    users = getUserList(req)
    lang = req['__lang']
    if not users:
        raise Exception(t('system.empty_export', lang))
    roleList = [t('users.superAdmin', lang), t('users.user', lang), t('users.admin', lang)]
    for user in users:
        user[t('users.id', lang)] = user['id']
        del user['id']
        user[t('users.username', lang)] = user['username']
        del user['username']
        user[t('users.name', lang)] = user['name']
        del user['name']
        user[t('users.isEnabled', lang)] = t('users.enable', lang) if user['enable'] == 1 else t('users.disable', lang)
        del user['enable']
        user[t('users.role', lang)] = roleList[user['role']]
        del user['role']
        user[t('users.createTime', lang)] = datetime.fromtimestamp(user['createTime']).strftime("%Y-%m-%d %H:%M:%S")
        del user['createTime']
    return commonUtils.exportToExcel(users)


def updateUserByAdmin(req):
    """
    超级管理员更新用户
    :param req:
    :return:
    """
    commonUtils.onlySuperAdmin(req)
    del req['__user']
    if req['role'] == 0 or req['role'] == '0':
        raise Exception(t('permission.cant_add_super_admin', req['__lang']))
    user = userMapper.getUserById(req['id'])
    if user['role'] == 0:
        raise Exception(t('permission.cant_edit_super_admin', req['__lang']))
    if 'site' not in req:
        req['site'] = None
    userMapper.updateUserByAdmin(req)


def resetPwdByAdmin(req):
    """
    超级管理员重置密码
    :param req:
    :return:
    """
    commonUtils.onlySuperAdmin(req)
    del req['__user']
    user = userMapper.getUserById(req['userId'])
    if user['role'] == 0:
        raise Exception(t('permission.cant_edit_super_admin', req['__lang']))
    userMapper.resetPasswd(req['userId'], commonUtils.passwd2md5(req['passwd']))


def addUser(username, name, passwd, lang=None):
    """
    用户注册
    :param username:
    :param name:
    :param passwd:
    :param lang:
    :return:
    """
    username = username.strip()
    user = userMapper.getUserByName(username)
    if user:
        raise Exception(t('login.username_exists', lang))
    userId = userMapper.addUser({
        "username": username,
        'name': name.strip(),
        'passwd': commonUtils.passwd2md5(passwd)
    }, lang)
    return {
        'id': userId,
        'username': username,
        'name': name,
        'enable': 0,
        'role': 1,
        'createTime': int(time.time())
    }


def updateUser(req):
    """
    用户信息修改
    :param req:
    :return:
    """
    user = req['__user']
    username = req['username'].strip()
    name = req['name'].strip()
    users = userMapper.getOtherUsername(username, user['id'])
    if users:
        raise Exception(t('login.username_exists', req['__lang']))
    userMapper.updateUser({
        'id': user['id'],
        'username': username,
        'name': name
    })
    user['username'] = username
    user['name'] = name
    return user


def checkPwd(userId, passwd, userName=None, lang=None):
    """
    检查密码是否正确
    :param userId: 用户id
    :param passwd: 密码
    :param userName: 用户名
    :param lang:
    :return: 用户信息
    """
    user = getUser(userId, userName, lang=lang)
    if commonUtils.passwd2md5(passwd) == user['passwd']:
        return user
    else:
        raise Exception(t('login.passwd_wrong', lang))


def resetPasswd(userId, passwd, oldPasswd, lang=None):
    """
    重置密码
    :param userId: 用户id
    :param passwd: 新密码
    :param oldPasswd: 旧密码
    :param lang:
    """
    checkPwd(userId, oldPasswd, lang)
    userMapper.resetPasswd(userId, commonUtils.passwd2md5(passwd))
