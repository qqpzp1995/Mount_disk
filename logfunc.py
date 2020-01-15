"""
日志模块
"""
import logging
import os
import time
from functools import wraps
from logging.handlers import RotatingFileHandler

from public_data import ProjectPath


def log_print_decorator(func):
    """日志修饰器"""

    @wraps(func)
    def inner(*args, **kwargs):
        log_format = '%(asctime)s-%(levelname)s-[进程ID:%(process)d][线程ID:%(thread)d,%(threadName)s]--%(message)s '
        '''log_format格式:
        %(levelno)s     打印日志级别的数值
        %(levelname)s   打印日志级别名称
        %(pathname)s    打印当前执行程序的路径
        %(filename)s    打印当前执行程序名称
        %(funcName)s    打印日志的当前函数
        %(lineno)d      打印日志的当前行号
        %(asctime)s     打印日志的时间
        %(thread)d      打印线程id
        %(threadName)s  打印线程名称
        %(process)d     打印进程ID
        %(message)s     打印日志信息'''

        # 时间格式
        data_format = '%Y-%m-%d %H:%M:%S'
        # 获取当前日期,作为日志文件名
        cur_time = time.strftime("%Y-%m-%d", time.localtime())
        # 设置第一个handler用于控制台输出日志,用StreamHandler
        handler_1 = logging.StreamHandler()
        # 设置第二个handler用于日志文件输出日志,用RotatingFileHandler
        # RotatingFileHandler可以按照大小自动分割日志文件，一旦达到指定的大小重新生成文件.
        log_dir = os.path.join(ProjectPath.project_path, 'logs')
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        filename = os.path.join(log_dir, "%s.log" % cur_time)
        handler_2 = RotatingFileHandler(filename, encoding='utf-8',
                                        maxBytes=1048576 * 5,  # maxBytes:最大日志文件的大小(Bytes为单位,1048576Bytes=1MB);
                                        backupCount=10)  # backupCount:指定保留的备份文件的个数.
        # 设置日志输出参数
        logging.basicConfig(format=log_format, datefmt=data_format, level=logging.INFO, handlers=[handler_1, handler_2])
        return func(*args, **kwargs)

    return inner


@log_print_decorator
def print_error(content, if_stop=True):
    """打印级别为error的日志,然后(默认)终止程序"""
    logging.error(content)
    if if_stop:
        quit('程序因异常而终止,请处理...')


@log_print_decorator
def print_warning(content):
    """打印级别为warning的日志"""
    logging.warning(content)


@log_print_decorator
def print_log(content):
    """打印级别为info的日志"""
    logging.info(content)


@log_print_decorator
def print_debug(content):
    """打印级别为debug的日志.如果需要显示在日志中,则需要将logging.basicConfig里level的参数设为logging.DEBUG"""
    logging.debug(content)
