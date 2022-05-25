# -*- coding: utf-8 -*-
'''
Created on 2021年3月18日

@author: 011305
'''
import json, re
from dfx.logger.logging import log


def sort_str(msg):
    '''
    * @Title: str_to_json
    * @Description:字符转排序
    * @parameter:
    * @author: 011305
    * @date 2021年3月24日 下午5:24:29
    '''
    # 响应体排序并去除空格
    # log.info("字符串排序：")
    msg=msg.replace("true", 'True')
    msg=msg.replace("false", 'False')    
    # msg=msg.replace("\\n", '')
    msg_json=eval(msg)
    # print(msg_json)
    # json转换成字符串并排序
    data=json.dumps(msg_json, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    data=data.replace("True", 'true')
    data=data.replace("False", 'false')
    # data=data.replace("\\n", '')
    # print(data)
    log.info("排序后的文本：\n"+data)
    return data


def reg_msg(reg, msg):
    '''
    * @Title: compare_respose
    * @Description:使用正则表达式匹配字符串
    * @parameter:
    * @author: 011305
    * @date 2021年3月24日 下午5:25:02
    '''
    log.info("匹配规则： "+reg)
#     reg = '{"mem_info":{"buffers":[0-9]*,"free":[0-9]*,"shared":[0-9]*,"total":[0-9]*,"used":[0-9]*},"state":{"CPU":[0-9]*,"RAM":[0-9]*,"ROM":[0-9]*,"TF_status":[0-9]*,"app_connection":[(true)|(false),"app_status":[0-9]*,"fw_connection":[(true)|(false),"run_time":[0-9]*}}'
#     log.info(reg)
    result=re.search(reg, msg)
    if result:
        rst=result.group()
        log.info("匹配到结果： "+rst)
    else:
        rst=''
        log.warning("未匹配到结果： "+rst)
    return rst


def get_key(dict_msg, key):
    '''
    * @Title: get_key
    * @Description:获取字典的指定值
    * @parameter:
    * @author: 011305
    * @date 2021年3月24日 下午5:26:52
    '''
    try:
        value=dict_msg[key, ""]
    except Exception as e:
        log.warn(key+"不存在")
    return value
    
