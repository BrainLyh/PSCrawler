#!/usr/bin/env python
# encoding: utf-8
'''
@author: Brian
@file: schoolList.py
@time: 2020/6/17 11:07
@desc: 使用Selenium 对研招网开设电子信息专硕的院校及所在城市进行爬取
	   流程为：多选框选择条件、点击跳转、当前页面爬取完成、点击下一页直到所有页面完成
'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


# 配置 driver
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


# 使用 driver 爬取目标 URL
# 本代码爬取的网站有多种跳转方式，这里只选取一种
# 需要注意的是在查询专业时必须通过选择一定条件后点击查询按钮进行跳转
# 并在跳转后的页面采集数据
def use_driver(url):
    driver = set_driver(url)
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
    # 成功跳转到目标网页

    # coding here
    school_list = []
    css_selector_schoolname = "body.ch-sticky:nth-child(2) " \
                              "div.main-wrapper:nth-child(2) " \
                              "div.container.clearfix:nth-child(4) " \
                              "div.zsml-row.clearfix " \
                              "div.zsml-list-box table.ch-table " \
                              "tbody:nth-child(2) " \
                              "tr:nth-child({}) " \
                              "td:nth-child(1) " \
                              "form:nth-child(1) > a:nth-child(1)"
    css_selector_cityname   = "body.ch-sticky:nth-child(2) " \
                              "div.main-wrapper:nth-child(2) " \
                              "div.container.clearfix:nth-child(4) " \
                              "div.zsml-row.clearfix div.zsml-list-box " \
                              "table.ch-table " \
                              "tbody:nth-child(2) " \
                              "tr:nth-child(1) > td:nth-child(2)"
    css_selector_pagenumbers = "body.ch-sticky:nth-child(2) " \
                               "div.main-wrapper:nth-child(2) " \
                               "div.container.clearfix:nth-child(4) " \
                               "div.zsml-row.clearfix " \
                               "div.zsml-page-box ul.ch-page li.lip:nth-child(8) > a:nth-child(1)"
    # 翻页数
    number = driver.find_element_by_css_selector(css_selector_pagenumbers).get_attribute("textContent")

    flag = 2
    while(flag <= int(number) + 1):
        for i in range(1, 32):
            if i == 31:
                try:
                    driver.find_element_by_css_selector("#goPageNo").send_keys(str(flag))  # 输入页码跳转
                    driver.find_element_by_xpath("//input[@class='page-btn']").click()     # 点击 Go，仍然同是一个 window_handle
                    flag += 1
                except:
                    print("已经是最后一页啦".center(100, "-"))
                break
            else:
                try:
                    school_name = driver.find_element_by_css_selector(css_selector_schoolname.format(i)).get_attribute("textContent")
                    city_name = driver.find_element_by_css_selector(css_selector_cityname).get_attribute("textContent")
                    school_and_city = school_name + "     " + city_name
                    school_list.append(school_and_city)
                    print(school_and_city)
                except :
                    print("全部学校爬取完毕！".center(100, "-"))

    print(len(school_list))

    # coding here
    driver.close()
    driver.quit()

    return school_list


def save_data(data_list):
    with open("../school_name.txt", "w") as f:
        for i in data_list:
            f.write(str(i) + "\r")


def main():
    url = "https://yz.chsi.com.cn/zsml/zyfx_search.jsp"
    school_list = use_driver(url)
    save_data(school_list)


if __name__ == '__main__':
    main()
