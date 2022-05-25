# -*- coding: utf-8 -*-
'''
Created on 2021年3月31日
整个工程的入口：执行器
@author: 011305
'''
import os
import re
import sys
import time
import unittest

from dfx.CONSTANT import CONSTANT
from dfx.ReadConfig import ReadConfig
from dfx.TestRunner import HTMLTestRunner, SMTP


def get_case_by_dir(start_dir='./scripts'):
    '''
    * @Title: get_case_by_dir
    * @Description:获取指定文件夹下的用例列表，并加入用例集
    * @parameter:
    * @author: 011305
    * @date 2021年3月31日 下午5:23:37
    '''
    suits=unittest.defaultTestLoader.discover(start_dir=start_dir, pattern='test*.py')
    print(suits)
    return suits


def get_case_by_txt():
    '''
    * @Title: get_case_by_txt
    * @Description:从配置文件获取用例，并加载到执行器
    * @parameter:
    * @author: 011305
    * @date 2021年4月1日 下午4:43:17
    '''
    
    file=os.path.join(CONSTANT.ROOT_PATH, 'project.txt')
    case_list=[]
    with open(file, mode='r') as f:
        cases=f.readlines()
    f.close()
    for c in cases:
        c=c.replace("\n", '')
        case_list.append(c)
        
    scrip_path=CONSTANT.SCRIPT_PATH
    root_path=CONSTANT.ROOT_PATH
    load=unittest.TestLoader()
    suits=unittest.TestSuite()
    files=os.walk(scrip_path)
    for root, dirs, file in files:
        for f in file:
            patt=r'.*.py$'
            r=re.match(patt, f)            
            if r: 
                if r.group() in case_list:
                    fp=os.path.join(root, f).replace(root_path, "")[:-3].replace("\\", ".")[1:]
                    __import__(fp)
                    the_module=sys.modules[fp]
                    case=getattr(the_module, f[:-3])
                    suits.addTests(load.loadTestsFromTestCase(testCaseClass=case))           
    return suits


def run_case(suits, file='', title='', desc=''):
    '''
    * @Title: run_case
    * @Description:执行用例
    * @parameter:
    * @author: 011305
    * @date 2021年4月1日 下午4:43:42
    '''
    is_open=False
    if file:
        filepath=os.path.join(CONSTANT.REPORT_PATH, file)
        fp=open(filepath, "wb")
        is_open=True  
        runner=HTMLTestRunner(stream=fp, title=title, description=desc)
    else:
        runner=unittest.TextTestRunner()
    runner.run(suits)
    if is_open:
        fp.close()


def send_email(to, filepath):
    conf=ReadConfig()
    host=conf.get_email("host")
    port=conf.get_email("port", key_type='int')
    acc=conf.get_email("acc")
    pwd=conf.get_email("pwd")
    time_now=time.strftime("%y%m%d%H%M%S", time.localtime())
    smtp_eml=SMTP(acc, pwd, host, port=port)
    smtp_eml.sender(to=to, subject="自动化测试_%s"%time_now, path=filepath)
