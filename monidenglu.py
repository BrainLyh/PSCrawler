#encoding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# driver = webdriver.PhantomJS(executable_path=r"E:\download\PhantomJS\phantomjs-2.1.1-windows\bin\phantomjs.exe")
driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'],executable_path=r"E:\download\PhantomJS\phantomjs-2.1.1-windows\bin\phantomjs.exe")
# driver.get("http://www.douban.com/")
# driver.get("http://www.youku.com/")
driver.get('http://101.132.41.135/login')

# driver.find_element_by_id("userneme").send_keys("..........")
# driver.find_element_by_id("password").send_keys("..........")

driver.find_element_by_xpath(".//*[@id='name-input']").send_keys("1889023789@qq.com")
driver.find_element_by_xpath(".//*[@id='password-input']").send_keys("1234567890")

driver.find_element_by_xpath("html/body/main/div[2]/div/div/form/div[3]/div[2]/button").click()

time.sleep(3)
driver.save_screenshot("douban.png")

driver.quit()