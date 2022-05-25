# _*_coding:utf-8 _*_
'''
Created on 2021年3月18日

@author: 011305
'''

import logging
import os
import sys
import time

from dfx.CONSTANT import CONSTANT

# 日志全局设备
log=logging.getLogger()
log.setLevel(logging.DEBUG)
fomater=logging.Formatter('%(asctime)s-%(levelname)s: %(message)s')

# 设备控制台打印
_handler=logging.StreamHandler(sys.stdout)
_handler.setFormatter(fomater)
log.addHandler(_handler)

# 设备文件输出打印
execute_time=time.strftime("%y-%m-%d_%H%M%S", time.localtime(time.time()))
name=os.path.basename(sys.argv[0])
f_name="%s_%s_report.log"%(execute_time, name.split(".")[0])
# f_path=os.path.basename(__file__)
path=CONSTANT.REPORT_PATH
if not os.path.exists(CONSTANT.REPORT_PATH):
    os.makedirs(path)
_handler_fh=logging.FileHandler(filename=os.path.join(path, f_name), encoding='utf-8')
_handler_fh.setFormatter(fomater)
log.addHandler(_handler_fh)

#
#
# def debug(msg):
    # log.debug("DEBUG "+str(msg))
    #
    #
# def info(msg):
    # log.info(Fore.GREEN+"INFO "+str(msg)+Style.RESET_ALL)
    #
    #
# def error(msg):
    # log.error(Fore.RED+"ERROR "+str(msg)+Style.RESET_ALL)
    #
    #
# def warn(msg):
    # log.warning(Fore.YELLOW+"WARNING "+str(msg)+Style.RESET_ALL)
    #
    #
# def _print(msg):
    # log.debug(Fore.BLUE+"PRINT "+str(msg)+Style.RESET_ALL)
    #
    #
# def set_level(level):
    # """ 设置log级别
    #
    # :param level: logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR
    # :return:
    # """
    # log.setLevel(level)
    #
    #
# def set_level_to_debug():
    # log.setLevel(logging.DEBUG)
