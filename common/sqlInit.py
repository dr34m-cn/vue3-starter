from common import sqlBase, commonUtils


@sqlBase.connect_sql
def init_sql(conn):
    cuVersion = 251027
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE name='settings'")
    fec = cursor.fetchone()
    if fec is None:
        cursor.execute("create table settings("
                       "id integer primary key autoincrement,"
                       "keyName text,"                  # 配置项关键字
                       "keyValue text,"                 # 配置项值
                       "createTime integer DEFAULT (strftime('%s', 'now'))"
                       ")")
        cursor.execute("insert into settings (keyName, keyValue) values (?, ?)", ('cuVersion', cuVersion))
        cursor.execute("create table user("
                       "id integer primary key autoincrement,"
                       "username text,"                 # 用户名
                       "name text,"                     # 姓名
                       "passwd text,"                   # 密码
                       "enable integer DEFAULT 1,"      # 是否启用
                       "role integer DEFAULT 1,"        # 角色，0-超级管理员，1-用户，2-管理员
                       "createTime integer DEFAULT (strftime('%s', 'now'))"
                       ")")
        users = [{
            'username': 'admin',
            'name': 'admin',
            'passwd': commonUtils.passwd2md5('admin123'),
            'role': 0
        }, {
            'username': 'user',
            'name': 'user',
            'passwd': commonUtils.passwd2md5('123456'),
            'role': 1
        }]
        cursor.executemany("insert into user (username, name, passwd, role) "
                           "values (:username, :name, :passwd, :role)", users)
        conn.commit()
    else:
        cursor.execute("select keyValue from settings where keyName='cuVersion'")
        sqlVersion = int(cursor.fetchone()[0])
        if sqlVersion < cuVersion:
            if sqlVersion < 251027:
                pass
            cursor.execute(f"update settings set keyValue={cuVersion} where keyName='cuVersion'")
            conn.commit()
    cursor.close()
