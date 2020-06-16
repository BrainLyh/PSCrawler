#!/usr/bin/env python
# encoding: utf-8
'''
@author: Brian
@file: yz-chsi-com.py
@time: 2020/6/16 14:41
@desc: 使用 Selenium 尝试抓取研招网信息
'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


def set_driver(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(executable_path="E:/Program Files/chromedriver_win32/chromedriver.exe",
                        chrome_options=chrome_options)
    driver.get(url)

    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    # print(width, height)
    # 窗口最大化
    driver.set_window_size(width, height)

    return driver


def use_driver(url):
    driver = set_driver(url)
    wait = WebDriverWait(driver, 10)
    original_window = driver.current_window_handle
    assert len(driver.window_handles) == 1

    try:
        # https://selenium-python-zh.readthedocs.io/en/latest/api.html
        # 使用 Select 处理下拉框的选项
        # 先通过 Xpath 找到 select 标签，然后通过 value 找到对应值即可选择
        Select(driver.find_element_by_xpath("//select[@id='mldm']")).select_by_value('zyxw')
        Select(driver.find_element_by_xpath("//select[@id='yjxkdm']")).select_by_value("0854")

    except Exception as e:
        print("wrong " + str(e))

    driver.find_element_by_xpath("//input[@name='button']").click()

    # 等待时间过长，超时
    # wait.until(EC.number_of_windows_to_be(2))

    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

    print(driver.current_url)
    # driver.save_screenshot("yzw.jpg")

    driver.close()
    driver.quit()


def main():
    url = "https://yz.chsi.com.cn/zsml/zyfx_search.jsp"
    use_driver(url)


if __name__ == '__main__':
    main()


