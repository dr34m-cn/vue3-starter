from common import sqlBase
from common.commonUtils import dealWithSearch

# 用户列表，key为{user.id}，value为用户字典
users = {}


def getUserByName(name):
    global users
    for item in users.keys():
        if users[item]['username'] == name:
            return users[item]
    userList = sqlBase.fetchall_to_table("select * from user where username = ?", (name,))
    if userList:
        user = userList[0]
        users[user['id']] = user
        return user
    else:
        return None


def getOtherUsername(username, userId):
    return sqlBase.fetchall_to_table("select * from user where username = ? and id != ?",
                                     (username, userId))


def getUserById(userId):
    userId = int(userId)
    global users
    if userId in users:
        return users[userId]
    userList = sqlBase.fetchall_to_table("select * from user where id = ?", (userId,))
    if userList:
        user = userList[0]
        users[user['id']] = user
        return user
    else:
        return None


def addUser(user, lang=None):
    return sqlBase.execute_insert("insert into user (username, name, passwd, enable) "
                                  "values (:username, :name, :passwd, 0)", user, lang)


def enableUser(userId, enable):
    sqlBase.execute_update("update user set enable = ? where id = ?", (enable, userId))


def getUserList(params):
    dealWithSearch(params)
    return sqlBase.fetchall_to_page(f"select id, username, name, role, enable, createTime from user where id > 0 "
                                    f"{'and (username like :search or name like :search) ' if 'search' in params else ''}"
                                    f"{'and enable=:enable ' if 'enable' in params else ''}",
                                    params)


def updateUserByAdmin(user):
    sqlBase.execute_update("update user set name = :name, username = :username, "
                           "role=:role, enable=:enable where id = :id", user)
    global users
    userId = int(user['id'])
    if userId in users:
        users[userId]['name'] = user['name']
        users[userId]['username'] = user['username']
        users[userId]['role'] = user['role']
        users[userId]['enable'] = user['enable']


def updateUser(user):
    sqlBase.execute_update("update user set name = :name, username = :username where id = :id", user)
    global users
    userId = int(user['id'])
    if userId in users:
        users[userId]['name'] = user['name']
        users[userId]['username'] = user['username']


def resetPasswd(userId, passwd):
    userId = int(userId)
    sqlBase.execute_update("update user set passwd = ? where id = ?", (passwd, userId))
    global users
    if userId in users:
        users[userId]['passwd'] = passwd


def addLog(logItem):
    sqlBase.execute_insert("insert into login_logs (ip, userAgent) values (:ip, :userAgent)", logItem)
