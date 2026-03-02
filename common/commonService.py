import json
import sys

from loguru import logger

from common.config import getConfig
from common.ecp import Ecp


# 日志规定
def setLogger():
    cfg = getConfig()
    logSave = cfg['server']['log_save']
    levelList = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    levelInt = cfg['server']['log_level']
    consoleLevelInt = cfg['server']['console_level']
    level = levelList[levelInt]
    consoleLevel = levelList[consoleLevelInt]
    logger.remove()
    logger.add(sys.stdout, level=consoleLevel, format="{time} {level} {message}")
    logger.add("data/log/sys_{time:YYYY-MM-DD}.log", rotation="00:00",
               retention=f"{logSave} days" if logSave != 0 else None,
               level=level, encoding="utf-8")


def get_post_data(self):
    post_data = self.request.arguments
    post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
    if not post_data:
        post_data = self.request.body.decode('utf-8')
        if post_data and post_data != '':
            post_data = json.loads(post_data)
        else:
            post_data = {}
    return post_data


def result_map(*dt):
    # code：200-成功，500-失败
    # 成功 ResultMap() or ResultMap(data) or ResultMap(msg, 200)
    # 失败 ResultMap(msg, 500)
    lenDt = len(dt)
    if lenDt == 1 and type(dt[0]) == Ecp:
        result = {
            "code": dt[0].code,
            "msg": dt[0].message
        }
    else:
        data = dt[0] if lenDt == 1 else None
        result = {
            "code": 200 if lenDt <= 1 else dt[1],
            "msg": "操作成功" if lenDt <= 1 else dt[0]
        }
        if data is not None:
            result['data'] = data

    return json.dumps(result, ensure_ascii=False)
