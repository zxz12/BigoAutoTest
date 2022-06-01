import json
import re
import requests
from dfx.logger import logging
from dfx.opr_excel import csv

url = r"/api/data/v1/get?callback=jQuery1123032241082367758445_1653065824335&sortColumns=NOTICE_DATE%2CSECURITY_CODE" \
      r"&sortTypes=-1%2C-1&pageSize=50&pageNumber=1&reportName=RPT_DMSK_FN_BALANCE&columns=ALL&filter=(" \
      r"SECURITY_TYPE_CODE+in+(%22058001001%22%2C%22058001008%22))(TRADE_MARKET_CODE!%3D%22069001017%22)(" \
      r"REPORT_DATE%3D%272022-03-31%27) "
Host = "https://datacenter-web.eastmoney.com"


def get_response(url):
    r = requests.get(url=Host + url, verify=False)
    logging.info(r.status_code)
    patt = r':\{(.+?)[0-9]\}'
    result = re.search(patt, string=r.text)
    rst = result.group()[1:]
    logging.info(rst)
    dicts = json.loads(rst, strict=False)
    page = dicts.get("pages")
    return dicts, page


def get_datas(dicts, page=1):
    sock_datas = []
    for socket in dicts['data']:
        sock_data = []
        sock_data.append(socket["SECURITY_CODE"])  # 股票代码
        sock_data.append(socket["SECURITY_NAME_ABBR"])  # 公司名称
        # 货币资金
        if socket["MONETARYFUNDS"]:
            sock_data.append(round(socket["MONETARYFUNDS"] / pow(10, 8), 2))
        else:
            socket["MONETARYFUNDS"] = 0
        # 应收账款
        if socket["ACCOUNTS_RECE"]:
            sock_data.append(round(socket["ACCOUNTS_RECE"] / pow(10, 8), 2))
        else:
            sock_data.append(0)  # 应收账款
        # 存货
        if socket["INVENTORY"]:
            sock_data.append(round(socket["INVENTORY"] / pow(10, 8), 2))
        else:
            sock_data.append(0)  # 应收账款
        # 总资产
        if socket["TOTAL_ASSETS"]:
            sock_data.append(round(socket["TOTAL_ASSETS"] / pow(10, 8), 2))
        else:
            sock_data.append(0)
        # 总资产同比
        if socket["TOTAL_ASSETS_RATIO"]:
            sock_data.append('{:.2f}%'.format(socket["TOTAL_ASSETS_RATIO"]))
        else:
            sock_data.append('{:.2f}%'.format(0))
        # 应付账款
        if socket["ACCOUNTS_PAYABLE"]:
            sock_data.append(round(socket["ACCOUNTS_PAYABLE"] / pow(10, 8), 2))
        else:
            sock_data.append(0)
        # 预收账款
        if socket["ADVANCE_RECEIVABLES"]:
            sock_data.append(round(socket["ADVANCE_RECEIVABLES"] / pow(10, 8), 2))
        else:
            sock_data.append(0)
        # 总负债
        if socket["TOTAL_LIABILITIES"]:
            sock_data.append(round(socket["TOTAL_LIABILITIES"] / pow(10, 8), 2))
        else:
            sock_data.append(0)
        # 资产负债率
        if socket["DEBT_ASSET_RATIO"]:
            debt_radio = round(socket["DEBT_ASSET_RATIO"], 2)
            sock_data.append('{:.2f}%'.format(socket["DEBT_ASSET_RATIO"]))
        else:
            debt_radio = 0
            sock_data.append('{:.2f}%'.format(0))
        # 股东权益合计
        if socket["TOTAL_EQUITY"]:
            sock_data.append(round(socket["TOTAL_EQUITY"] / pow(10, 8), 2))
        else:
            sock_data.append(0)
        # 公告日期
        if socket["NOTICE_DATE"]:
            sock_data.append(socket["NOTICE_DATE"].split(" ")[0])
        else:
            sock_data.append(0)
        logging.info(sock_data)
        if debt_radio < 50:
            sock_datas.append(sock_data)
    return sock_datas


dicts, page = get_response(url)
datas = get_datas(dicts, page)
header = ["股票代码", "公司名称", "货币资金", "应收账款", "存货", "总资产", "总资产同比", "应付账款", "预收账款", "总负债", "资产负债率", "股东权益合计",
          "公告日期"]
f1 = csv.write_csv(header=header, datas=datas)
