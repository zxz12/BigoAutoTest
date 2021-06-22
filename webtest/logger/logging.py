import logging.handlers
import os
import sys
import time

from colorama import Fore, Style

from webtest.aw.CONSTANT import CONSTANT

# 日志全局设备
_logger = logging.getLogger('aw')
_logger.setLevel(logging.DEBUG)
fomater = logging.Formatter('%(asctime)s %(message)s')

# 设备控制台打印
_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(fomater)
_logger.addHandler(_handler)

# 设备文件输出打印
execute_time = time.strftime("%y-%m-%d_%H%M%S", time.localtime(time.time()))
name = os.path.basename(sys.argv[0])
f_name = "%s_%s_report.log" % (execute_time, name.split(".")[0])
# f_path=os.path.basename(__file__)
_handler_fh = logging.FileHandler(filename=os.path.join(CONSTANT.REPORT_PATH, f_name), encoding='utf-8')
_handler_fh.setFormatter(fomater)
_logger.addHandler(_handler_fh)


def debug(msg):
    _logger.debug("DEBUG " + str(msg))


def info(msg):
    _logger.info(Fore.GREEN + "INFO " + str(msg) + Style.RESET_ALL)


def error(msg):
    _logger.error(Fore.RED + "ERROR " + str(msg) + Style.RESET_ALL)


def warn(msg):
    _logger.warning(Fore.YELLOW + "WARNING " + str(msg) + Style.RESET_ALL)


def _print(msg):
    _logger.debug(Fore.BLUE + "PRINT " + str(msg) + Style.RESET_ALL)


def set_level(level):
    """ 设置log级别

    :param level: logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR
    :return:
    """
    _logger.setLevel(level)


def set_level_to_debug():
    _logger.setLevel(logging.DEBUG)


def set_level_to_info():
    _logger.setLevel(logging.INFO)


def set_level_to_warn():
    _logger.setLevel(logging.WARN)


def set_level_to_error():
    _logger.setLevel(logging.ERROR)
