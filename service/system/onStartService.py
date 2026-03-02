"""
@Author：dr34m
@Date  ：2024/7/30 16:06 
"""
import os

from loguru import logger

from common import sqlInit, commonService, locales


def init():
    # 初始化日志
    if not os.path.exists('data/log'):
        os.makedirs('data/log')
    commonService.setLogger()
    # 读取语言包
    locales.initLang()
    # 初始化数据库，没有则创建
    sqlInit.init_sql()
    logger.info(locales.t('system.init_sql'))
