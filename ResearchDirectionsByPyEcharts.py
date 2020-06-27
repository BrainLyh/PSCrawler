#!/usr/bin/env python
# encoding: utf-8
'''
@author: Brian
@file: ResearchDirectionsByPyEcharts.py
@time: 2020/6/27 15:38
@desc: 对每个城市的高校开设的研究方向进行处理
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

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
    ul = driver.find_element_by_xpath("//ul[@class='ch-page']")
    li = ul.find_elements_by_xpath("li")
    # print("当前页面翻页元素长度：" + str(len(li)))
    # 第一页右下角的标签数量最大为10，小于10时没有 Go 输入跳转框
    if(len(li) < 10):
        pagenumber = int(li[-2].text)
    # print(pagenumber)
    else:
        pagenumber = int(li[-3].text)
    print("当前页数：" + str(pagenumber))
    return pagenumber


# 复选框条件选择，选择城市、门类、学科类别
def select_option(driver, count):
    school_list = []
    # https://selenium-python-zh.readthedocs.io/en/latest/api.html
    # 使用 Select 处理下拉框的选项
    # 先通过 Xpath 找到 select 标签，然后通过 value 找到对应值即可选择
    try:
        # print("当前正在选择的城市代码为： " + count)
        Select(driver.find_element_by_xpath("//select[@id='ssdm']")).select_by_value(count)
        Select(driver.find_element_by_xpath("//select[@id='mldm']")).select_by_value('zyxw')
        Select(driver.find_element_by_xpath("//select[@id='yjxkdm']")).select_by_value("0854")
    except Exception as e:
        print("选择城市时出现错误：" + e)

    # 找到查询按钮进行点击,进入高校列表界面
    # 点击完还是在一个 tab 里， handle 也一样
    driver.find_element_by_xpath("//input[@name='button']").click()
    set_height_width(driver)

    # 得到高校列表
    school_name_list, major_numbers_list = get_school_name(driver)

    for school in school_name_list:
        school = school[7::]
        school_list.append(school)
    driver.close()
    driver.quit()
    print(school_list, major_numbers_list)
    # ['黑龙江大学', '哈尔滨工业大学', '哈尔滨理工大学', '哈尔滨工程大学', '黑龙江科技大学', '东北石油大学', '黑龙江八一农垦大学', '东北林业大学', '哈尔滨师范大学', '齐齐哈尔大学']
    #  [8, 21, 15, 59, 6, 10, 2, 3, 10, 6]
    # return school_name_list, major_numbers_list


# 获得当前条件下的所有高校名称,返回名称列表
def get_school_name(driver):
    pagenumber = paging(driver)
    name_list = []
    major_numbers_list = []
    original_window = driver.current_window_handle

    if (pagenumber == 1):
        numbers = driver.find_elements_by_xpath("//tbody//tr")
        for line in range(1, len(numbers)+1):
            school_name = driver.find_element_by_xpath("//tr[{}]//td[1]//form[1]//a[1]".format(line)).get_attribute("textContent")
            print(school_name)
            name_list.append(school_name)

            # 跳转到每个学校对应的研究方向信息页面
            driver.find_element_by_link_text(school_name).click()
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break
            driver = set_height_width(driver)

            # 得到该学校各个研究方向的列表
            major_list = get_major_info(driver)
            major_numbers_list.append(major_list)

            # 关闭信息页面，转到学校列表页面
            driver.close()
            driver.switch_to.window(original_window)
            driver = set_height_width(driver)
    elif (pagenumber < 7):
        while (pagenumber):
            numbers = driver.find_elements_by_xpath("//tbody//tr")
            for line in range(1, len(numbers)+1):
                school_name = driver.find_element_by_xpath("//tr[{}]//td[1]//form[1]//a[1]".format(line)).get_attribute("textContent")
                name_list.append(school_name)
                print(school_name)

                # 跳转到每个学校对应的研究方向信息页面
                driver.find_element_by_link_text(school_name).click()
                for window_handle in driver.window_handles:
                    if window_handle != original_window:
                        driver.switch_to.window(window_handle)
                        break
                driver = set_height_width(driver)

                # 得到该学校各个研究方向的列表
                major_list = get_major_info(driver)
                major_numbers_list.append(major_list)

                # 关闭信息页面，转到学校列表页面
                driver.close()
                driver.switch_to.window(original_window)
                driver = set_height_width(driver)

            ul = driver.find_element_by_xpath("//ul[@class='ch-page']")
            li = ul.find_elements_by_xpath("li")
            li[-1].click()
            pagenumber -= 1

    # print(name_list)
    return name_list, major_numbers_list


# 获得某个院校在目标专业下的研究方向的数量，返回数量列表
def get_major_info(driver):
    # 当前 Tab 里有多少个页面
    pagenumber = paging(driver)
    majors = 0
    # 定位跳转
    css_selector_jumpto = "body.ch-sticky:nth-child(2) " \
                          "div.main-wrapper:nth-child(2) " \
                          "div.container.clearfix:nth-child(5) " \
                          "div.zsml-row.clearfix " \
                          "div.zsml-page-box ul.ch-page "
    if(pagenumber == 1):
        # 不用下一页操作
        major = driver.find_elements_by_xpath("//tbody//tr")
        print("这一页的专业数量" + str(len(major)))
        majors += len(major)

    elif(pagenumber < 7 ):
        # 找到下一页按钮
        while(pagenumber):
            try:
                major = driver.find_elements_by_xpath("//tbody//tr")
                print("这一页的专业数量" + str(len(major)))
                majors += len(major)
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
            try:
                major = driver.find_elements_by_xpath("//tbody//tr")
                print("这一页的专业数量" + str(len(major)))
                majors += len(major)
            except Exception as e:
                print(e)
            driver.find_element_by_css_selector("#goPageNo").send_keys(str(flag))  # 输入页码跳转
            driver.find_element_by_xpath("//input[@class='page-btn']").click()  # 点击 Go，仍然同是一个 window_handle
            pagenumber -= 1
            flag +=1

    # print(len(major_list))
    print("专业数量： " + str(majors))

    return majors


def main():
    url = "https://yz.chsi.com.cn/zsml/queryAction.do"
    driver = set_driver(url)
    count = '23'
    select_option(driver, count)


if __name__ == '__main__':
    main()