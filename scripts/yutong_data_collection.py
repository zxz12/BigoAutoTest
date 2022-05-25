from webtest.aw.CONSTANT import CONSTANT
from webtest.model.files.excel import *
from webtest.model.gateway.gateway_fun import gateway_fun
from webtest.model.gateway.gateway_interface import gateway_interfance
from webtest.model.iot.iot_fun import iot_fun
from webtest.model.iot.iot_interfance import iot_interfance

logging.info('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~准备数据~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
# 变量
global insCode
insCode = 1613960000001
sheet_names = ['IOT设备类型与设备名称配置', 'IOT数据字典配置', 'IOT指令集', 'IOT指令集参数配置', 'gateway逻辑设备配置', 'gateway指令配置',
               'gateway指令参数配置',
               'Sheet1']

# 测试环境
# user = 'xianzhi'
# pwd = '123456'
# api_base_url = CONSTANT.BASE_URL_API
# gate_api_base_url = CONSTANT.GATE_BASE_URL_API
# iot_url = CONSTANT.IOT_URL
# gate_url = CONSTANT.GATE_URL
# xls_dir = '数据采集配置表测试'

# 正式环境
user = 'ytot'
pwd = 'admin123'
api_base_url = CONSTANT.BASE_URL_YUN_API
gate_api_base_url = CONSTANT.GATE_BASE_URL_YUN_API
iot_url = CONSTANT.IOT_URL_YUN
gate_url = CONSTANT.GATE_URL_YUN
xls_dir = '数据采集配置表'

files = get_xls_list(file_path=os.path.join(CONSTANT.RES_PATH, xls_dir))  # 或取此文件夹下的所有表格文件
logging.info("所有的表格文件列表：")
logging.info(files)

logging.info('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~开始执行~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
# 读取每个表格所有的的sheets页
for file in files:
    xls = excel(filename=file)
    # 获取全局的设备类型
    models = xls.get_lines(sheet_names[0])
    device_model = models[0][0]
    logging.info("此表格的设备类型是： %s" % device_model)
    # 接口登录平台
    iot_in = iot_interfance(base_url=api_base_url, user=user, pwd=pwd)
    gate_in = gateway_interfance(base_url=gate_api_base_url, user=user, pwd=pwd)
    models_list = iot_in.get_models()
    device_list = iot_in.get_devices()
    # ins_list = iot_in.get_ins(model_name=device_model)
    data_conf_list = gate_in.get_data_conf_names(user=user)

    # 添加所有的sheet页
    sheets = xls.get_sheets()
    # 添加指定的sheet页
    # sheets = [sheet_names[0], sheet_names[1]]
    for sheet in sheets:
        lines = xls.get_lines(sheet)
        # 添加设备类型和设备；line_header=['设备类型', '所属系统', '设备名称']
        if sheet == sheet_names[0]:
            for i in range(len(lines)):
                # 设备类型：如果存在则不添加
                if lines[i][0] not in models_list:
                    iot_in.add_model(model_name=lines[i][0], system_type=lines[i][1])
                # 设备：如果存在则不添加
                if lines[i][2] not in device_list:
                    iot_in.add_devices(model_name=lines[i][0], device_name=lines[i][2])
            logging.info('恭喜，恭喜！！！！sheet页添加完成：%s ' % sheet)

        # 添加数据字典；line_header=['设备类型', '数据名称', '英文名', '数据单位', '数据类型', '是否是设备检查项']
        elif sheet == sheet_names[1]:
            for i in range(len(lines)):
                # 字典：如果存在则不添加 （接口自动判断）
                iot_in.add_dict(deviceModel=lines[i][0], dataName=lines[i][1], englishName=lines[i][2],
                                dataUnit=lines[i][3], data_Type=lines[i][4])
            logging.info('恭喜，恭喜！！！！sheet页添加完成：%s ' % sheet)

        # 配置指令;header=['设备类型', '指令名称', '指令类型', '备注']
        elif sheet == sheet_names[2]:
            ins_list = iot_in.get_ins(model_name=device_model)
            for i in range(len(lines)):
                logging.info(lines[i][0])
                # 指令：如果存在则不添加
                if lines[i][1] not in ins_list:
                    iot_in.add_ins(deviceModel=lines[i][0], insName=lines[i][1], ins_Type=lines[i][2],
                                   insCode=insCode,
                                   remarks=lines[i][3])
                insCode = insCode + 1
            logging.info('恭喜，恭喜！！！！sheet页添加完成：%s ' % sheet)

        # 通过UI配置指令集参数;header=['设备类型', '指令名称', '参数名称', '参数类型', '是否必填', '默认值', '优先级']
        elif sheet == sheet_names[3]:
            iot_ui = iot_fun()
            iot_ui.login(url=iot_url, user=user, pwd=pwd)
            iot_ui.enter_devices_type(deviceType=device_model)
            # 指令参数：如果存在则不添加（如果存在，则添加失败）
            for i in range(len(lines)):
                iot_ui.add_ins(ins_name=lines[i][1], param_name=lines[i][2], param_type=lines[i][3],
                               isNeed=lines[i][4],
                               defaultValue=lines[i][5], priority=i + 1)
            logging.info('恭喜，恭喜！！！！sheet页添加完成：%s ' % sheet)

        # 添加数采配置step1:逻辑设备配置
        # header=['逻辑设备', '通讯协议', '硬件接口', '设备IP', '端口', '从站地址', '拓展字段']
        elif sheet == sheet_names[4]:
            data_conf_name = lines[0][0]
            gate_ui = gateway_fun()
            try:
                gate_ui.login(gate_url, user, pwd)
            except:
                pass
            # 数采名称：如果存在则不添加
            if data_conf_name not in data_conf_list:
                gate_in.add_data_conf(dataConfigName=data_conf_name)
            gate_ui.enter_data_conf(data_conf_name)
            # 逻辑设备：如果存在则不添加
            logic_device = gate_in.get_logic_device(user=user, dataConfigName=data_conf_name)
            for i in range(len(lines)):
                # 添加并配置逻辑设备，如果存在则不添加
                if lines[i][1] not in logic_device:
                    gate_ui.add_logic_device(logic_device=lines[i][1], protocol=lines[i][2],
                                             hardware_interface=lines[i][3], dev_ip=lines[i][4],
                                             dev_port=lines[i][5], dev_node=lines[i][6], ext=lines[i][7])
            logging.info('恭喜，恭喜！！！！sheet页添加完成：%s ' % sheet)

        # 添加数采配置step2:指令配置
        elif sheet == sheet_names[5]:
            # 获取数据采集名称
            sheet4 = xls.get_lines(sheet_names[4])
            data_name = lines[0][0]
            gate_ui = gateway_fun()
            logging.info("sheet5 网关登录")
            try:
                gate_ui.login(gate_url, user, pwd)
                logging.info("登录成功")
            except Exception as e:
                logging.info("登录失败")
                logging.info(e)
            gate_ui.enter_data_conf(data_name)
            logging.info("进入数采配置: 逻辑设备列表")
            ins_confs = {}
            for i in range(len(lines)):
                l_values = ins_confs.get(lines[i][0], [])
                l_values.append(lines[i])
                ins_confs[lines[i][0]] = l_values
            logging.info("打印表格中读取的指令字典")
            logging.info(ins_confs)
            # 进入数采名称之后，循环进入逻辑设备进行指令配置
            for key in ins_confs.keys():
                logging.info(len(ins_confs[key]))
                # 逻辑设备 : 指令列表
                gate_ui.enter_logic_device(device_name=key)
                logging.info("进入逻辑设备详情：指令列表界面，然后循环配置此设备的指令")
                for ins_conf in ins_confs[key]:
                    # ['厂房一楼空调系统ACP1-1', 'VD400-508', 'V-变量存储器', 400.0, 110.0, 1000.0, 1.0, '自动', '实时上报', 1000.0]
                    logging.info(ins_conf)
                    # 如果存在则自动添加失败，如果存在则不添加
                    gate_ui.conf_ins(ins_name=ins_conf[1], reg_type=ins_conf[2], reg_start_addr=ins_conf[3],
                                     offset_len=ins_conf[4], timeout=ins_conf[5], try_times=ins_conf[6],
                                     executeType=ins_conf[7],
                                     up_way=ins_conf[8],
                                     fixed_time=ins_conf[9], daq_interval=ins_conf[10])
                logging.info('返回指令列表界面，继续下一个设备的配置')
                gate_ui.ins_conf_back()
            logging.info('恭喜，恭喜！！！！sheet页添加完成： %s ' % sheet)

        elif sheet == sheet_names[6]:
            # 获取数据采集名称
            sheet4 = xls.get_lines(sheet_names[4])
            data_name = lines[0][0]
            ins_device_confs = {}  # 一个设备有好几个指令
            ins_name_confs = {}  # 一条指令有几个参数
            # 获取设备指令集
            for i in range(1, len(lines)):
                l_values = ins_device_confs.get(lines[i][0], [])
                l_values.append(lines[i][1:])
                ins_device_confs[lines[i][0]] = l_values
            logging.info(ins_device_confs)
            gate_ui = gateway_fun()
            try:
                gate_ui.login(gate_url, user, pwd)
            except:
                pass
            # 进入数采名称之后，循环进入逻辑设备，循环进入指令配置，循环进入参数配置，进行参数的配置
            gate_ui.enter_data_conf(data_name)
            for ins_device_name in ins_device_confs.keys():
                logging.info("进入逻辑设备详情：指令列表界面")
                gate_ui.enter_logic_device(device_name=ins_device_name)
                for ins_device_name in ins_device_confs.keys():
                    logging.info(ins_device_name)
                    ins_device_conf = ins_device_confs[ins_device_name]
                    logging.info(ins_device_conf)
                    ins_name_confs = {}  # 一条指令有几个参数
                    for i in range(len(ins_device_conf)):
                        l_values = ins_name_confs.get(ins_device_conf[i][0], [])
                        l_values.append(ins_device_conf[i][1:])
                        ins_name_confs[ins_device_conf[i][0]] = l_values
                    logging.info("读取设备对应的指令参数配置")
                    logging.info(ins_name_confs)
                for key in ins_name_confs.keys():
                    logging.info(ins_name_confs[key])
                    logging.info("进入指令详情界面：指令参数列表列表界面")
                    gate_ui.enter_ins_param_list(ins_name=key)
                    for ins_data_conf in ins_name_confs[key]:
                        logging.info(ins_data_conf)
                        gate_ui.conf_ins_param(param_name=ins_data_conf[0], parse_offset=ins_data_conf[1],
                                               parse_len=ins_data_conf[2], parse_rule=ins_data_conf[3],
                                               parse_value=ins_data_conf[4], ext=ins_data_conf[5],
                                               remark=ins_data_conf[6])
                    logging.info('返回指令列表界面，继续下一个设备的配置')
                    gate_ui.ins_conf_back()
                logging.info('返回指令列表界面，继续下一个设备的配置')
                gate_ui.ins_conf_back()
            logging.info('sheet页 %s 添加完成，恭喜，恭喜！！！！' % sheet)
    logging.info('恭喜，恭喜！！！！表格添加完成: %s ，' % file)
    xls.close()
logging.info('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~开始收尾~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
try:
    gate_ui.close_browser()
    iot_ui.close_browser()
except:
    pass
