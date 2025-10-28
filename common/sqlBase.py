import re
import sqlite3
import time

from common.config import getConfig
from common.locales import t

RUN_FLAG = False
cfg = getConfig()


def connect_sql(func):
    def wrapper(*args, **kwargs):
        global RUN_FLAG
        while RUN_FLAG:
            time.sleep(0.073)
        RUN_FLAG = True
        conn = None
        try:
            conn = sqlite3.connect(cfg['db']['dbname'])
            result = func(conn, *args, **kwargs)
        except Exception as e:
            raise Exception(e)
        finally:
            RUN_FLAG = False
            if conn:
                conn.close()
        return result

    return wrapper


@connect_sql
def fetchall(conn, query, params=()):
    cursor = conn.cursor()
    cursor.execute(query, params)
    rst = cursor.fetchall()
    cursor.close()
    return rst


@connect_sql
def fetch_count(conn, query, params=()):
    cursor = conn.cursor()
    cursor.execute(query, params)
    rst = cursor.fetchall()
    cursor.close()
    if len(rst) == 1:
        return rst[0][0]
    else:
        return len(rst)


@connect_sql
def fetchall_to_table(conn, query, params=()):
    cursor = conn.cursor()
    cursor.execute(query, params)
    rst = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    results = []
    for row in rst:
        results.append(dict(zip(columns, row)))
    return results


def fetchall_to_page(sql, params=None):
    if params is None:
        params = {}
    sql_end = ''
    pageSize = params['pageSize'] if 'pageSize' in params else None
    pageNum = params['pageNum'] if 'pageNum' in params else None
    if pageNum is None or pageSize is None:
        return fetchall_to_table(sql, params)
    else:
        sql_end += ' limit :pageSize offset :offset'
        params['offset'] = (int(pageNum) - 1) * int(pageSize)
    dataList = fetchall_to_table(sql + sql_end, params)
    pattern = r'(SELECT\s+)(?:DISTINCT\s+)?.*?(\s+FROM)'
    replacement = r'\1count(*)\2'
    result = re.sub(pattern, replacement, sql, flags=re.IGNORECASE | re.DOTALL)
    count = fetch_count(result, params)
    return {
        'dataList': dataList,
        'count': count
    }


@connect_sql
def execute_insert(conn, query, params=(), lang=None):
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        lastId = cursor.lastrowid
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise Exception(t('system.same_exists', lang).format(str(e)))
    except Exception as e:
        raise Exception(e)
    finally:
        cursor.close()
    return lastId


@connect_sql
def execute_manny(conn, query, params=()):
    cursor = conn.cursor()
    cursor.executemany(query, params)
    conn.commit()
    cursor.close()


@connect_sql
def execute_update(conn, query, params=()):
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    cursor.close()


def check_and_add_sql(sql, params, data, lang=None):
    """
    检查字段并自动生成sql
    :param sql: 初始sql
    :param params: 参数列表，例如['sort','remark']
    :param data: 入参对象
    :param lang:
    :return 生成的sql
    """
    flag = 0
    for item in params:
        if item in data:
            sql += " {}=:{},".format(item, item)
            flag += 1
    if flag == 0 or 'id' not in data:
        raise Exception(t('system.lost_part', lang))
    sql = sql[:-1]
    sql += " where id=:id"
    return sql
