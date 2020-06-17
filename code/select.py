from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = webdriver.Firefox()
driver.get("https://yz.chsi.com.cn/zsml/zyfx_search.jsp")
all_options = driver.find_elements_by_xpath("//select[@name='ssdm']")#elements
for option in all_options:
    print("Value is:%s" % option.get_attribute("value"))
    option.click()
