"""
@Author：dr34m
@Date  ：2024/7/30 16:06 
"""
import logging
import os

from common import sqlInit, commonService, locales
from service.system import logJobService


def init():
    # 初始化日志
    if not os.path.exists('data/log'):
        os.makedirs('data/log')
    commonService.setLogger()
    logger = logging.getLogger()
    # 读取语言包
    locales.initLang()
    # 初始化数据库，没有则创建
    sqlInit.init_sql()
    logger.info(locales.t('system.init_sql'))
    logJobService.startJob()
