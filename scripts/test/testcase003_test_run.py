# -*- coding: utf-8 -*-
'''
Created on 2021年4月1日

@author: 011305
'''
import unittest

from common.gateway import gateway
from dfx.logger.logging import log


class testcase003_test_run(unittest.TestCase):
    '''
    * @Title:testcase003_test_run
    * @Description:获取测试用例3
    * @author: 011305
    * @date 2021年4月6日 下午4:01:58
    '''

    def setUp(self):
        log.info("预置条件: ") 

    def testName(self):
        log.info("step: 1.对比结果并将结果写回表格")
        gateway.compare_respose(self.filename)
        
        log.info("checkpoint: ")

    def tearDown(self):
        log.info("收尾: ")

