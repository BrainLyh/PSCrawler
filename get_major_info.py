#!/usr/bin/env python
# encoding: utf-8
'''
@author: Brian
@file: get_major_info.py
@time: 2020/6/18 10:22
@desc: 测试学校对应的研究方向页面内的页面跳转
'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def set_driver():
    url = "https://yz.chsi.com.cn/zsml/queryAction.do"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(executable_path="E:/Program Files/chromedriver_win32/chromedriver.exe",
                                  chrome_options=chrome_options)
    driver.get(url)

    driver = set_height_width(driver)

    print("set driver: " + driver.current_window_handle)
    driver.save_screenshot("set-driver.jpg")
    return driver


def set_height_width(driver):
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    driver.set_window_size(width, height)
    return driver


# 如果需要翻页就翻页
def paging(driver):

    css_selector_pages = "body.ch-sticky:nth-child(2) " \
                         "div.main-wrapper:nth-child(2) " \
                         "div.container.clearfix:nth-child(5) " \
                         "div.zsml-row.clearfix div.zsml-page-box > ul.ch-page"

    ul = driver.find_element_by_css_selector(css_selector_pages)
    li = ul.find_elements_by_xpath("li")
    if(len(li) < 10):
        pagenumber = int(li[-2].text)

    else:
        pagenumber = int(li[-3].text)
    return pagenumber


def select_major(driver):
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
    driver = set_height_width(driver)
    print("select driver " + driver.current_window_handle)
    driver.save_screenshot("select-driver.jpg")
    return driver


# 获得所有院校列表
def get_school_name(driver):
    original_window = driver.current_window_handle
    school_name_list = []
    all_major_list = []
    # 定位学校名称、所在城市、页面数量
    css_selector_schoolname = "body.ch-sticky:nth-child(2) " \
                              "div.main-wrapper:nth-child(2) " \
                              "div.container.clearfix:nth-child(4) " \
                              "div.zsml-row.clearfix " \
                              "div.zsml-list-box table.ch-table " \
                              "tbody:nth-child(2) " \
                              "tr:nth-child(1) " \
                              "td:nth-child(1) " \
                              "form:nth-child(1) > a:nth-child(1)"
    css_selector_cityname = "body.ch-sticky:nth-child(2) " \
                            "div.main-wrapper:nth-child(2) " \
                            "div.container.clearfix:nth-child(4) " \
                            "div.zsml-row.clearfix div.zsml-list-box " \
                            "table.ch-table " \
                            "tbody:nth-child(2) " \
                            "tr:nth-child(1) > td:nth-child(2)"

    school_name = driver.find_element_by_css_selector(css_selector_schoolname).get_attribute(
        "textContent")
    city_name = driver.find_element_by_css_selector(css_selector_cityname).get_attribute("textContent")

    driver.find_element_by_link_text(school_name).click()

    # 跳转到学校对应的页面
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

    # print("get major name " + driver.current_window_handle)
    driver = set_height_width(driver)
    # driver.save_screenshot("get-major.jpg")

    # 得到各个研究方向的列表
    major_list = get_major(driver)
    all_major_list.append(major_list)
    school_and_city = school_name + "     " + city_name

    school_name_list.append(school_and_city)

    driver.close()
    driver.switch_to.window(original_window)
    driver = set_height_width(driver)
    # print("跳转结束" + driver.current_window_handle)
    # driver.save_screenshot("跳转结束.jpg")
    print(school_name_list)
    print(major_list)
    print(all_major_list)

    driver.close()
    driver.quit()

    return school_name_list,all_major_list


def get_major(driver):
    # 当前页面有多少条数据
    major_list = []
    # 当前 Tab 里有多少个页面
    pagenumber = paging(driver)
    print(pagenumber)

    # 定位研究方向
    css_selector_major = "body.ch-sticky:nth-child(2) " \
                         "div.main-wrapper:nth-child(2) " \
                         "div.container.clearfix:nth-child(5) " \
                         "div.zsml-row.clearfix " \
                         "div.zsml-list-box table.ch-table " \
                         "tbody:nth-child(2) " \
                         "tr:nth-child({}) > td:nth-child(4)"
    css_selector_number = "body.ch-sticky:nth-child(2) " \
                          "div.main-wrapper:nth-child(2) " \
                          "div.container.clearfix:nth-child(5) " \
                          "div.zsml-row.clearfix " \
                          "div.zsml-list-box " \
                          "table.ch-table " \
                          "tbody:nth-child(2) " \
                          "tr:nth-child({}) " \
                          "td.ch-table-center:nth-child(7) > a.js-from-title:nth-child(2)"
    css_selector_jumpto = "body.ch-sticky:nth-child(2) " \
                          "div.main-wrapper:nth-child(2) " \
                          "div.container.clearfix:nth-child(5) " \
                          "div.zsml-row.clearfix " \
                          "div.zsml-page-box ul.ch-page "
    if(pagenumber == 1):
        # 不用下一页操作
        numbers = driver.find_elements_by_xpath("//tbody//tr")
        for i in range(1, len(numbers)+1):
            try:
                major = driver.find_element_by_css_selector(css_selector_major.format(i)).get_attribute("textContent")
                number = driver.find_element_by_css_selector(css_selector_number.format(i)).get_attribute("data-title")
                major_number = major + "  " + number
                major_list.append(major_number)
            except Exception as e:
                print(e)
    elif(pagenumber < 7 ):
        # 找到下一页按钮
        while(pagenumber):
            numbers = driver.find_elements_by_xpath("//tbody//tr")
            for i in range(1, len(numbers)+1):
                try:
                    major = driver.find_element_by_css_selector(css_selector_major.format(i)).get_attribute("textContent")
                    number = driver.find_element_by_css_selector(css_selector_number.format(i)).get_attribute("data-title")
                    major_number = major + "  " + number
                    major_list.append(major_number)
                except Exception as e:
                    print(e)
            ul = driver.find_element_by_css_selector(css_selector_jumpto)
            li = ul.find_elements_by_xpath("li")
            li[-1].click()
            pagenumber -= 1
    else:
        # 下一页按钮位置不同,用 Go
        flag = 2  # 下一次要Go的页码
        while(pagenumber):
            numbers = driver.find_elements_by_xpath("//tbody//tr")

            for i in range(1, len(numbers)+1):
                try:
                    major = driver.find_element_by_css_selector(css_selector_major.format(i)).get_attribute("textContent")
                    number = driver.find_element_by_css_selector(css_selector_number.format(i)).get_attribute("data-title")
                    major_number = major + "  " + number
                    major_list.append(major_number)
                except Exception as e:
                    print(e)
            driver.find_element_by_css_selector("#goPageNo").send_keys(str(flag))  # 输入页码跳转
            driver.find_element_by_xpath("//input[@class='page-btn']").click()  # 点击 Go，仍然同是一个 window_handle
            pagenumber -= 1
            flag +=1

    print(len(major_list))
    # print(major_list)
    return major_list


def merge_data(school_name_list, all_major_list):
    # dictionary = dict(zip(school_list, major_list))

    dictionary = {}
    for j in range(0,len(school_name_list)):
        for i in range(0,len(all_major_list)):
            print(school_name_list[j])
            dictionary.setdefault(school_name_list[j],[]).append(all_major_list[i])
    print(dictionary)


def main():
    # driver = set_driver()
    # driver = select_major(driver)
    # school_name_list, all_major_list = get_school_name(driver)
    school_name_list = ['(10001)北京大学     (11)北京市', '(10001)清华大学     (11)北京市']
    all_major_list = [['(00)不区分研究方向  专业：3(不含推免)', '(01)软件工程  专业：390(不含推免)'], ['(02)网络安全  专业：390(不含推免)', '(03)智能科技  专业：390(不含推免)']]
    merge_data(school_name_list, all_major_list)

if __name__ == '__main__':
    main()
