import requests

from webtest.aw.CONSTANT import CONSTANT
from webtest.logger import logging


class iot_interfance:
    def __init__(self, base_url=CONSTANT.BASE_URL_YUN_API, user='', pwd=''):
        self.base_url = base_url
        body = {"username": user, "password": pwd}
        p = requests.post(url=base_url + CONSTANT.LOGIN_API, headers=CONSTANT.LOGIN_HEADER,
                          json=body)
        # print(p.json())
        if p.status_code == 200:
            token = p.json()['data']['token']
        else:
            raise TypeError('登录失败')
        self.header = {
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': "Bearer " + token
        }

    def get_models(self):
        """
        获取设备类型列表
        :return:设备类型列表
        """
        model = []
        body = {"orders": [{"key": "id", "dir": 0}]}
        p = requests.post(url=self.base_url + CONSTANT.GET_MODEL_LIST, headers=self.header, json=body)
        m_lists = p.json()['data']['list']
        logging.info("设备类型列表如下：")
        for i in range(len(m_lists)):
            model.append(m_lists[i]['modelName'])
            logging.info(m_lists[i]['modelName'])
        logging.info("共： %s 个" % len(model))
        return model

    def get_id_by_model_name(self, model_name):
        """
        根据设备类型名称获取设备类型id
        :param model_name: 设备类型
        :return:设备类型id
        """
        body = {"page": 1, "size": 8, "orders": [{"key": "id", "dir": 0}],
                "cond": {"likes": [{"key": "modelName", "val": model_name}]}}
        p = requests.post(url=self.base_url + CONSTANT.DEVICE_MODEL_LIST_API, headers=self.header, json=body)
        # print(p.json())
        model_id = p.json()['data']['list'][0]['id']
        return model_id

    def add_model(self, model_name, system_type):
        """
        添加设备类型，并返回设备id，若已存在则直接返回id
        :param model_name:设备类型
        :param system_type:所属系统类别
        :return:设备类型id
        """
        system_types = {
            "电系统": 1,
            "水系统": 2,
            "车间监控系统": 3
        }
        systemType = system_types[system_type]
        body = {"modelName": model_name, "systemType": systemType, "modelImg": "", "modelNote": "", "modeNote": ""}
        p = requests.post(url=self.base_url + CONSTANT.ADD_DEVICE_MODEL_API, headers=self.header, json=body)
        logging.info(p.json())
        if '已存在' in p.json()['msg']:
            logging.info("%s 设备类型已存在" % model_name)
        else:
            logging.info("%s 设备类型添加成功" % model_name)
        logging.info("设备类型添加完成")

    def get_devices(self):
        """
        获取设备列表
        :return:设备名称列表
        """
        device_list = []
        body = {"page": 1, "size": 500}
        p = requests.post(url=self.base_url + CONSTANT.GET_DEVICE_LIST, headers=self.header, json=body)
        devices = p.json()['data']['list']
        for d in devices:
            device_list.append(d['instanceName'])
        return device_list

    def get_ins(self, model_name):
        """
        获取指令列表
        :return:设备名称列表
        """
        devTypeId = self.get_id_by_model_name(model_name)
        ins_list = []
        body = {"devTypeId": devTypeId, "page": 1, "size": -1}
        p = requests.post(url=self.base_url + CONSTANT.GET_INS_LIST, headers=self.header, json=body)
        devices = p.json()['data']['list']
        for d in devices:
            ins_list.append(d['insName'])
        return ins_list

    def add_devices(self, model_name, device_name):
        """
        批量添加设备，设备类型若不存在则添加
        :param device_name: 设备名称
        :param model_name: 设备所属类型
        :param device_name: 设备名称
        :return:
        """
        deviceModelID = self.get_id_by_model_name(model_name)
        body = {
            "instanceName": device_name,
            "deviceModelID": deviceModelID,
        }
        r = requests.post(url=self.base_url + CONSTANT.ADD_DEVICE_API, headers=self.header, json=body)
        if r.json()['msg'] != '添加成功':
            logging.error("设备 %s 添加失败" % device_name)
        logging.info("设备添加完成")

    def add_ins(self, deviceModel, insName, ins_Type, insCode, remarks=''):
        """
        添加指令
        :param remarks: 指令备注
        :param deviceModel: 设备类型
        :param insName: 指令名名称
        :param ins_Type: 指令类型
        :param insCode: 指令code码，不重复即可
        :return:
        """
        devTypeId = self.get_id_by_model_name(deviceModel)
        ins_list = self.get_ins(deviceModel)
        if insName not in ins_list:
            INS_TYPE = {"控制": 1, "数据请求": 2, "其他": 3}
            insType = INS_TYPE[ins_Type]
            body = {"devTypeId": devTypeId, "devTypeName": deviceModel, "insCode": insCode, "insName": insName,
                    "insType": insType, "remarks": remarks}
            r = requests.post(url=self.base_url + CONSTANT.INSERT_INS, headers=self.header, json=body)
            if 'SUCCESS' not in r.json()['msg']:
                logging.warn(r.json())

    def add_dict(self, deviceModel, dataName, englishName, dataUnit, data_Type, isShowed=0):
        """
        添加字典
        :param deviceModel: 设备类型
        :param dataName: 数据字典名称
        :param englishName: 英文名称
        :param dataUnit: 数据单元
        :param data_Type: 数据类型
        :param isShowed:是否展示，默认展示
        :return:
        """
        data_ytpes = {'bit': 1, 'byte': 2, 'short': 3, 'ushort': 4, 'ulong': 5, 'long': 6, 'float': 7, 'String': 8}
        dataType = data_ytpes[data_Type.lower()]
        deviceModelID = self.get_id_by_model_name(deviceModel)
        body = {"deviceModelID": deviceModelID, "dataName": dataName, "englishName": englishName, "dataUnit": dataUnit,
                "dataType": dataType, "isShowed": isShowed, "dictionaryNote": "", "parentID": 0, "level": 1}
        r = requests.post(url=self.base_url + CONSTANT.ADD_DICT, headers=self.header, json=body)
        if '已存在' in r.json()['msg']:
            logging.warn(r.json())
        else:
            logging.info(r.json())
