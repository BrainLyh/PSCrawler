#!/usr/bin/env python
# encoding: utf-8
'''
@author: Brian
@file: RDsBySchoolName.py
@time: 2020/7/1 14:20
@desc: 通过学校名字来获得相关信息
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from pyecharts.charts import Line
from pyecharts.charts import Bar
from pyecharts import options as opts
import re


class RDsBySchoolName(object):

    def __init__(self, url, schoolname, yjxkdm):
        self.url = url
        self.schoolname = schoolname
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
        else:
            pagenumber = int(li[-3].text)
        # print("当前页面页数：" + str(pagenumber))
        return pagenumber

    # 通过学校名与专业选择学校
    def select_school(self, driver,):
        # 专业列表,研究方向数量列表，拟招生人数列表
        label_list = []
        major_number_list = []
        admission_list = []
        original_window = driver.current_window_handle
        flag = True
        try:
            driver.find_element_by_xpath("//input[@id='dwmc']").send_keys(self.schoolname)
            Select(driver.find_element_by_xpath("//select[@id='yjxkdm']")).select_by_value(self.yjxkdm)

            # 找到查询按钮进行点击,进入高校列表界面
            # 点击完还是在一个 tab 里， handle 也一样
            driver.find_element_by_xpath("//input[@name='button']").click()

            school_name = driver.find_element_by_xpath("//tr[1]//td[1]//form[1]//a[1]").get_attribute(
                "textContent")
            print(school_name)

            # 跳转到每个学校对应的研究方向信息页面
            driver.find_element_by_link_text(school_name).click()
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break
            driver = self.set_height_width(driver)

            label_list, major_number_list, admission_list = self.get_major_list(driver)

        except:
            flag = False
            print("选择条件出现错误，请检查学校名称与学科类别代码是否正确，或是该院校未开设该专业！程序即将退出...")

        driver.close()
        driver.quit()
        return label_list, major_number_list, admission_list, flag

    def get_major_list(self, driver):
        major_number_list = []
        admission_list = []
        label_list = []
        value_list = []

        ul = driver.find_element_by_xpath("//ul[@class='zsml-zy-filter']")
        li = ul.find_elements_by_xpath("li")
        print("当前院校专业数量：" + str(len(li)))

        input_selector = "/html[1]/body[1]/div[2]/div[3]/div[1]/div[2]/div[2]/form[1]/ul[1]/li[{}]/input[1]"
        label_selector = "/html[1]/body[1]/div[2]/div[3]/div[1]/div[2]/div[2]/form[1]/ul[1]/li[{}]/label[1]"
        for check_box in range(1, len(li)+1):
            try:
                value = driver.find_element_by_xpath(input_selector.format(check_box)).get_attribute("value")
                label = driver.find_element_by_xpath(label_selector.format(check_box)).get_attribute("textContent")
                driver.find_element_by_xpath(input_selector.format(check_box)).click()
                driver.find_element_by_xpath("//input[@class='blue-btn-s']").click()
                label_list.append(label)
                value_list.append(value)

                # 得到每个专业下的研究方向数量与拟招生人数
                majors, all_number = self.get_major_info(driver)
                major_number_list.append(majors)
                admission_list.append(all_number)

                print(" 当前专业：" + label)
                print(" 研究方向数量： " + str(majors), "拟招生人数： " + str(all_number))
                # 两次点击取消选择
                driver.find_element_by_xpath(input_selector.format(check_box)).click()
                driver.find_element_by_xpath("//input[@class='blue-btn-s']").click()
            except Exception as e:
                print(e)
        print(value_list, label_list)
        print(major_number_list, admission_list)
        return label_list, major_number_list, admission_list

    # 得到研究方向数量与拟招生人数
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

        if (pagenumber == 1):
            # 不用下一页操作
            major = driver.find_elements_by_xpath("//tbody//tr")
            majors += len(major)
            for i in range(1, len(major) + 1):
                try:
                    number = driver.find_element_by_xpath("//tr[{}]//td[7]//a[1]".format(i)).get_attribute("data-title")
                    numbers = re.sub(r"[^0-9]", "", number)
                    all_number += int(numbers)

                except Exception as e:
                    print(e)
        else:
            # 找到下一页按钮
            while (pagenumber):
                try:
                    major = driver.find_elements_by_xpath("//tbody//tr")
                    # print("这一页的研究方向数量" + str(len(major)))
                    majors += len(major)
                    for i in range(1, len(major) + 1):
                        try:
                            number = driver.find_element_by_xpath("//tr[{}]//td[7]//a[1]".format(i)).get_attribute(
                                "data-title")
                            numbers = re.sub(r"[^0-9]", "", number)
                            # print("  拟招生：" + numbers)
                            all_number += int(numbers)
                        except Exception as e:
                            print(e)
                except Exception as e:
                    print(e)
                ul = driver.find_element_by_css_selector(css_selector_jumpto)
                li = ul.find_elements_by_xpath("li")
                li[-1].click()
                pagenumber -= 1

        return majors, all_number

    # 数据可视化
    def stacked_area_chart(self, x_data, y1_data, y2_data, flag):
        schoolname = self.schoolname
        if(flag):
            (
                Bar()
                    .add_xaxis(xaxis_data=x_data)
                    .add_yaxis("专业下研究方向数量", y1_data)
                    .add_yaxis("各专业拟招生人数", y2_data)
                    .set_global_opts(
                    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
                    title_opts=opts.TitleOpts(title=schoolname + "专业信息折线图", subtitle="下属研究方向与拟招生人数"),
                )
                    .render("ReserachDirectionsBySchoolName.html")
            )
            print("绘制成功，请在同级目录下查看 ReserachDirectionsBySchoolName.html 文件！")
        else:
            print("出现错误，停止绘制图表！")
