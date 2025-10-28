import configparser
import logging
import os

sysConfig = None


def getPasswordStr():
    """
    获取加密字符串
    :return: 加密字符串
    """
    from common.commonUtils import readOrSet, generatePasswd
    if not os.path.exists('data/log'):
        os.makedirs('data/log')
    fileName = 'data/secret.key'
    passwdStr = readOrSet(fileName, generatePasswd(256))
    return passwdStr


def getConfig():
    global sysConfig
    if sysConfig is None:
        passwdStr = getPasswordStr()
        sCfg = {
            # 数据库配置
            'db': {
                # 数据库文件名称sqlLite
                'dbname': 'data/starter.db'
            },
            # 服务器配置
            'server': {
                'is_demo': 0,
                'key': passwdStr,
                'cookie_name': 'bms',
                'cookie_expires_days': 180,
                # 启动端口
                'port': 8023,
                # 日志等级，0-DEBUG，1-INFO，2-WARNING，3-ERROR，4-CRITICAL；数值越大，产生的日志越少，推荐1或2
                'log_level': 1,
                # 控制台日志等级，0-DEBUG，1-INFO，2-WARNING，3-ERROR，4-CRITICAL；数值越大，产生的日志越少，推荐1或2
                'console_level': 2,
                # 日志文件保留时间，单位天。如需保留所有日志请设置为0
                'log_save': 7
            }
        }
        if os.path.exists('data/config.ini'):
            logger = logging.getLogger()
            try:
                cfg = configparser.ConfigParser()
                cfg.read('data/config.ini', encoding='utf-8')
                for k, v in sCfg.items():
                    if k in cfg:
                        for k_2, v_2 in v.items():
                            if k_2 in cfg[k]:
                                try:
                                    v[k_2] = type(sCfg[k][k_2])(cfg[k][k_2])
                                except Exception as e:
                                    logger.error(f"读取配置项{k}.{k_2}失败，将使用默认值{v[k_2]}，失败原因为：{str(e)}")
                                    logger.exception(e)
            except Exception as e:
                logger.error(f"读取配置文件失败，将使用默认配置，失败原因为：{str(e)}")
                logger.exception(e)
        sysConfig = sCfg
    return sysConfig
