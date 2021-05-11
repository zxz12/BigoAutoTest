import requests

from webtest.logger import logging
from webtest.aw.CONSTANT import CONSTANT


class gateway_interfance:
    def __init__(self, base_url=CONSTANT.GATE_BASE_URL_YUN_API, user='', pwd=''):
        """
        初始化接口，登录获取token
        :param base_url:接口基础地址
        :param user:用户名
        :param pwd:密码
        """
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

    def get_data_conf_names(self, user):
        """
        获取系统中当前用户已有的数采名称
        :param user:
        :return:系统中已经存在的数据采集名称列表
        """
        users = {'xianzhi': 119, 'ytot': 9}
        roleID = users[user]
        get_data_conf_names = []
        body = {"page": 1, "size": 500, "roleID": roleID}
        p = requests.post(url=self.base_url + CONSTANT.GATE_GET_DATA_CONF_LIST, headers=self.header, json=body)
        if p.json()['data']:
            m_lists = p.json()['data']['list']
            # logging.info(m_lists)
            for i in range(len(m_lists)):
                get_data_conf_names.append(m_lists[i]['dataConfigName'])
                logging.info(m_lists[i]['dataConfigName'])
            logging.info("共： %s 个" % len(get_data_conf_names))
        return get_data_conf_names

    def get_data_conf_uuid(self, user, dataConfigName):
        """
        通过数采名称获取数次uuid
        :param user:
        :param dataConfigName:
        :return:数采对应的uuid
        """
        users = {'xianzhi': 119, 'ytot': 9}
        roleID = users[user]
        body = {"page": 1, "size": 500, "roleID": roleID}
        p = requests.post(url=self.base_url + CONSTANT.GATE_GET_DATA_CONF_LIST, headers=self.header, json=body)
        if p.json()['data']:
            m_lists = p.json()['data']['list']
            # logging.info(m_lists)
            data_conf_uuid = ''
            for i in range(len(m_lists)):
                if m_lists[i]['dataConfigName'] == dataConfigName:
                    data_conf_uuid = m_lists[i]['dataConfigUUID']
                    break
        return data_conf_uuid

    def get_logic_device(self, user, dataConfigName):
        """
        获取指定数采下的逻辑设备列表
        :param user:
        :param dataConfigName:
        :return:改数采中已有的设备列表
        """
        logic_dev = []
        dataConfigUUID = self.get_data_conf_uuid(user=user, dataConfigName=dataConfigName)
        if dataConfigUUID:
            body = {"dataConfigUUID": dataConfigUUID}
            p = requests.post(url=self.base_url + CONSTANT.GATE_GET_LOGIC_DEVICES_LIST, headers=self.header, json=body)
            if p.json()['data']:
                m_lists = p.json()['data']['list']
                logging.info(m_lists)
                for i in range(len(m_lists)):
                    logic_dev.append(m_lists[i]['dev_name'])
                    logging.info(m_lists[i]['dev_name'])
        else:
            logging.error("数采不存在,无法获取逻辑设备")
        return logic_dev

    def get_dev_uuid(self, user, dataConfigName, dev_name):
        """
        根据逻辑设备名称获取逻辑设备配置的uuid
        :param user:
        :param dataConfigName:
        :param dev_name:
        :return:
        """
        dev_cd_uuid = []
        dataConfigUUID = self.get_data_conf_uuid(user=user, dataConfigName=dataConfigName)
        if dataConfigUUID:
            body = {"dataConfigUUID": dataConfigUUID}
            p = requests.post(url=self.base_url + CONSTANT.GATE_GET_LOGIC_DEVICES_LIST, headers=self.header, json=body)
            if p.json()['data']:
                m_lists = p.json()['data']['list']
                # logging.info(m_lists)
                for i in range(len(m_lists)):
                    if m_lists[i]['dev_name'] == dev_name:
                        dev_cd_uuid = m_lists[i]['cd_uuid']
                        break
        else:
            logging.error("设备不存在，无法获取逻辑设备的uuid")
        return dev_cd_uuid

    def get_ins_list(self, user, dataConfigName, dev_name):
        """
        根据设备名称获取设备的指令列表
        :param user:
        :param dataConfigName:
        :param dev_name:
        :return:指定设备的指令列表
        """
        dev_ins_list = []
        cd_uuid = self.get_dev_uuid(user=user, dataConfigName=dataConfigName, dev_name=dev_name)
        if cd_uuid:
            body = {"cd_uuid": cd_uuid, "page": 500, "size": -1}
            p = requests.post(url=self.base_url + CONSTANT.GATE_GET_DEV_INS_LIST, headers=self.header, json=body)
            if p.json()['data']:
                m_lists = p.json()['data']['list']
                # logging.info(m_lists)
                for i in range(len(m_lists)):
                    dev_ins_list.append(m_lists[i]['request_name'])
                    logging.info(m_lists[i]['request_name'])
        else:
            logging.error("设备不存在,无法获取设备的指令列表")
        return dev_ins_list

    def get_ins_uuid(self, user, dataConfigName, dev_name, ins_name):
        """
        根据指令名称获取指令uuid
        :param ins_name:
        :param user:
        :param dataConfigName:
        :param dev_name:指定请求的uuid
        :return:指定指令
        """
        ins_uuid = []
        # 根据设备名称获取设备的指令列表
        cd_uuid = self.get_dev_uuid(user=user, dataConfigName=dataConfigName, dev_name=dev_name)
        if cd_uuid:
            body = {"cd_uuid": cd_uuid, "page": 500, "size": -1}
            p = requests.post(url=self.base_url + CONSTANT.GATE_GET_DEV_INS_LIST, headers=self.header, json=body)
            if p.json()['data']:
                m_lists = p.json()['data']['list']
                # logging.info(m_lists)
                for i in range(len(m_lists)):
                    # 如果请求名称同于要获取的请求名称则返回此请求的uuid
                    if m_lists[i]['request_name'] == ins_name:
                        ins_uuid = m_lists[i]['request_uuid']
                        break
        else:
            logging.error("设备uuid不存在，所以不存在指令，无法获取指令的uuid")
        return ins_uuid

    def get_ins_list(self, user, dataConfigName, dev_name, ins_name):
        """
        根据指令名曾获取指令的参数列表
        :param user:
        :param dataConfigName:
        :param dev_name:
        :param ins_name:
        :return:
        """
        ins_para_list = []
        ins_uuid = self.get_ins_uuid(user=user, dataConfigName=dataConfigName, dev_name=dev_name, ins_name=ins_name)
        if ins_uuid:
            body = {"request_uuid": ins_uuid}
            p = requests.post(url=self.base_url + CONSTANT.GATE_GET_INS_PARA_LIST, headers=self.header, json=body)
            if p.json()['data']:
                m_lists = p.json()['data']['list']
                # logging.info(m_lists)
                for i in range(len(m_lists)):
                    ins_para_list.append(m_lists[i]['data_name'])
                    logging.info(m_lists[i]['data_name'])
        else:
            logging.error("设备不存在,无法获取设备的指令列表")
        return ins_para_list

    def add_data_conf(self, dataConfigName):
        body = {"dataConfigName": dataConfigName, "dataConfigNote": ""}
        r = requests.post(url=self.base_url + CONSTANT.GATE_ADD_DATA_COLLECT, headers=self.header, json=body)
        # print(r.json())
