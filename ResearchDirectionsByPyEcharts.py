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
from pyecharts.charts import Line
from pyecharts import options as opts
import re


class ReserachDirections(object):

    def __init__(self, url, count, mldm, yjxkdm):
        self.url = url
        self.count = count
        self.mldm = mldm
        self.yjxkdm = yjxkdm

    # 配置 driver
    def set_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(executable_path="E:/Program Files/chromedriver_win32/chromedriver.exe",
                                  chrome_options=chrome_options)
        driver.get(self.url)
        driver = self.set_height_width(driver)

        return driver

    # 将设置屏幕大小独立出来，方便每次跳转完使用
    def set_height_width(self, driver):
        width = driver.execute_script("return document.documentElement.scrollWidth")
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.set_window_size(width, height)
        return driver

    # 如果需要翻页就翻页
    def paging(self, driver):
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

    # 获得当前条件下的所有高校名称,返回名称列表
    def get_school_name(self, driver):
        pagenumber = self.paging(driver)
        name_list = []
        major_numbers_list = []
        number_list = []
        original_window = driver.current_window_handle
        flag = True

        if (pagenumber == 1):
            numbers = driver.find_elements_by_xpath("//tbody//tr")
            for line in range(1, len(numbers)+1):
                try:
                    school_name = driver.find_element_by_xpath("//tr[{}]//td[1]//form[1]//a[1]".format(line)).get_attribute("textContent")
                    print(school_name)
                    name_list.append(school_name)

                    # 跳转到每个学校对应的研究方向信息页面
                    driver.find_element_by_link_text(school_name).click()
                    for window_handle in driver.window_handles:
                        if window_handle != original_window:
                            driver.switch_to.window(window_handle)
                            break
                    driver = self.set_height_width(driver)

                    # 得到该学校各个研究方向的列表
                    major_list ,number = self.get_major_info(driver)
                    major_numbers_list.append(major_list)
                    number_list.append(number)

                    # 关闭信息页面，转到学校列表页面
                    driver.close()
                    driver.switch_to.window(original_window)
                    driver = self.set_height_width(driver)
                except:
                    flag = False
                    print("查找失败，请检查当前页面是否为空！")

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
                    driver = self.set_height_width(driver)

                    # 得到该学校各个研究方向的列表
                    major_list, number = self.get_major_info(driver)
                    major_numbers_list.append(major_list)
                    number_list.append(number)

                    # 关闭信息页面，转到学校列表页面
                    driver.close()
                    driver.switch_to.window(original_window)
                    driver = self.set_height_width(driver)

                ul = driver.find_element_by_xpath("//ul[@class='ch-page']")
                li = ul.find_elements_by_xpath("li")
                li[-1].click()
                pagenumber -= 1

        # print(name_list)
        return name_list, major_numbers_list, number_list, flag


    # 获得某个院校在目标专业下的研究方向的数量，返回数量列表
    def get_major_info(self, driver):
        # 当前 Tab 里有多少个页面
        pagenumber = self.paging(driver)
        majors = 0
        all_number = 0
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
            for i in range(1, len(major) + 1):
                try:
                    number = driver.find_element_by_xpath("//tr[{}]//td[7]//a[1]".format(i)).get_attribute("data-title")
                    numbers = re.sub(r"[^0-9]", "", number)
                    all_number += int(numbers)
                    print("  拟招生：" + numbers)

                except Exception as e:
                    print(e)

        elif(pagenumber < 7 ):
            # 找到下一页按钮
            while(pagenumber):
                try:
                    major = driver.find_elements_by_xpath("//tbody//tr")
                    print("这一页的专业数量" + str(len(major)))
                    majors += len(major)
                    for i in range(1, len(major) + 1):
                        try:
                            number = driver.find_element_by_xpath("//tr[{}]//td[7]//a[1]".format(i)).get_attribute(
                                "data-title")
                            numbers = re.sub(r"[^0-9]", "", number)
                            print("  拟招生：" + numbers)
                            all_number += int(numbers)
                        except Exception as e:
                            print(e)
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
        print("  共招生: " + str(all_number))

        return majors, all_number

    # 复选框条件选择，选择城市、门类、学科类别
    def select_option(self, driver):

        school_list = []
        flag = True
        list_211 = ['清华大学', '北京大学', '中国人民大学', '北京工业大学', '北京理工大学', '北京航空航天大学', '北京化工大学',
                    '北京邮电大学', '对外经济贸易大学', '中国传媒大学', '中央民族大学', '中国矿业大学', '中央财经大学',
                    '中国政法大学', '中央音乐学院', '北京体育大学', '北京外国语大学', '北京交通大学', '北京科技大学',
                    '北京林业大学', '中国农业大学', '北京中医药大学', '华北电力大学', '北京师范大学', '中国地质大学',
                    '复旦大学', '华东师范大学', '上海外国语大学', '上海大学', '同济大学', '华东理工大学', '东华大学',
                    '上海财经大学', '上海交通大学', '南开大学', '天津大学', '天津医科大学', '河北工业大学', '重庆大学',
                    '西南大学', '太原理工大学', '内蒙古大学', '大连理工大学', '东北大学', '辽宁大学', '大连海事大学',
                    '吉林大学', '东北师范大学', '延边大学', '东北农业大学', '东北林业大学', '哈尔滨工业大学', '哈尔滨工程大学',
                    '南京大学', '东南大学', '苏州大学', '河海大学', '中国药科大学', '南京师范大学', '南京理工大学',
                    '南京航空航天大学', '江南大学', '南京农业大学', '浙江大学', '安徽大学', '合肥工业大学', '中国科学技术大学',
                    '厦门大学', '福州大学', '南昌大学', '山东大学', '中国海洋大学', '中国石油大学', '郑州大学', '武汉大学',
                    '华中科技大学', '华中师范大学', '华中农业大学', '中南财经政法大学', '武汉理工大学', '湖南大学', '中南大学',
                    '湖南师范大学', '中山大学', '暨南大学', '华南理工大学', '华南师范大学', '广西大学', '四川大学', '西南交通大学',
                    '电子科技大学', '西南财经大学', '四川农业大学', '云南大学', '贵州大学', '西北大学', '西安交通大学',
                    '西北工业大学', '陕西师范大学', '西北农林科大', '西安电子科技大学', '长安大学', '兰州大学', '新疆大学',
                    '石河子大学', '海南大学', '宁夏大学', '青海大学', '西藏大学', '第二军医大学', '第四军医大学', '国防科学技术大学']

        # https://selenium-python-zh.readthedocs.io/en/latest/api.html
        # 使用 Select 处理下拉框的选项
        # 先通过 Xpath 找到 select 标签，然后通过 value 找到对应值即可选择
        try:
            # print("当前正在选择的城市代码为： " + self.count)
            Select(driver.find_element_by_xpath("//select[@id='ssdm']")).select_by_value(self.count)
            Select(driver.find_element_by_xpath("//select[@id='mldm']")).select_by_value(self.mldm)
            Select(driver.find_element_by_xpath("//select[@id='yjxkdm']")).select_by_value(self.yjxkdm)

            # 找到查询按钮进行点击,进入高校列表界面
            # 点击完还是在一个 tab 里， handle 也一样
            driver.find_element_by_xpath("//input[@name='button']").click()
            self.set_height_width(driver)

            # 得到高校列表
            school_name_list, major_numbers_list, number_list, flag= self.get_school_name(driver)

            for school in school_name_list:
                school = school[7::]
                school_list.append(school)
        except:
            print("选择条件出现错误，请检查门类代码与学科类别代码对应关系是否正确！程序即将退出...".rjust(50, '*'))

        empty = []
        for i in school_list:
            for j in list_211:
                if i == j:

                    empty.append(i)
                    break
        print("当前条件下，985&211 院校有：")
        print(empty)

        driver.close()
        driver.quit()
        # print(school_list, major_numbers_list, number_list)
        # ['黑龙江大学', '哈尔滨工业大学', '哈尔滨理工大学', '哈尔滨工程大学', '黑龙江科技大学', '东北石油大学', '黑龙江八一农垦大学', '东北林业大学', '哈尔滨师范大学', '齐齐哈尔大学']
        #  [8, 21, 15, 59, 6, 10, 2, 3, 10, 6]
        #  [78, 1549, 123, 201, 153, 149, 331, 221, 115, 520]

        print("正在准备绘制图表...")
        return school_name_list, major_numbers_list, number_list, flag

    def stacked_area_chart(self, x_data, y1_data, y2_data, flag):

        if(flag):
            (
                Line()
                    .add_xaxis(xaxis_data=x_data)
                    .add_yaxis(
                    series_name="研究方向数量",
                    stack="总量",
                    y_axis=y1_data,
                    areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
                    label_opts=opts.LabelOpts(is_show=False),
                )
                    .add_yaxis(
                    series_name="拟招生人数",
                    stack="总量",
                    y_axis=y2_data,
                    areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
                    label_opts=opts.LabelOpts(is_show=False),
                )

                    .set_global_opts(
                    title_opts=opts.TitleOpts(title="高校研究方向折线图"),
                    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                    yaxis_opts=opts.AxisOpts(
                        type_="value",
                        axistick_opts=opts.AxisTickOpts(is_show=True),
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    ),

                    xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False, name_rotate=60, name_gap=20),
                )
                    .render("ReserachDirections.html")
            )
            print("绘制成功，请在同级目录下查看 ReserachDirections.html 文件！")
        else:
            print("出现错误，停止绘制图表！")
