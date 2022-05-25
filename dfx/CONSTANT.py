# _*_coding:utf-8 _*_
'''
Created on 2021年3月18日

@author: 011305
'''
import os


class CONSTANT:
    # 项目相关路径
    ROOT_PATH=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    AW_PATH=os.path.join(ROOT_PATH, 'aw')
    RES_PATH=os.path.join(ROOT_PATH, 'res')
    REPORT_PATH=os.path.join(ROOT_PATH, 'report')
    SCRIPT_PATH=os.path.join(ROOT_PATH, 'scripts')

    # 驱动路径
    # CHROME_DRIVER_PATH = r'D:\dev\pycharm_space\gateway\res\chromedriver.exe'
    CHROME_DRIVER_PATH = os.path.join(RES_PATH, 'chromedriver.exe')

