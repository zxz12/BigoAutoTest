from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from webtest.aw.CONSTANT import CONSTANT

driver = webdriver.Chrome(CONSTANT.CHROME_DRIVER_PATH)
x=driver.get_window_rect()
print(x)