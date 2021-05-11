from poium import Page, Element

'''
定义页面元素控件
'''


class gateway_ele(Page):
    # 登录页面
    user_button = Element(id_='username', describe='用户名')
    pwd_button = Element(id_='password', describe='密码')
    login_button = Element(css='.ant-btn', describe="登录")

    # 设备管理页面
    devices_manage = Element(css='#root > section > aside > div > ul > li:nth-child(2)', describe='网关配置管理')
    device_types = Element(link_text='网关数采配置', describe='网关数采配置')
    device_type_input = Element(css=".ant-input", describe='数采名称搜索框聚焦')
    device_type_select = Element(css=".ant-input", describe='设备类型搜索框输入')
    enter_device_type = Element(css=".ant-btn-link:nth-child(3)", describe='点击数采配置第一条记录的详情')

    # param_name_input = Element(css='#dataItemId .ant-select-selection__rendered', describe='参数名称聚焦')
    # param_name_text = Element(css='.ant-select-search__field__wrap > #dataItemId', describe='参数名称输入')

    # 网关
    ins_conf_back = Element(css='.ant-btn-primary:nth-child(1)', describe='数采配置返回按钮')
    # 数采配置step1:逻辑设备配置
    add = Element(css='.ant-btn:nth-child(2)', describe='添加按钮')
    logic_device_input = Element(css='#dev_id .ant-select-selection__rendered', describe='逻辑设备名称聚焦')
    logic_device_text = Element(css='.ant-select-search__field__wrap > #dev_id', describe='逻辑设备参数名称输入')
    protocol_input = Element(css='#protocol .ant-select-selection__rendered', describe='协议名称聚焦')
    hardware_interface_input = Element(css='#hardware_interface .ant-select-selection__placeholder', describe='硬件接口输入')
    dev_ip = Element(css='#dev_ip', describe='设备ip')
    dev_port = Element(css='#dev_port', describe='设备端口')
    dev_node_rtu = Element(css='#dev_node_rtu', describe='设备从站地址')
    dev_node_rtu_1 = Element(css='#dev_node_ip', describe='设备从站地址1')
    ext_input = Element(css='#ext', describe='扩展字段')
    add_logic_devices = Element(css='_1n-fmZWWxBJbATUaNKaK3C', describe='添加逻辑设备标题')
    kongbai = Element(css='.\_1VZsfUs3Qhb-yMegjGb-bP', describe='添加逻辑设备标题')
    kongbai_insCode = Element(css='.ant-table-row-cell-break-word', describe='指令UUID')
    data_conf_step1_sure = Element(css='.l7rBvnhab0XGPrSHBEJFP > .ant-btn-primary', describe='确定')
    data_conf_step1_close = Element(css='.anticon-close > svg', describe='添加失败关闭')

    # 逻辑设备step2：指令列表界面
    pages_select = Element(css='.ant-select-selection-selected-value', describe='展开翻页按钮')
    reg_type_input = Element(css='#reg_type .ant-select-selection__rendered', describe='寄存器类型框聚焦')
    reg_type_text = Element(css='.ant-select-search__field__wrap > #reg_type', describe='寄存器类型框输入')
    start_add = Element(css='#reg_addr', describe='寄存器起始地址')
    offset_len = Element(css='#offset_len', describe='偏移长度')
    timeout = Element(css='#timeout', describe='超时时间')
    try_times = Element(css='#try_times', describe='重试次数')
    executeType_input = Element(css='#executeType .ant-select-selection__rendered', describe='执行模式框聚焦')
    executeType_text = Element(css='.ant-select-search__field__wrap > #executeType', describe='执行模式框输入')
    up_way_input = Element(css='#up_way .ant-select-selection__rendered', describe='上报方式框聚焦')
    up_way_text = Element(css='.ant-select-search__field__wrap > #up_way', describe='上报方式框输入')
    fixed_time = Element(css='#fixed_time', describe='定时时间')
    daq_interval = Element(css='#daq_interval', describe='采集间隔')
    ins_conf_sure = Element(css='.\_1DiLHTzyM0CorVPQCmRV-H > .ant-btn-primary', describe='确定')
    modify_ins = Element(css='_2wn96RV18b6rzKnzkvcD49', describe='修改网关指令配置标题')
    modify_ins = Element(css='_2vOuNNtiietgfb51nd1J42', describe='修改网关指令配置标题')
    modify_ins_close = Element(css='.anticon-close > svg', describe='添加失败关闭')

    # 指令详情：指令参数配置界面
    parse_offset = Element(css='#parse_offset', describe='数据地址')
    parse_len = Element(css='#parse_len', describe='数据长度')
    parse_rule_input = Element(css='#parse_rule .ant-select-selection__rendered', describe='处理规则聚焦')
    parse_rule_text = Element(css='.ant-select-search__field__wrap > #parse_rule', describe='处理规则框输入')
    parse_value = Element(css='#parse_value', describe='解析失败默认值')
    note = Element(css='#note', describe='参数备注')
    ins_param_sure = Element(css='.\_1DiLHTzyM0CorVPQCmRV-H > .ant-btn-primary', describe='确定')
    next_page=Element(css='.ant-pagination-next > .ant-pagination-item-link', describe='下一页')
