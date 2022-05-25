from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from webtest.aw.CONSTANT import *
from webtest.model.gateway.gateway_ele import gateway_ele
from webtest.logger import logging

driver = webdriver.Chrome(CONSTANT.CHROME_DRIVER_PATH)
driver.set_window_size(1936, 1056)
driver.execute_script("document.body.style.transform='scale(0.8)'")
gate_ele = gateway_ele(driver)


class gateway_fun:

    def close_browser(self):
        """
        关闭窗口并退出浏览器
        :return:
        """
        logging.info("即将关闭浏览器")
        driver.quit()
        logging.info("浏览器退出成功")

    def open_url(self, url):
        """
        打开网址
        :param url:
        :return:
        """
        logging.info("打开URL: %s" % url)
        driver.get(url=url)

    def login(self, url, user, pwd):
        """
        @起始页面：  无
        @功能：    登录系统
        @结束页面：  首页
        :param url:
        :param user:
        :param pwd:
        :return:
        """
        self.open_url(url)
        gate_ele.user_button.send_keys(user)
        gate_ele.pwd_button.send_keys(pwd)
        gate_ele.login_button.click()
        logging.info("网关管理系统登录成功")

    def enter_data_conf(self, data_name):
        '''
        @起始页面：  首页
        @功能：    进入指定的数采详情界面，配置逻辑设备
        @结束页面：  数采配置: 逻辑设备列表
        :param data_name:数采名称
        :return:
        '''
        logging.info("进入数采： %s" % data_name)
        driver.implicitly_wait(2)
        gate_ele.devices_manage.click()
        driver.implicitly_wait(6)
        gate_conf = gate_ele.device_types
        if not gate_conf:
            driver.refresh()
            gate_ele.devices_manage.click()
            driver.implicitly_wait(6)
        gate_conf.click()
        gate_ele.device_type_input.click()
        driver.implicitly_wait(1)
        gate_ele.device_type_select.send_keys(data_name)
        driver.implicitly_wait(1)
        gate_ele.device_type_select.send_keys(Keys.ENTER)
        driver.implicitly_wait(3)
        driver.find_element_by_xpath('//td[contains(.,"%s")]/../td[9]/div/button[2]' % data_name).click()
        # gate_ele.enter_device_type.click()
        logging.info("进入数采OK")

    def add_logic_device(self, logic_device, protocol, hardware_interface, dev_ip, dev_port, dev_node, ext):
        """
        @起始页面：  逻辑设备列表；
        @功能：    添加数据采集步骤1：添加并配置逻辑设备
        @结束页面：  逻辑设备列表
        :param logic_device:
        :param protocol:
        :param hardware_interface:
        :param dev_ip:
        :param dev_port:
        :param dev_node:
        :param ext:
        :return:
        """
        if dev_port != '':
            dev_port = int(dev_port)
        if dev_node != '':
            dev_node = int(dev_node)
        if "ETH" in hardware_interface:
            hardware_interface = hardware_interface.replace(" ", '')
        protocol_type = {"ModbusRTU": 1, "ModbusTCP": 2, 'MaxgeModbusRTU': 3, "KebaOpcDa": 4, "SiemensS7": 5}
        hardware_interfaces = {
            "RS232 CH1": 1, "RS232 CH2": 2, 'RS232 CH3': 3, "RS232 CH4": 4,
            "RS485 CH1": 5, 'RS485 CH2': 6, 'RS485 CH3': 7, 'RS485 CH4': 8,
            'ETH0': 9, 'ETH1': 10
        }
        logging.info("开始配置设备 %s 的数采" % logic_device)
        driver.implicitly_wait(2)
        gate_ele.add.click()
        driver.implicitly_wait(2)
        gate_ele.logic_device_input.click()
        driver.implicitly_wait(1)
        gate_ele.logic_device_text.send_keys(logic_device)
        driver.implicitly_wait(1)
        gate_ele.logic_device_text.send_keys(Keys.ENTER)
        driver.implicitly_wait(1)
        try:
            # 点击空白处
            gate_ele.kongbai.click()
            # ActionChains(driver).move_by_offset(1000, 400).perform()
            # ActionChains(driver).click().perform()
            # driver.implicitly_wait(1)
        except:
            pass
        # 协议类型选择
        gate_ele.protocol_input.click()
        driver.implicitly_wait(1)
        protocol = protocol.replace(" ", "")
        print(protocol)
        pro_i = protocol_type[protocol]
        xpath_pro = '/html/body/div[5]/div/div/div/ul/li[%s]' % pro_i
        protocol_input_value = driver.find_element_by_xpath(xpath_pro)
        logging.info("选择接口名称为：%s " % protocol_input_value.text)
        protocol_input_value.click()
        logging.info("协议名称添加OK")
        # 硬件接口选择
        gate_ele.hardware_interface_input.click()
        driver.implicitly_wait(1)
        hard_i = hardware_interfaces[hardware_interface]
        xpath_hard = '/html/body/div[4]/div/div/div/ul/li[%s]' % hard_i
        hard_input_value = driver.find_element_by_xpath(xpath_hard)
        driver.execute_script("arguments[0].scrollIntoView();", hard_input_value)
        driver.implicitly_wait(0.5)
        hard_input_value.click()
        logging.info("选择接口名称为：%s " % hard_input_value.text)
        logging.info("硬件接口添加OK")
        if 'ETH' in hardware_interface:
            dev_ip = dev_ip.replace(" ", "")
            gate_ele.dev_ip.send_keys(dev_ip)
            gate_ele.dev_port.send_keys(dev_port)
        try:
            gate_ele.dev_node_rtu.send_keys(dev_node)
        except:
            gate_ele.dev_node_rtu_1.send_keys(dev_node)
        if ext != '':
            gate_ele.ext_input.send_keys(ext)
        gate_ele.data_conf_step1_sure.click()
        driver.implicitly_wait(2)
        try:
            # 如果还在当前页面则添加失败
            page = gate_ele.add_logic_devices
            if page:
                logging.info("关闭添加逻辑设备页面，继续添加下一个")
                close = gate_ele.data_conf_step1_close
                close.click()
                logging.error("逻辑设备 %s 数采配置失败！" % logic_device)
        except:
            logging.info("逻辑设备 %s 数采配置成功！" % logic_device)

    def enter_logic_device(self, device_name):
        '''
        @起始页面：  数采配置: 逻辑设备列表
        @功能：    进入指定的逻辑设备
        @结束页面：  逻辑设备 : 指令列表
        :param device_name:
        :return:
        '''
        global bro
        logging.info("进入逻辑设备: %s 的指令列表" % device_name)
        driver.implicitly_wait(15)
        try:
            # 设置每页显示20条记录
            gateway_ele.pages_select.click()
            page_fath = '//*[@id="f695bfeb-e035-4e15-b247-d326cdabed93"]/ul/li[7]'
            driver.find_element_by_xpath(page_fath).click()
            driver.implicitly_wait(1)
        except:
            pass
        logging.info("获取总页数，循环在每页中查找 %s " % device_name)
        # 获取总页数，循环在每页中查找
        num = self.get_pages()
        logging.info("开始循环")
        driver.find_element_by_link_text('1').click()  # 每次都从第一页开始查找
        for i in range(num):
            logging.info("第 %s 次循环：" % i)
            try:
                logging.info("查找参数名称")
                # driver.execute_script("window .find（%s，false，false，false，false，false，false）;" % device_name)
                bro = driver.find_element_by_xpath('//td[contains(.,"%s")]/../td[12]/span/button[2]' % device_name)
                logging.info("找到了")
                logging.info(bro.text)
                driver.execute_script("arguments[0].scrollIntoView();", bro)
                driver.implicitly_wait(0.5)
                break
            except:
                gate_ele.next_page.click()
        try:
            bro.click()
            logging.info("点击可见元素")
        except:
            driver.execute_script("arguments[0].click();", bro)  # 向下滑动至可见
            logging.info("点击不可见元素")
            driver.implicitly_wait(0.5)

        # 原来的
        # xpath_device_name = '//td[contains(.,"%s")]/../td[12]/span/button[2]' % device_name
        # logging.info(xpath_device_name)
        # driver.find_element_by_xpath(xpath_device_name).click()
        driver.implicitly_wait(1)
        logging.info("进入设备： %s 的指令列表OK" % device_name)

    def conf_ins(self, ins_name, reg_type, reg_start_addr, offset_len, timeout, try_times, executeType, up_way,
                 fixed_time, daq_interval):
        """
        @起始页面：  逻辑设备 : 指令列表
        @功能：    为指定的设备配置指令
        @结束页面： 逻辑设备 : 指令列表
        :param ins_name:指令名称
        :param reg_type:寄存器类型
        :param reg_start_addr:寄存器起始地址
        :param offset_len:偏移长度
        :param timeout:超时时间0
        :param try_times:重试次数
        :param executeType:执行方式
        :param up_way:上报方式
        :param fixed_time:定时时间，当上报方式为定时时生效
        :param daq_interval:采集时间间隔
        :return:
        """
        logging.info("配置指令：%s" % ins_name)
        reg_start_addr = int(reg_start_addr)
        offset_len = int(offset_len)
        timeout = int(timeout)
        try_times = int(try_times)
        daq_interval = int(daq_interval)
        reg_type = reg_type.split('-')[0]
        logging.info("获取总页数，循环在每页中查找")
        driver.implicitly_wait(8)
        # 获取总页数，循环在每页中查找
        num = self.get_pages()
        logging.info("开始循环")
        # 循环1，2，3
        driver.find_element_by_link_text('1').click()  # 每次都从第一页开始查找
        for i in range(num):
            try:
                # 查找参数名称
                # driver.execute_script("window .find（%s，false，false，false，false，false，false）;" % ins_name)
                bro = driver.find_element_by_xpath(
                    '//td[contains(.,"%s")]/../td[14]/span/button[1]' % ins_name)  # 指令参数采集项配置
                logging.info(bro.text)
                driver.execute_script("arguments[0].scrollIntoView();", bro)
                driver.implicitly_wait(0.5)
                break
            except:
                gate_ele.next_page.click()
        # logging.error("所有页面均未找到指令： %s" % ins_name)
        # ins_detail_xpath = '//td[contains(.,"%s")]/../td[14]/span/button[1]' % ins_name  # 指令详情
        # driver.find_element_by_xpath(ins_detail_xpath).click()
        try:
            bro.click()
        except:
            # 元素在窗口之外时，滑动至可见
            # gateway_ele.kongbai_insCode.click()
            # driver.implicitly_wait(0.5)
            driver.execute_script("arguments[0].click();", bro)  # 向下滑动至可见
            driver.implicitly_wait(0.5)
            # bro.click()
        try:
            # 寄存器类型
            driver.implicitly_wait(1)
            gate_ele.reg_type_input.click()
        except:
            driver.find_element_by_xpath('//td[contains(.,"%s")]/../td[14]/span/button[1]' % ins_name).click()
            driver.implicitly_wait(1)
            gate_ele.reg_type_input.click()
        driver.implicitly_wait(1)
        gate_ele.reg_type_text.send_keys(reg_type)
        driver.implicitly_wait(1)
        gate_ele.reg_type_text.send_keys(Keys.ENTER)
        driver.implicitly_wait(1)
        gate_ele.start_add.clear()
        gate_ele.start_add.send_keys(reg_start_addr)
        gate_ele.offset_len.clear()
        gate_ele.offset_len.send_keys(offset_len)
        gate_ele.timeout.clear()
        gate_ele.timeout.send_keys(timeout)
        gate_ele.try_times.clear()
        gate_ele.try_times.send_keys(try_times)
        # 执行模式
        gate_ele.executeType_input.click()
        driver.implicitly_wait(1)
        gate_ele.executeType_text.send_keys(executeType)
        driver.implicitly_wait(1)
        gate_ele.executeType_text.send_keys(Keys.ENTER)
        driver.implicitly_wait(1)
        # 上报方式
        gate_ele.up_way_input.click()
        driver.implicitly_wait(1)
        gate_ele.up_way_text.send_keys(up_way)
        driver.implicitly_wait(1)
        gate_ele.up_way_text.send_keys(Keys.ENTER)
        driver.implicitly_wait(1)
        if "定时" in up_way:
            gate_ele.fixed_time.clear()
            gate_ele.fixed_time.send_keys(int(fixed_time))
        gate_ele.daq_interval.clear()
        gate_ele.daq_interval.send_keys(daq_interval)
        gate_ele.ins_conf_sure.click()
        driver.implicitly_wait(2)
        try:
            gate_ele.modify_ins_close.click()
            logging.error("指令 %s 配置失败！" % ins_name)
        except:
            logging.info("指令 %s 配置成功！" % ins_name)

    def enter_ins_param_list(self, ins_name):
        '''
        @起始页面： 逻辑设备 : 指令列表
        @功能：    进入指定的指令，以配置指令参数参数
        @结束页面：  指令配置 : 参数列表
        :param param_name:
        :return:
        '''
        logging.info("进入指令： %s 的参数列表" % ins_name)
        driver.implicitly_wait(8)
        try:
            # 设置每页显示20条记录
            gateway_ele.pages_select.click()
            page_path = '//*[@id="f695bfeb-e035-4e15-b247-d326cdabed93"]/ul/li[7]'
            driver.find_element_by_xpath(page_path).click()
            driver.implicitly_wait(1)
        except:
            pass
        logging.info("获取总页数，循环在每页中查找")
        # 获取总页数，循环在每页中查找
        num = self.get_pages()
        logging.info("开始循环")
        # 循环1，2，3
        driver.find_element_by_link_text('1').click()  # 每次都从第一页开始查找
        for i in range(num):
            logging.info(i)
            try:
                # logging.info("查找")
                # driver.execute_script(js % (ins_name,ins_name))
                # logging.info("查找OK")
                bro = driver.find_element_by_xpath(
                    '//td[contains(.,"%s")]/../td[14]/span/button[3]' % ins_name)  # 指令参数配置控件
                logging.info(bro.text)
                driver.execute_script("arguments[0].scrollIntoView();", bro)
                driver.implicitly_wait(0.5)
                break
            except:
                gate_ele.next_page.click()
        try:
            bro.click()
            logging.info("点击可见元素")
        except:
            driver.execute_script("arguments[0].click();", bro)  # 向下滑动至可见
            logging.info("点击不可见元素")
            driver.implicitly_wait(0.5)
            # bro.click()
        # ins_param_xpath = '//td[contains(.,"%s")]/../td[14]/span/button[3]' % ins_name  # 指令参数配置控件
        # logging.info(ins_param_xpath)
        # driver.find_element_by_xpath(ins_param_xpath).click()
        driver.implicitly_wait(2)
        # #概率进入失败
        # try:
        #     driver.find_element_by_xpath(
        #         '//td[contains(.,"%s")]/../td[14]/span/button[3]' % ins_name).click()
        # except:
        #     pass
        logging.info("进入指令参数列表OK")
        try:
            bro = driver.find_element_by_xpath(
                '//td[contains(.,"%s")]/../td[14]/span/button[3]' % ins_name)  # 指令参数配置控件
            if bro:
                logging.info("进入指令参数失败,下拉滚动条，继续点击")
                driver.find_element_by_class_name('ant-table-tbody').click()  # 选中表格
                driver.execute_script("window.scrollTo(0,800);")  # 向下滑动500像素
                driver.execute_script("window.scrollTo(500,0);")  # 向下滑动500像素
                bro = driver.find_element_by_xpath(
                    '//td[contains(.,"%s")]/../td[14]/span/button[3]' % ins_name)  # 指令参数配置控件
                bro.click()
                logging.warn("重新进入")
        except Exception as e:
            logging.info(e)

    def conf_ins_param(self, param_name, parse_offset, parse_len, parse_rule, parse_value, ext, remark):
        '''
        @起始页面：  指令配置 : 参数列表
        @功能：    进入指定的指令，以配置指令参数
        @结束页面：  指令配置 : 参数列表
        :param remark:
        :param ext:
        :param parse_value:
        :param parse_rule:
        :param parse_len:
        :param parse_offset:
        :param param_name:
        :return:
        '''
        logging.info("配置参数： %s" % param_name)
        driver.implicitly_wait(8)
        try:
            # 设置每页显示20条记录
            gateway_ele.pages_select.click()
            page_fath = '//*[@id="f695bfeb-e035-4e15-b247-d326cdabed93"]/ul/li[7]'
            driver.find_element_by_xpath(page_fath).click()
            driver.implicitly_wait(1)
        except:
            pass
        logging.info("获取总页数，循环在每页中查找")
        # 获取总页数，循环在每页中查找
        num = self.get_pages()
        logging.info("开始循环")
        # 循环1，2，3
        driver.find_element_by_link_text('1').click()#每次都从第一页开始查找
        for i in range(num):
            logging.info(i)
            try:
                # 查找参数名称
                # driver.execute_script("window .find（%s，false，false，false，false，false，false）;" % param_name)
                bro = driver.find_element_by_xpath(
                    '//td[contains(.,"%s")]/../td[14]/span/button/span' % param_name)  # 指令参数采集项配置
                logging.info(bro.text)
                driver.execute_script("arguments[0].scrollIntoView();", bro)
                driver.implicitly_wait(1)
                break
            except:
                gate_ele.next_page.click()
        try:
            bro.click()
            logging.info("可见")
        except:
            # 元素在窗口之外时，滑动至可见
            # gateway_ele.kongbai_insCode.click()
            # driver.implicitly_wait(0.5)
            driver.execute_script("arguments[0].click();", bro)  # 向下滑动至可见
            logging.info("不可见")
            driver.implicitly_wait(0.5)
            # bro.click()

        # ins_param_xpath = '//td[contains(.,"%s")]/../td[14]/span/button' % param_name  # 参数详情
        # logging.info(ins_param_xpath)
        # driver.find_element_by_xpath(ins_param_xpath).click()
        driver.implicitly_wait(1)
        # 判断是进入详情界面
        try:
            offset = gate_ele.parse_offset
            logging.info(offset.text)
            if not offset:
                logging.info("进入指令详情失败，当前仍停留在参数列表界面")
                bro = driver.find_element_by_xpath(
                    '//td[contains(.,"%s")]/../td[14]/span/button/span' % param_name)  # 详情
                for _ in range(5):
                    bro.send_keys(Keys.DOWN)
                bro.click()
                logging.info("重新进入详情OK")
        except Exception as e:
            logging.warn(e)
        gate_ele.parse_offset.clear()
        gate_ele.parse_offset.send_keys(int(parse_offset))
        gate_ele.parse_len.clear()
        gate_ele.parse_len.send_keys(int(parse_len))
        # 处理规则
        gate_ele.parse_rule_input.click()
        driver.implicitly_wait(1)
        gate_ele.parse_rule_text.send_keys(parse_rule)
        driver.implicitly_wait(1)
        gate_ele.parse_rule_text.send_keys(Keys.ENTER)
        driver.implicitly_wait(1)
        gate_ele.parse_value.clear()
        gate_ele.parse_value.send_keys(parse_value)
        if ext != '':
            if isinstance(ext, float):
                ext = int(ext)
            gate_ele.ext_input.clear()
            gate_ele.ext_input.send_keys(ext)
        if remark != '':
            gate_ele.note.clear()
            gate_ele.note.send_keys(remark)
        gate_ele.ins_conf_sure.click()
        driver.implicitly_wait(3)
        try:
            # 如果还在当前页面则添加失败
            gate_ele.modify_ins_close.click()
            logging.error("参数 %s 配置失败！" % param_name)
        except:
            logging.info("参数 %s 配置成功！" % param_name)

    def ins_conf_back(self):
        '''
        @起始页面：  网关指令列表页面
        @功能：    进入指定的指令，以配置指令参数参数
        @结束页面：  网关指令详情：参数列表界面
        :param param_name:
        :return:
        '''
        logging.info("返回")
        driver.implicitly_wait(2)
        gate_ele.ins_conf_back.click()
        driver.implicitly_wait(2)

    def get_pages(self):
        '''
        获取总页数
        :return:
        '''
        # 获取总页数，循环在每页中查找
        driver.implicitly_wait(5)
        cs = '.ant-pagination-item'
        pages = driver.find_elements_by_css_selector(cs)
        num = len(pages)
        logging.info("总页数为： %s" % pages[num - 1].text)
        n = int(pages[num - 1].text)
        return n
