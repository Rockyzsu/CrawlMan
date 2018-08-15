# -*-coding=utf-8-*-
import logging
import datetime
import os
# from setting import llogger
def llogger(filename):

    logger = logging.getLogger(filename)  # 不加名称设置root logger
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    # 使用FileHandler输出到文件
    prefix = os.path.splitext(filename)[0]
    fh = logging.FileHandler(prefix+'.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    # 使用StreamHandler输出到屏幕
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    # 添加两个Handler
    logger.addHandler(ch)
    logger.addHandler(fh)
    # logger.info('this is info message')
    # logger.warning('this is warn message')
    return logger

