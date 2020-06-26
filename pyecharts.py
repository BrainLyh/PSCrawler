#!/usr/bin/env python
# encoding: utf-8
'''
@author: Brian
@file: pyecharts.py
@time: 2020/6/26 15:06
@desc: 重新选择爬取方法，更好的为可视化提供数据
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from pyecharts import options as opts
from pyecharts.charts import Map


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
    # print("当前页数：" + str(pagenumber))
    return pagenumber


# 复选框条件选择
def select_option(driver, count):
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

    # 找到查询按钮进行点击
    driver.find_element_by_xpath("//input[@name='button']").click()

    # 点击完还是在一个 tab 里， handle 也一样

    counts = count_city(driver)
    # print("当前城市的学校数量：" + str(counts))
    return counts


# 返回当前所选择城市开设目标专业的高校数量
def count_city(driver):
    pagenumber = paging(driver)
    counts = 0

    if (pagenumber == 1):
        # 不用下一页操作
        numbers = driver.find_elements_by_xpath("//tbody//tr")
        counts = len(numbers)

    elif (pagenumber < 7):
        # 找到下一页按钮
        while (pagenumber):
            numbers = driver.find_elements_by_xpath("//tbody//tr")
            counts += len(numbers)
            ul = driver.find_element_by_xpath("//ul[@class='ch-page']")
            li = ul.find_elements_by_xpath("li")
            li[-1].click()
            pagenumber -= 1
    else:
        # 下一页按钮位置不同,用 Go
        flag = 2  # 下一次要Go的页码

        while (pagenumber):
            numbers = driver.find_elements_by_xpath("//tbody//tr")
            # 定位页码
            counts += len(numbers)
            driver.find_element_by_css_selector("#goPageNo").send_keys(str(flag))  # 输入页码跳转
            driver.find_element_by_xpath("//input[@class='page-btn']").click()  # 点击 Go，仍然同是一个 window_handle
            pagenumber -= 1
            flag += 1

    return counts


# 选择目标专业
def select_major(driver):
    # 记录所有的城市代码
    city_value = []
    # 记录所有城市名字
    city_name = []
    # 城市的高校数量
    school_counts = []
    assert len(driver.window_handles) == 1

    # 选择省市
    options = driver.find_element_by_css_selector("#ssdm")
    option = options.find_elements_by_xpath("option")
    for city in option[1::]:
        city_name.append(city.get_attribute("textContent"))
        city_value.append(city.get_attribute("value"))
    print(city_name, city_value)

    for count in city_value:
        counts = select_option(driver, count)
        school_counts.append(counts)
    print(school_counts)

    driver.close()
    driver.quit()
    return city_name,school_counts


# 数据可视化
def visulize(city_name, school_counts):
    realcity = []
    # 处理城市名，只保留两字或三字名称
    for citys in city_name:
        if "黑龙江" in citys:
            a = "黑龙江"
        elif "内蒙古" in citys:
            a = "内蒙古"
        else:
            a = citys[4:6]
        realcity.append(a)
    # print(realcity)
    # 将数据处理成列表
    list1 = [[realcity[i], school_counts[i]] for i in range(len(realcity))]
    print(list1)

    map_1 = Map()
    map_1.set_global_opts(
        title_opts=opts.TitleOpts(title="2020高校分布"),
        visualmap_opts=opts.VisualMapOpts(max_=40)  # 最大数据范围
    )
    map_1.add("020高校分布", list1, maptype="china")
    map_1.render('map1.html')


def main():
    driver = set_driver("https://yz.chsi.com.cn/zsml/queryAction.do")
    city_name, school_counts = select_major(driver)
    visulize(city_name, school_counts)


if __name__ == '__main__':
    main()