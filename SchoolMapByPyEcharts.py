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


class SchoolMap(object):

    def __init__(self, url, mldm, yjxkdm):
        self.url = url
        self.mldm = mldm
        self.yjxkdm = yjxkdm
        self.flagofProcess = True


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
        # print("当前页数：" + str(pagenumber))
        return pagenumber


    # 复选框条件选择，通过城市，门类、学科类别来区分
    def select_option(self, driver, count):
        # https://selenium-python-zh.readthedocs.io/en/latest/api.html
        # 使用 Select 处理下拉框的选项
        # 先通过 Xpath 找到 select 标签，然后通过 value 找到对应值即可选择
        try:
            # print("当前正在选择的城市代码为： " + count)
            Select(driver.find_element_by_xpath("//select[@id='ssdm']")).select_by_value(count)
            Select(driver.find_element_by_xpath("//select[@id='mldm']")).select_by_value(self.mldm)
            Select(driver.find_element_by_xpath("//select[@id='yjxkdm']")).select_by_value(self.yjxkdm)

            # 找到查询按钮进行点击
            driver.find_element_by_xpath("//input[@name='button']").click()

            # 点击完还是在一个 tab 里， handle 也一样
            # 条件选择完之后开始统计数量
            counts = self.count_city(driver)
        except:
            print("选择条件出现错误，请检查门类代码与学科类别代码对应关系是否正确！程序即将退出...".rjust(50, '*'))
        # print("当前城市的学校数量：" + str(counts))
        return counts


    # 返回当前所选择城市开设目标专业的高校数量
    def count_city(self, driver):
        pagenumber = self.paging(driver)
        counts = 0
        self.flagofProcess = True

        if (pagenumber == 1):
            try:
                # 不用下一页操作
                numbers = driver.find_elements_by_xpath("//tbody//tr")
                counts = len(numbers)
            except:
                self.flagofProcess = False
                print("查找失败，请检查当前页面是否为空！")

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


    # 返回所有城市代码，然后遍历城市，得到高校数量
    def select_major(self, driver):
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

        # 遍历城市代码，传入统计高校数量的函数
        for count in city_value:
            counts = self.select_option(driver, count)
            school_counts.append(counts)
        print(school_counts)

        driver.close()
        driver.quit()
        return city_name, school_counts


    # 数据可视化
    def visulize(self, city_name, school_counts):
        if(self.flagofProcess):
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
            map_1.add("2020高校分布", list1, maptype="china")
            map_1.render('SchoolMap.html')
            print("绘制成功，请在同级目录下查看！")
        else:
            print("出现错误，停止绘制图表！")


def main():
    print(""

          """
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
    print("请根据上方对应关系输入门类类别代码、学科类别代码进行图表生成：".center(50, '-'))
    print("例如:zyxw 0854 将会绘制开设 专业学位 电子信息 的高校在全国的分布信息".center(60, '-'))
    mldm = str(input("请输入门类类别代码： "))
    yjxkdm = str(input("请输入学科类别代码： "))
    url = "https://yz.chsi.com.cn/zsml/queryAction.do"

    school_map = SchoolMap(url, mldm, yjxkdm)
    driver = school_map.set_driver()
    city_name, school_counts = school_map.select_major(driver)

    school_map.visulize(city_name, school_counts)


if __name__ == '__main__':
    main()