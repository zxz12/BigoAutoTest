import os


class CONSTANT:
    # 项目相关路径
    ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    AW_PATH = os.path.join(ROOT_PATH, 'aw')
    RES_PATH = os.path.join(ROOT_PATH, 'res')
    REPORT_PATH = os.path.join(ROOT_PATH, 'report')

    # 驱动路径
    # CHROME_DRIVER_PATH = r'D:\dev\pycharm_space\gateway\res\chromedriver.exe'
    CHROME_DRIVER_PATH = os.path.join(RES_PATH, 'chromedriver.exe')
    PACP_Y_PATH = r'D:\dev\pycharm_space\gateway\res\pscp_y.exe'
    GATEWAY_LOCAL_PATH = 'D:\\dev\\pycharm_space\\gateway\\res\\vir_V100.001.00.009\\'

    # IOT平台UI
    IOT_URL = "http://10.110.1.188/iot/"
    IOT_URL_YUN = "http://122.112.253.184//iot/"
    GATEWAY_PORT = '8050'
    MQTT_IP = '10.110.1.183'

    # websocket
    WEBSOCKET_SERVER = "http://10.110.1.192:8080/"

    # IOT接口
    BASE_URL_YUN_API = 'http://119.3.32.248:8082'
    BASE_URL_API = 'http://10.110.1.188:8082'
    # iot接口
    LOGIN_API = '/login'
    LOGIN_HEADER = {'Content-Type': 'application/json;charset=utf-8'}
    GATEWAY_LIST_API = '/GatewayItem/list'
    GATEWAY_DELETE_API = '/GatewayItem/delete'
    ADD_DEVICE_API = '/deviceInstance/add'
    DEVICE_MODEL_LIST_API = '/deviceModel/list'
    ADD_DEVICE_MODEL_API = '/deviceModel/add'
    GET_DEVICE_LIST = '/deviceInstance/page/list'
    GET_INS_LIST = '/ins/list/page'
    GET_MODEL_LIST = '/deviceModel/list'
    INSERT_INS = '/ins/insert'
    ADD_DICT = '/deviceDictionary/add'

    # 网关网址
    GATE_URL = "http://10.110.1.188/gateway/"
    GATE_URL_YUN = "http://122.112.253.184//gateway/"

    # 网关接口
    GATE_BASE_URL_YUN_API = 'http://119.3.32.248:8001'
    GATE_BASE_URL_API = 'http://10.110.1.188:8001'
    GATE_ADD_DATA_COLLECT = '/data/collect/insert'
    GATE_GET_DATA_CONF_LIST = '/data/collect/selectDataCollectListByPage'
    GATE_GET_LOGIC_DEVICES_LIST = '/data/collect/device/selectByCollectIdPage'
    GATE_GET_DEV_INS_LIST = '/collect/device/request/selectByCdUuidPage'
    GATE_GET_INS_PARA_LIST = '/collect/device/requestItem/selectByRequestUuidPage'
