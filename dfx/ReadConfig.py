# -*- coding: utf-8 -*-
'''
Created on 2021年3月23日

@author: 011305
'''
import configparser
import os

from dfx.CONSTANT import CONSTANT
from dfx.logger.logging import log

configPath=(os.path.join(CONSTANT.ROOT_PATH, "project.ini"))


class ReadConfig:

    def __init__(self):
        self.cf=configparser.ConfigParser()  
        self.cf.read(configPath)
        log.info("配置文件打开ok")
        
    def get_websocket(self, key, key_type=''):
        '''
        * @Title: get_websocket
        * @Description:读取测试配置信息
        * @parameter:
        * @author: 011305
        * @date 2021年4月13日 下午6:25:08
        '''
        if key_type=="int":
            value=self.cf.getint("WEBSOCKET", key)
        elif key_type=="boolean":
            value=self.cf.getboolean("WEBSOCKET", key)
        else: 
            value=self.cf.get("WEBSOCKET", key)
        log.info(key+": "+str(value))
        return value
    
    def get_email(self, key, key_type=''):
        '''
        * @Title: get_email
        * @Description:读取邮件配置信息
        * @parameter:
        * @author: 011305
        * @date 2021年4月13日 下午6:25:08
        '''
        if key_type=="int":
            value=self.cf.getint("EMAIL", key)
        elif key_type=="boolean":
            value=self.cf.getboolean("EMAIL", key)
        else: 
            value=self.cf.get("EMAIL", key)
        log.info(key+": "+str(value))
        return value

        
rf=ReadConfig()
ip=rf.get_websocket(key='ip')
port=rf.get_websocket(key='port', key_type='int')
usr=rf.get_websocket('usr')
pwd=rf.get_websocket('pwd')
