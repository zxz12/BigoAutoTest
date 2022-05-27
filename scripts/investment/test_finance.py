import re
import unittest

import requests

url = r"/api/data/v1/get?callback=jQuery1123032241082367758445_1653065824335&sortColumns=NOTICE_DATE%2CSECURITY_CODE" \
      r"&sortTypes=-1%2C-1&pageSize=50&pageNumber=1&reportName=RPT_DMSK_FN_BALANCE&columns=ALL&filter=(" \
      r"SECURITY_TYPE_CODE+in+(%22058001001%22%2C%22058001008%22))(TRADE_MARKET_CODE!%3D%22069001017%22)(" \
      r"REPORT_DATE%3D%272022-03-31%27) "
Host = "https://datacenter-web.eastmoney.com"
r = requests.get(url=Host + url, verify=False)
print(r.status_code)
print(r.text)
patt=r'"result":\{(.+?)0\}'
result=re.search(patt,string=r.text)
print(result.group())

class TestFinance(unittest.TestCase):
      def setUp(self) -> None:
            pass


      def tearDown(self) -> None:
            pass