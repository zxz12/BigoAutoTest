# -*- coding: utf-8 -*-
'''
Created on 2021年4月1日

@author: 011305
'''

from dfx.ReadConfig import ReadConfig
from dfx.runner import *

if __name__ == "__main__":
    conf = ReadConfig()
    run_all = conf.get_websocket("run_all", key_type="boolean")
    sen_email = conf.get_email("need_send", key_type="boolean")
    # 执行测试
    if run_all:
        suits = get_case_by_dir()
    else:
        suits = get_case_by_txt()
    starTime = time.strftime("%y%m%d%H%M%S", time.localtime())
    file = 'test result_%s.html' % starTime
    run_case(suits, file=file, title="网关本地测试项目")

    # 邮件发送测试报告
    if sen_email:
        to = conf.get_email("to")
        filepath = os.path.join(CONSTANT.REPORT_PATH, file)
        send_email(to=to, filepath=filepath)
