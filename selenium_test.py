#coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

# 为了解决这个问题：
# UserWarning: Selenium support for PhantomJS has been deprecated,
# please use headless versions of Chrome or Firefox instead
# 使用无头浏览器
#driver = webdriver.PhantomJS()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(executable_path="E:/Program Files/chromedriver_win32/chromedriver.exe",
                          chrome_options=chrome_options)
driver.get("http://www.baidu.com/")
data = driver.find_element_by_id("wrapper").text

print(driver.title)
print(driver.current_window_handle)
driver.find_element_by_id("kw").send_keys(u"长城")
# 百度一下的id:su
driver.find_element_by_id("su").click()

print(driver.current_window_handle)
# 全选输入内容
input = driver.find_element_by_id("kw").send_keys(Keys.CONTROL, 'a')
# print("输入框内容：" + input)

# 剪切输入框内容
cut = driver.find_element_by_id("kw").send_keys(Keys.CONTROL, 'x')

# 在访问第一个元素之前 sleep 2s,可以避免 InvalidElementStateException 错误
# 原因是 PhantomJS 驱动程序不等待页面加载
# 由于不同的请求机制，采用 chromedriver 之后不必再等待
# time.sleep(2)

# 取到href
href = driver.find_element_by_xpath("html/body/div/div[1]/div[2]/a[1]").get_attribute("href")
print("当前位置： " + href)

driver.find_element_by_id("su").send_keys(Keys.RETURN)
driver.find_element_by_id("kw").clear()

# 生成页面快照并保存
driver.save_screenshot("baidu.png")

print("当前URL " + driver.current_url)
# print(driver.page_source)

driver.close()
driver.quit()
