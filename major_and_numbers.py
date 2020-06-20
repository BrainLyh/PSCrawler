#!/usr/bin/env python
# encoding: utf-8
'''
@author: Brian
@file: major_and_numbers.py
@time: 2020/6/18 10:06
@desc: 在之前爬取的院校列表基础上，对每个学校该专业研究方向，拟招收人数进行爬取
'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import datetime


# 配置 driver
def set_driver(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(executable_path="E:/Program Files/chromedriver_win32/chromedriver.exe",
                              chrome_options=chrome_options)
    driver.get(url)
    driver = set_height_width(driver)

    return driver


# 将设置屏幕大小独立出来，方便每次跳转完使用
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
    # print(len(li))
    # 第一页右下角的标签数量最大为10，小于10时没有 Go 输入跳转框
    if(len(li) < 10):
        pagenumber = int(li[-2].text)
    # print(pagenumber)
    else:
        pagenumber = int(li[-3].text)
    return pagenumber


# 选择目标专业
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

    # 找到查询按钮进行点击
    driver.find_element_by_xpath("//input[@name='button']").click()

    # 等待时间过长，超时
    # wait.until(EC.number_of_windows_to_be(2))

    # 判断当前页面
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
    # 成功跳转到目标网页
    driver = set_height_width(driver)
    return driver


# 获得所有院校列表
def get_school_name(driver):
    # 记录院校列表页面的 handle
    original_window = driver.current_window_handle
    school_name_list = []
    major_list = []
    # 定位学校名称、所在城市、页面数量
    css_selector_schoolname = "body.ch-sticky:nth-child(2) " \
                              "div.main-wrapper:nth-child(2) " \
                              "div.container.clearfix:nth-child(4) " \
                              "div.zsml-row.clearfix " \
                              "div.zsml-list-box table.ch-table " \
                              "tbody:nth-child(2) " \
                              "tr:nth-child({}) " \
                              "td:nth-child(1) " \
                              "form:nth-child(1) > a:nth-child(1)"
    css_selector_cityname = "body.ch-sticky:nth-child(2) " \
                            "div.main-wrapper:nth-child(2) " \
                            "div.container.clearfix:nth-child(4) " \
                            "div.zsml-row.clearfix div.zsml-list-box " \
                            "table.ch-table " \
                            "tbody:nth-child(2) " \
                            "tr:nth-child({}) > td:nth-child(2)"
    css_selector_pagenumbers = "body.ch-sticky:nth-child(2) " \
                               "div.main-wrapper:nth-child(2) " \
                               "div.container.clearfix:nth-child(4) " \
                               "div.zsml-row.clearfix " \
                               "div.zsml-page-box ul.ch-page li.lip:nth-child(8) > a:nth-child(1)"
    # 翻页数
    number = driver.find_element_by_css_selector(css_selector_pagenumbers).get_attribute("textContent")

    # 下一页的页码
    flag = 2
    while (flag <= int(number) + 1):
        for i in range(1, 32):
            if i == 31:
                try:
                    driver.find_element_by_css_selector("#goPageNo").send_keys(str(flag))  # 输入页码跳转
                    driver.find_element_by_xpath("//input[@class='page-btn']").click()  # 点击 Go，仍然同是一个 window_handle
                    flag += 1
                except:
                    print("已经是最后一页啦".center(100, "-"))
                break
            else:
                try:
                    school_name = driver.find_element_by_css_selector(css_selector_schoolname.format(i)).get_attribute(
                        "textContent")
                    city_name = driver.find_element_by_css_selector(css_selector_cityname.format(i)).get_attribute("textContent")

                    # 跳转到每个学校对应的研究方向信息页面
                    driver.find_element_by_link_text(school_name).click()
                    for window_handle in driver.window_handles:
                        if window_handle != original_window:
                            driver.switch_to.window(window_handle)
                            break
                    driver = set_height_width(driver)

                    # 得到该学校各个研究方向的列表
                    major_list = get_major_info(driver)
                    major_list.insert(0, school_name)

                    print(major_list)

                    # 关闭信息页面，转到学校列表页面
                    driver.close()
                    driver.switch_to.window(original_window)
                    driver = set_height_width(driver)

                    school_and_city = school_name + "     " + city_name
                    school_name_list.append(school_and_city)
                    # print(school_name_list)

                except Exception as e:
                    print(e)
                    # print("全部学校爬取完毕！".center(100, "-"))

    print(school_name_list)
    save_data(school_name_list)
    # 结果如下
    # ['(10002)中国人民大学', '(01)不区分研究方向  专业：17(不含推免)', '(02)不区分研究方向  专业：44(不含推免)']
    driver.close()
    driver.quit()
    # return


# 获得院校在目标专业下的研究方向等信息
def get_major_info(driver):
    # 当前页面有多少条数据
    major_list = []
    # 当前 Tab 里有多少个页面
    pagenumber = paging(driver)
    # print(pagenumber)

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
            # 定位页码
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

    # print(len(major_list))
    # print(major_list)

    return major_list

# 保存数据
def save_data(data_list):
    with open("../major_info.txt", "w") as f:
        for line in data_list:
            f.write(line + "\r")


def main():
    url = "https://yz.chsi.com.cn/zsml/zyfx_search.jsp"
    begin_time = datetime.datetime.now()
    driver = set_driver(url)
    driver = select_major(driver)
    get_school_name(driver)
    end_time = datetime.datetime.now()
    spend_time = end_time - begin_time
    print("共花费：" + str(spend_time.seconds) + "s")


if __name__ == '__main__':
    main()
