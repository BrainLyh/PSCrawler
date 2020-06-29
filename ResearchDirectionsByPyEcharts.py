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
        driver.close()
        driver.quit()
        # print(school_list, major_numbers_list, number_list)
        # ['黑龙江大学', '哈尔滨工业大学', '哈尔滨理工大学', '哈尔滨工程大学', '黑龙江科技大学', '东北石油大学', '黑龙江八一农垦大学', '东北林业大学', '哈尔滨师范大学', '齐齐哈尔大学']
        #  [8, 21, 15, 59, 6, 10, 2, 3, 10, 6]
        #  [78, 1549, 123, 201, 153, 149, 331, 221, 115, 520]
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
            print("绘制成功，请在同级目录下查看！")
        else:
            print("出现错误，停止绘制图表！")


def main():

    print(""
          
          """
    城市代码：
        ['(11)北京市', '(12)天津市', '(13)河北省', '(14)山西省', '(15)内蒙古自治区', '(21)辽宁省', '(22)吉林省', 
        '(23)黑龙江省', '(31)上海市', '(32)江苏省', '(33)浙江省', '(34)安徽省', '(35)福建省', '(36)江西省', '
        (37)山东省', '(41)河南省', '(42)湖北省', '(43)湖南省', '(44)广东省', '(45)广西壮族自治区', '(46)海南省', 
        '(50)重庆市', '(51)四川省', '(52)贵州省', '(53)云南省', '(54)西藏自治区', '(61)陕西省', '(62)甘肃省', 
        '(63)青海省', '(64)宁夏回族自治区', '(65)新疆维吾尔自治区']
    
    门类类别：
        专业学位：
        (zyxw)专业学位
        ['(0251)金融', '(0252)应用统计', '(0253)税务', '(0254)国际商务', '(0255)保险', '(0256)资产评估',
                  '(0257)审计', '(0351)法律', '(0352)社会工作', '(0353)警务', '(0451)教育', '(0452)体育',
                  '(0453)汉语国际教育', '(0454)应用心理', '(0551)翻译', '(0552)新闻与传播', '(0553)出版',
                  '(0651)文物与博物馆', '(0851)建筑学', '(0853)城市规划', '(0854)电子信息', '(0855)机械',
                  '(0856)材料与化工', '(0857)资源与环境', '(0858)能源动力', '(0859)土木水利', '(0860)生物与医药',
                  '(0861)交通运输', '(0951)农业', '(0952)兽医', '(0953)风景园林', '(0954)林业', '(1051)临床医学',
                  '(1052)口腔医学', '(1053)公共卫生', '(1054)护理', '(1055)药学', '(1056)中药学', '(1057)中医',
                  '(1151)军事', '(1251)工商管理', '(1252)公共管理', '(1253)会计', '(1254)旅游管理', '(1255)图书情报',
                  '(1256)工程管理', '(1351)艺术']
        学术学位：
        (01)哲学
        ['(0101)哲学']
    
        (02)经济学
        ['(0201)理论经济学', '(0202)应用经济学', '(0270)统计学']
    
        (03)法学
        ['(0301)法学', '(0302)政治学', '(0303)社会学', '(0304)民族学', '(0305)马克思主义理论', '(0306)公安学']
    
        (04)教育学
        ['(0401)教育学', '(0402)心理学', '(0403)体育学', '(0471)']
    
        (05)文学
        ['(0501)中国语言文学', '(0502)外国语言文学', '(0503)新闻传播学']
    
        (06)历史学
        ['(0601)考古学', '(0602)中国史', '(0603)世界史']
    
        (07)理学
        ['(0701)数学', '(0702)物理学', '(0703)化学', '(0704)天文学', '(0705)地理学', '(0706)大气科学', '(0707)海洋科学',
         '(0708)地球物理学', '(0709)地质学', '(0710)生物学', '(0711)系统科学', '(0712)科学技术史', '(0713)生态学', '
         (0714)统计学', '(0771)心理学', '(0772)力学', '(0773)材料科学与工程', '(0774)电子科学与技术', '(0775)计算机科学与技术',
         '(0776)环境科学与工程', '(0777)生物医学工程', '(0778)基础医学', '(0779)公共卫生与预防医学', '(0780)药学',
         '(0781)中药学', '(0782)医学技术', '(0783)护理学', '(0784)', '(0785)', '(0786)']
    
        (08)工学
        ['(0801)力学', '(0802)机械工程', '(0803)光学工程', '(0804)仪器科学与技术', '(0805)材料科学与工程', '(0806)冶金工程',
        '(0807)动力工程及工程热物理', '(0808)电气工程', '(0809)电子科学与技术', '(0810)信息与通信工程', '(0811)控制科学与工程',
        '(0812)计算机科学与技术', '(0813)建筑学', '(0814)土木工程', '(0815)水利工程', '(0816)测绘科学与技术',
        '(0817)化学工程与技术', '(0818)地质资源与地质工程', '(0819)矿业工程', '(0820)石油与天然气工程', '(0821)纺织科学与工程',
        '(0822)轻工技术与工程', '(0823)交通运输工程', '(0824)船舶与海洋工程', '(0825)航空宇航科学与技术', '(0826)兵器科学与技术',
        '(0827)核科学与技术', '(0828)农业工程', '(0829)林业工程', '(0830)环境科学与工程', '(0831)生物医学工程',
        '(0832)食品科学与工程', '(0833)城乡规划学', '(0834)风景园林学', '(0835)软件工程', '(0836)生物工程', '(0837)安全科学与工程',
        '(0838)公安技术', '(0839)网络空间安全', '(0870)科学技术史', '(0871)管理科学与工程', '(0872)设计学']
    
        (09)农学
        ['(0901)作物学', '(0902)园艺学', '(0903)农业资源与环境', '(0904)植物保护', '(0905)畜牧学', '(0906)兽医学', '(0907)林学',
        '(0908)水产', '(0909)草学', '(0970)科学技术史', '(0971)环境科学与工程', '(0972)食品科学与工程', '(0973)风景园林学']
    
        (10)医学
        ['(1001)基础医学', '(1002)临床医学', '(1003)口腔医学', '(1004)公共卫生与预防医学', '(1005)中医学', '(1006)中西医结合',
        '(1007)药学', '(1008)中药学', '(1009)特种医学', '(1010)医学技术', '(1011)护理学', '(1071)科学技术史', '(1072)生物医学工程',
         '(1073)', '(1074)']
    
        (11)军事学
        ['(1101)军事思想及军事历史', '(1102)战略学', '(1103)战役学', '(1104)战术学', '(1105)军队指挥学', '(1106)军事管理学',
        '(1107)军队政治工作学', '(1108)军事后勤学', '(1109)军事装备学', '(1110)军事训练学']
    
        (12)管理学
        ['(1201)管理科学与工程', '(1202)工商管理', '(1203)农林经济管理', '(1204)公共管理', '(1205)图书情报与档案管理']
    
        (13)艺术学
        ['(1301)艺术学理论', '(1302)音乐与舞蹈学', '(1303)戏剧与影视学', '(1304)美术学', '(1305)设计学']

    """
          "")
    print("请根据上方对应关系输入城市代码、门类类别代码、学科类别代码进行图表生成：".center(50, '-'))
    print("例如:41 zyxw 0854 将会查询 河南省 专业学位 电子信息 的相关信息".center(60, '-'))

    url = "https://yz.chsi.com.cn/zsml/queryAction.do"
    count = str(input("请输入城市代码： "))
    mldm = str(input("请输入门类类别代码： "))
    yjxkdm = str(input("请输入学科类别代码： "))
    researdirection = ReserachDirections(url, count, mldm, yjxkdm)
    driver = researdirection.set_driver()

    x, y1,y2,flag = researdirection.select_option(driver)

    researdirection.stacked_area_chart(x, y1, y2, flag)


if __name__ == '__main__':
    main()