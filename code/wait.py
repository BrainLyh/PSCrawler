from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
####显式等待####
# driver = webdriver.Firefox()
# driver.get("http://www.baidu.com")
# try:
#     element = WebDriverWait(driver,10).until(
#         EC.presence_of_all_elements_located((By.ID,"what_you_find"))
#     )
# finally:
#     driver.quit()

####隐式等待####
driver.implicitly_wait(10)
driver.get("http://www.baidu.com")
what_you_want = driver.find_element_by_id("what_you_want")
