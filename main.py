# -*- coding:utf-8 -*-
import unittest
from webtest.common.files.excel import *
from webtest.common.gateway.gateway_fun import gateway_fun
from webtest.aw.CONSTANT import CONSTANT


class yu_data_point_conf_testcase003(unittest.TestCase):
    """
    执行全部的gateway部分sheet页：gateway 6
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_step1(self):

        # # 测试环境
        # user = 'xianzhi'
        # pwd = '123456'
        # api_base_url = CONSTANT.BASE_URL_API
        # gate_api_base_url = CONSTANT.GATE_BASE_URL_API
        # iot_url = CONSTANT.IOT_URL
        # gate_url = CONSTANT.GATE_URL
        # xls_dir = '数据采集配置表测试'

        # 正式环境
        user='ytot'
        pwd='admin123'
        api_base_url=CONSTANT.BASE_URL_YUN_API
        gate_api_base_url = CONSTANT.GATE_BASE_URL_YUN_API
        iot_url = CONSTANT.IOT_URL_YUN
        gate_url=CONSTANT.GATE_URL_YUN
        xls_dir='testcase003'

        # 添加数采配置step1:逻辑设备配置
        gate_ui = gateway_fun()
        gate_ui.login(gate_url, user, pwd)
        gate_ui.enter_data_conf('5楼网关01数据采集配置')
        n=gate_ui.get_pages()
        print(n)
        gate_ui.next_page()