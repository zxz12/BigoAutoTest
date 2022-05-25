# -*- coding: utf-8 -*-
'''
Created on 2021年4月13日

@author: 011305
'''
import json
import unittest

from ddt import ddt, data, file_data, unpack

from common.gateway.gate_interface import gate_interface
from dfx.logger.logging import log


@ddt
class testcase005_test_ddt(unittest.TestCase):
    '''
    * @Title:testcase005_test_ddt
    * @Description:测试数据驱动，登录接口
    * @author: 011305
    * @date 2021年4月13日 下午4:34:17
    '''

    @classmethod
    def setUpClass(cls):
        log.info("类预置条件: ") 
        cls.gt_in=gate_interface()

    @classmethod
    def tearDownClass(cls):
        log.info("类收尾: ")
        cls.gt_in.close()
                
    def setUp(self):
        log.info("预置条件: ")
        
    def tearDown(self):
        log.info("收尾: ") 

    @unittest.skip("不执行")
    @data(
        ("case0", "user", '123456', "ok"),
        ("case1", "user", '', "failed"),
        )
    @unpack
    def testName(self, case, usr, pwd, rst):
        log.info("step: 测试登录接口")
        log.info(case)
        cmd='account_access'
        self.gt_in.set_body(key="cmd", value=cmd) 
        self.gt_in.set_body(key="data", sec='user_name', value=usr)
        body=self.gt_in.set_body(key="data", sec='password', value=pwd)
        self.gt_in.send(data=body)
        body_raw=self.gt_in.recv()
        if 'time out' not in body_raw:
            body_dict=json.loads(body_raw)
            result=body_dict["data"]["result"]
        else:
            result=""
        log.info("checkpoint: 检查登陆成功")
        print(result)
        self.assertEqual(result, rst, msg="测试结果不为%s"%rst)

    @file_data('../../res/testcase005_test_ddt.json')   
    def testName1(self, usr, pwd, rst):
        log.info("step: 测试登录接口")
        cmd='account_access'
        self.gt_in.set_body(key="cmd", value=cmd) 
        self.gt_in.set_body(key="data", sec='user_name', value=usr)
        body=self.gt_in.set_body(key="data", sec='password', value=pwd)
        self.gt_in.send(data=body)
        body_raw=self.gt_in.recv()
        if 'time out' not in body_raw:
            body_dict=json.loads(body_raw)
            result=body_dict["data"]["result"]
        else:
            result=""
        log.info("checkpoint: 检查登陆成功")
        print(result)
        self.assertEqual(result, rst, msg="测试结果不为%s"%rst)
