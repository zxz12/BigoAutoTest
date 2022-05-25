import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from webtest.aw.CONSTANT import *
from webtest.model.iot.iot_ele import iot_ele
from webtest.logger import logging

driver = webdriver.Chrome(CONSTANT.CHROME_DRIVER_PATH)
driver.maximize_window()
# set_window_size(1936, 1056)
iot_ele = iot_ele(driver)


class iot_fun:

    def close_browser(self):
        """
        关闭窗口并退出浏览器
        :return:
        """
        driver.quit()
        logging.info("浏览器退出成功")

    def open_url(self, url):
        """
        打开网址
        :param url:
        :return:
        """
        driver.get(url=url)

    def login(self, url, user, pwd):
        """
        登录IOT平台
        :param url:
        :param user:
        :param pwd:
        :return:
        """
        self.open_url(url)
        iot_ele.user_button.send_keys(user)
        iot_ele.pwd_button.send_keys(pwd)
        iot_ele.login_button.click()
        logging.info("iot 平台登录成功")

    def enter_devices_type(self, deviceType):
        """
        进入指定设备类型的设备详情
        :param deviceType:设备类型
        :setup 任意页面
        :return:设备类型详情页
        """
        driver.implicitly_wait(2)
        iot_ele.devices_manage.click()
        driver.implicitly_wait(1)
        iot_ele.device_types.click()
        iot_ele.device_type_input.click()
        driver.implicitly_wait(1)
        iot_ele.device_type_select.send_keys(deviceType)
        driver.implicitly_wait(1)
        iot_ele.device_type_select.send_keys(Keys.ENTER)
        driver.implicitly_wait(1)
        iot_ele.enter_device_type.click()
        driver.implicitly_wait(2)
        # time.sleep(2)
        # import requests
        # deviceType = requests.utils.quote(deviceType)
        # url = 'http://10.110.1.188/iot/#/device/type/details?id=%s&modelName=%s' % (modle_id,deviceType)
        # print(url)
        # # driver.get(url)
        # js = 'window.open("%s");' % url
        # iot_ele.execute_script(js)
        # driver.implicitly_wait(2)
        # handles = driver.window_handles
        # for handle in handles:
        #     print(driver.title)
        #     if deviceType in driver.title:
        #         driver.switch_to.window(handle)
        # driver.refresh()

    def add_ins(self, ins_name, param_name, param_type, isNeed, defaultValue, priority):
        needs = {"必填": 1}
        need = needs.get(isNeed, 0)
        if defaultValue:
            defaultValue = int(defaultValue)
        # driver.refresh()
        driver.implicitly_wait(5)
        iot_ele.ins.click()
        driver.implicitly_wait(5)
        logging.info("获取总页数，循环在每页中查找： %s" % ins_name)
        # 获取总页数，循环在每页中查找
        cs = '.ant-pagination-item'
        pages = driver.find_elements_by_css_selector(cs)
        logging.info("总页数：")
        logging.info(len(pages))
        logging.info("开始循环")
        # 循环1，2，3
        for i in range(1, len(pages) + 2):
            print(i)
            try:
                driver.find_element_by_link_text(str(i)).click()
            except:
                pass
            # driver.execute_script("arguments[0].scrollIntoView();", page)
            # 指定名称后面的详情
            try:
                bro = driver.find_element_by_xpath('//td[contains(.,"%s")]/../td[7]/span/button[3]' % ins_name)
                print(bro)
                break
            except:
                pass
        bro.click()
        driver.implicitly_wait(5)
        iot_ele.param_name_input.click()
        driver.implicitly_wait(1)
        iot_ele.param_name_text.send_keys(param_name)
        driver.implicitly_wait(2)
        iot_ele.param_name_text.send_keys(Keys.ENTER)
        iot_ele.param_type_input.click()
        driver.implicitly_wait(1)
        iot_ele.param_type_text.send_keys(param_type)
        driver.implicitly_wait(1)
        iot_ele.param_type_text.send_keys(Keys.ENTER)
        if param_type == "入参":
            if need:
                iot_ele.need_radio.click()
                iot_ele.defaultValue_input.click()
                if isinstance(defaultValue, float):
                    defaultValue = int(defaultValue)
                iot_ele.defaultValue_input.send_keys(defaultValue)
            else:
                iot_ele.not_need_radio.click()
        if priority:
            iot_ele.priority_input.send_keys(Keys.BACKSPACE)
            iot_ele.priority_input.send_keys(int(priority))
        iot_ele.ins_add_sure_button.click()
        time.sleep(1)
        try:
            iot_ele.close.click()
            logging.error("指令 %s 配置失败！" % ins_name)
        except:
            logging.info("指令 %s 配置成功！" % ins_name)
