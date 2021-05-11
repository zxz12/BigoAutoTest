from poium import Page, Element

'''
定义页面元素控件
'''


class iot_ele(Page):
    # 登录页面
    user_button = Element(id_='username', describe='用户名')
    pwd_button = Element(id_='password', describe='密码')
    login_button = Element(css='.ant-btn', describe="登录")

    # 设备管理页面
    devices_manage = Element(css='#root > section > aside > div > ul > li:nth-child(3) > div.ant-menu-submenu-title',
                             describe='设备管理中心')
    device_types = Element(link_text='设备类型', describe='设备类型')
    device_type_input = Element(css="#TDeviceTypeSelect1", describe='设备类型搜索框聚焦')
    device_type_select = Element(css=".ant-select-search__field__wrap > #TDeviceTypeSelect1", describe='设备类型搜索框')
    enter_device_type = Element(css=".ant-table-row:nth-child(1) .ant-btn:nth-child(1)", describe='点击设备类型第一条记录的详情')
    # 设备类型详情页面
    ins = Element(css='.ant-radio-button-wrapper:nth-child(3)', describe='指令集按钮')
    param_name_input = Element(css='#dataItemId .ant-select-selection__rendered', describe='参数名称聚焦')
    param_name_text = Element(css='.ant-select-search__field__wrap > #dataItemId', describe='参数名称输入')
    param_type_input = Element(css='#paramType .ant-select-selection__rendered', describe='参数类型聚焦')
    param_type_text = Element(css='.ant-select-search__field__wrap > #paramType', describe='参数类型输入')
    need_radio = Element(css='.ant-radio-wrapper:nth-child(1) .ant-radio-input', describe='是否必填按钮：是')
    not_need_radio = Element(css='.ant-radio-wrapper:nth-child(2) .ant-radio-input', describe='是否必填按钮：否')
    priority_input = Element(id_='num', describe='优先级')
    defaultValue_input = Element(id_='defaultValue', describe='默认值')
    ins_add_sure_button = Element(css='.ant-btn-primary:nth-child(2)', describe='确定')
    add_para = Element(css='_2vOuNNtiietgfb51nd1J42', describe='新增参数标题')
    close = Element(css='.anticon-close > svg', describe='添加失败关闭按钮')
