"""
@Author：dr34m
@Date  ：2024/4/24 14:07 
"""
import logging
import os
import time

from apscheduler.schedulers.background import BackgroundScheduler

from common.locales import t
from common.commonService import setLogger
from common.config import getConfig

cfg = getConfig()

logSave = cfg['server']['log_save']


def logClearJob():
    saveLogList = []
    dayNow = int(time.time())
    for i in range(logSave):
        dateName = time.strftime('%Y-%m-%d', time.localtime(dayNow))
        saveLogList.append(f'sys_{dateName}.log')
        dayNow -= 60 * 60 * 24
    for file in os.listdir('data/log'):
        if file.endswith('.log') and file not in saveLogList:
            logger = logging.getLogger()
            try:
                os.remove(f'data/log/{file}')
                logger.info(t('log.delete_success').format(file=file))
            except Exception as e:
                logger.error(t('log.delete_fail').format(file=file, error=str(e)))
                logger.error(f"日志文件{file}删除失败，原因为：{str(e)}")
                logger.exception(e)


def logChangeJob():
    setLogger()


def startJob():
    logger = logging.getLogger()
    logger.info(t('log.change_job'))
    startChangeScheduler()
    if logSave > 0:
        logger.info(t('log.clear_job'))
        startClearScheduler()
    else:
        logger.info(t('log.save_all'))


def startClearScheduler():
    logClearJob()
    scheduler = BackgroundScheduler()
    scheduler.add_job(logClearJob, 'cron', hour=0, minute=0, second=10, misfire_grace_time=None)
    scheduler.start()


def startChangeScheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(logChangeJob, 'cron', hour=0, minute=0, second=0, misfire_grace_time=None)
    scheduler.start()
