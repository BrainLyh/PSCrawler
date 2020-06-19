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
    url = "https://yz.chsi.com.cn/zsml/querySchAction.do?ssdm=11&dwmc=%E5%8C%97%E4%BA%AC%E9%82%AE%E7%94%B5%E5%A4%A7%E5%AD%A6" \
          "&mldm=zyxw&mlmc=&yjxkdm=0854&xxfs=&zymc="
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
    major_list = []
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
    school_and_city = school_name + "     " + city_name
    school_name_list.append(school_and_city)

    driver.close()
    driver.switch_to.window(original_window)
    driver = set_height_width(driver)
    # print("跳转结束" + driver.current_window_handle)
    # driver.save_screenshot("跳转结束.jpg")
    print(school_name_list)
    print(major_list)

    driver.close()
    driver.quit()


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
    print(major_list)
    # return major_list


def main():
    driver = set_driver()
    get_major(driver)
"['(01)Web多媒体搜索与挖掘，网络智能信息处理  专业：203(不含推免)', '(02)未来通信与网络、智能信息处理与智能医疗  专业：203(不含推免)', '(03)宽带无线移动通信系统理论、技术及应用  专业：203(不含推免)', '(04)先进网络信息处理、空间通信与智能数据融合  专业：203(不含推免)', '(05)宽带无线移动通信、下一代网络及信息处理  专业：203(不含推免)', '(06)未来网络架构、软件定义网络、网络人工智能  专业：203(不含推免)', '(07)智能数据科学与应用  专业：203(不含推免)', '(08)宽带协同融合网络与智能安全控管技术  专业：203(不含推免)', '(09)无线大数据与泛在智能系统  专业：203(不含推免)', '(10)大数据、物联网、网络安全应用  专业：203(不含推免)', '(11)智慧5G、物联网和智能服务开发  专业：203(不含推免)', '(12)移动通信与网络大数据，视频智能计算及应用  专业：203(不含推免)', '(13)移动通信  专业：203(不含推免)', '(14)物联网智能应用及机器学习  专业：203(不含推免)', '(15)无线大数据、边缘计算系统和平台研发、天地一体化信息网络研发  专业：203(不含推免)', '(16)物联网与人工智能  专业：203(不含推免)', '(17)机器认知与智能视觉，数字广播  专业：203(不含推免)', '(18)宽带移动通信与物联网应用  专业：203(不含推免)', '(19)未来移动通信、机器学习与网络多媒体  专业：203(不含推免)', '(20)未来移动通信技术、智能计算与智慧物联网  专业：203(不含推免)', '(21)计算机视觉与图像识别  专业：203(不含推免)', '(22)物联网、区块链、频谱工程、人工智能  专业：203(不含推免)', '(23)物联网、移动互联网与人工智能技术  专业：203(不含推免)', '(24)信息系统与人工智能  专业：203(不含推免)', '(25)工业互联网、大数据分析及应用  专业：203(不含推免)', '(26)无线大数据与移动互联安全  专业：203(不含推免)', '(27)人工智能与大数据，区块链应用与物联网安全  专业：203(不含推免)', '(28)认知无线电通信工程  专业：203(不含推免)', '(29)车联网、智能医疗及大数据工程  专业：203(不含推免)', '(30)区块链与物联网技术，网络信息智能分析  专业：203(不含推免)', '(31)移动通信系统与移动互联应用技术  专业：203(不含推免)', '(32)人工智能与智能计算、物联网大数据学习  专业：203(不含推免)', '(33)移动物联通信与大数据人工智能应用  专业：203(不含推免)', '(34)智能信息处理、物联网、新无线通信技术  专业：203(不含推免)', '(35)电磁场、计算机视觉、人工智能、信号处理  专业：203(不含推免)', '(36)宽带无线通信与移动互联网  专业：203(不含推免)', '(37)宽带无线通信理论与移动通信新技术  专业：203(不含推免)', '(38)5G后续演进及6G移动通信技术  专业：203(不含推免)', '(39)天地一体化融合网络  专业：203(不含推免)', '(40)数据处理与模式识别  专业：203(不含推免)', '(41)智能信息与通信技术  专业：203(不含推免)', '(42)光纤通信与光传感技术  专业：203(不含推免)', '(43)人工智能与计算机视觉  专业：203(不含推免)', '(44)智能硬件、无线信号处理  专业：203(不含推免)', '(45)时间频率传输技术  专业：203(不含推免)', '(46)无线宽带通信与物联网工程  专业：203(不含推免)', '(47)工业互联网、大数据技术  专业：203(不含推免)', '(48)移动互联网与智能信息处理  专业：203(不含推免)', '(49)智慧网络、智慧城市、智慧能源  专业：203(不含推免)', '(50)大数据智能处理与智慧医疗  专业：203(不含推免)', '(51)云游戏，无线VR，计算机视觉与编码  专业：203(不含推免)', '(52)空天信息工程、智能信号处理  专业：203(不含推免)', '(53)信息论编码与5G移动物联网通信  专业：203(不含推免)', '(54)多媒体信息智能分析与机器学习  专业：203(不含推免)', '(55)无人智能系统宽带移动通信技术  专业：203(不含推免)', '(56)机器学习与信号处理  专业：203(不含推免)', '(57)数字电视  专业：203(不含推免)', '(58)机器视觉图像处理与定位  专业：203(不含推免)', '(59)移动大数据与物联网  专业：203(不含推免)', '(60)人工智能赋能的无线网络优化技术  专业：203(不含推免)', '(61)可信宽带无线通信和物联网  专业：203(不含推免)', '(62)物理层安全技术  专业：203(不含推免)', '(63)智慧城市中的人工智能及物联网应用研究  专业：203(不含推免)', '(64)数据中心网络、大数据与深度学习新技术  专业：203(不含推免)', '(65)移动通信工业物联网  专业：203(不含推免)', '(66)Web多媒体搜索与挖掘，网络智能信息处理  专业：90(不含推免)', '(67)未来通信与网络、智能信息处理与智能医疗  专业：90(不含推免)', '(68)先进网络信息处理、空间通信与智能数据融合  专业：90(不含推免)', '(69)宽带无线移动通信、下一代网络及信息处理  专业：90(不含推免)', '(70)安全通信与大数据  专业：90(不含推免)', '(71)智能数据科学与应用  专业：90(不含推免)', '(72)大数据、物联网、网络安全应用  专业：90(不含推免)', '(73)基于人工智能的5G和物联网应用开发  专业：90(不含推免)', '(74)移动通信与网络大数据，视频智能计算及应用  专业：90(不含推免)', '(75)移动通信  专业：90(不含推免)', '(76)数据分析平台、边缘计算系统研发  专业：90(不含推免)', '(77)物联网与人工智能  专业：90(不含推免)', '(78)机器认知与智能视觉，数字广播  专业：90(不含推免)', '(79)计算机视觉与图像识别  专业：90(不含推免)', '(80)宽带移动通信与物联网应用  专业：90(不含推免)', '(81)未来移动通信、机器学习与网络多媒体  专业：90(不含推免)', '(82)大数据与智能信号处理  专业：90(不含推免)', '(83)未来移动通信技术、智能计算与智慧物联网  专业：90(不含推免)', '(84)物联网、区块链、频谱工程、人工智能  专业：90(不含推免)', '(85)物联网、移动互联网与人工智能技术  专业：90(不含推免)', '(86)工业互联网、大数据分析及应用  专业：90(不含推免)', '(87)信息处理与智能系统  专业：90(不含推免)', '(88)认知无线电通信工程  专业：90(不含推免)', '(89)人工智能与大数据，区块链应用与物联网安全  专业：90(不含推免)', '(90)智能信息处理与智能医疗  专业：90(不含推免)', '(91)移动互联网与大数据分析  专业：90(不含推免)', '(92)智能信息处理、物联网、新无线通信技术  专业：90(不含推免)', '(93)电磁场、计算机视觉、人工智能、信号处理  专业：90(不含推免)', '(94)宽带无线通信与移动互联网  专业：90(不含推免)', '(95)天地一体化网络数字信号处理  专业：90(不含推免)', '(96)数据处理与模式识别  专业：90(不含推免)', '(97)移动互联网与智能信息处理  专业：90(不含推免)', '(98)多媒体信息智能分析与机器学习  专业：90(不含推免)', '(A1)机器视觉图像处理与定位  专业：90(不含推免)', '(A2)智慧城市中的人工智能及物联网应用开发  专业：90(不含推免)', '(A3)5G后续演进及6G移动通信技术  专业：90(不含推免)', '(A4)宽带通信与新型网络  专业：90(不含推免)', '(A5)智能硬件、无线信号处理  专业：90(不含推免)', '(A6)大数据技术  专业：90(不含推免)', '(A7)智慧网络、智慧城市、智慧能源  专业：90(不含推免)', '(A8)视频物联网、高速移动平台组网  专业：90(不含推免)', '(A9)空天信息工程、智能信号处理  专业：90(不含推免)', '(B1)移动物联网通信  专业：90(不含推免)', '(B2)数字电视  专业：90(不含推免)', '(B3)工业互联网网络与大数据分析  专业：90(不含推免)', '(B4)移动大数据与物联网  专业：90(不含推免)', '(B5)数据驱动的无线通信新技术  专业：90(不含推免)', '(B6)物理层攻击识别技术  专业：90(不含推免)', '(B7)交互式无人机器通信与组网技术  专业：90(不含推免)', '(B8)数据中心网络、大数据与深度学习新技术  专业：90(不含推免)', '(B9)移动通信工业物联网  专业：90(不含推免)', '(01)无线通信与智慧微波、物联网与移动互联网  专业：118(不含推免)', '(02)无线通信、光纤通信、卫星与空间通信工程  专业：118(不含推免)', '(03)移动互联网、未来通信与大数据、人工智能  专业：118(不含推免)', '(04)通信电子、卫星导航及多媒体；物联网  专业：118(不含推免)', '(05)卫星移动通信、多媒体与物联网  专业：118(不含推免)', '(06)人工智能与金融  专业：118(不含推免)', '(07)宽带融合网、智能光互联、空天地一体网络  专业：118(不含推免)', '(08)宽带通信  专业：118(不含推免)', '(09)空间光通信和图像处理  专业：118(不含推免)', '(10)宽带通信与人工智能、空天地一体网络  专业：118(不含推免)', '(11)光电器件与集成  专业：118(不含推免)', '(12)宽带通信与光智能信息处理技术  专业：118(不含推免)', '(13)高速融合光通信  专业：118(不含推免)', '(14)宽带光接入与光网络融合技术  专业：118(不含推免)', '(15)移动电子商务、无线通信与物联网、数据挖掘  专业：118(不含推免)', '(16)无线通信  专业：118(不含推免)', '(17)卫星/移动通信、天地一体化网络、物联网  专业：118(不含推免)', '(18)射频天线、太赫兹通信  专业：118(不含推免)', '(19)电磁兼容与信息安全、智慧电子技术与人工智能  专业：118(不含推免)', '(20)宽带通信器件和系统、智能信息处理  专业：118(不含推免)', '(21)无线光通信、微波光子技术  专业：118(不含推免)', '(22)认知无线电、智能信息处理  专业：118(不含推免)', '(23)无线通信理论研究与应用  专业：118(不含推免)', '(24)数据信息处理与智能服务  专业：118(不含推免)', '(25)射频技术、人工智能、雷达信号处理  专业：118(不含推免)', '(26)天线与电波传播  专业：118(不含推免)', '(27)电磁兼容、超宽带无线通信、移动互联网  专业：118(不含推免)', '(28)物联网与大数据  专业：118(不含推免)', '(29)微纳电子技术、智能通信、物联网与大数据  专业：118(不含推免)', '(30)多媒体通信与集成电路技术  专业：118(不含推免)', '(31)光电检测与光通信  专业：118(不含推免)', '(32)图像处理  专业：118(不含推免)', '(33)移动互联网、通信网络及安全  专业：118(不含推免)', '(34)信息物理融合、智能人机交互、移动云计算  专业：118(不含推免)', '(35)柔性可穿戴器件  专业：118(不含推免)', '(36)柔性光电子材料及器件、拓扑光子学  专业：118(不含推免)', '(37)信息材料器件与信息处理  专业：118(不含推免)', '(38)电子信息材料及器件  专业：118(不含推免)', '(39)无线通信与智慧微波、物联网与移动互联网  专业：2(不含推免)', '(40)无线通信、光纤通信、卫星与空间通信工程  专业：2(不含推免)', '(41)移动互联网、未来通信与大数据、人工智能  专业：2(不含推免)', '(42)通信电子、卫星导航及多媒体  专业：2(不含推免)', '(43)卫星移动通信、多媒体与物联网  专业：2(不含推免)', '(44)人工智能与金融  专业：2(不含推免)', '(45)宽带融合网、智能光互联、空天地一体网络  专业：2(不含推免)', '(46)宽带通信  专业：2(不含推免)', '(47)空间光通信和图像处理  专业：2(不含推免)', '(48)光通信与人工智能、空天地一体网络  专业：2(不含推免)', '(49)光电器件与集成  专业：2(不含推免)', '(50)宽带通信与光智能信息处理技术  专业：2(不含推免)', '(51)高速融合光通信  专业：2(不含推免)', '(52)宽带光接入与光网络融合技术  专业：2(不含推免)', '(53)移动电子商务、无线通信与物联网、数据挖掘  专业：2(不含推免)', '(54)无线通信  专业：2(不含推免)', '(55)卫星通信、移动通信、物联网  专业：2(不含推免)', '(56)射频天线、太赫兹通信  专业：2(不含推免)', '(57)电磁兼容与信息安全、智慧电子技术与人工智能  专业：2(不含推免)', '(58)宽带通信器件和系统、电磁兼容  专业：2(不含推免)', '(59)无线光通信、微波光子技术  专业：2(不含推免)', '(60)认知无线电、智能信息处理  专业：2(不含推免)', '(61)无线通信理论研究与应用  专业：2(不含推免)', '(62)数据信息处理与智能服务  专业：2(不含推免)', '(63)人工智能、雷达信号处理  专业：2(不含推免)', '(64)天线与电波传播  专业：2(不含推免)', '(65)电磁兼容、超宽带无线通信、移动互联网  专业：2(不含推免)', '(66)物联网与大数据  专业：2(不含推免)', '(67)微纳电子技术、智能通信、物联网与大数据  专业：2(不含推免)', '(68)多媒体通信与集成电路技术  专业：2(不含推免)', '(69)光电检测与光通信  专业：2(不含推免)', '(70)图像处理  专业：2(不含推免)', '(71)移动互联网、通信网络及安全  专业：2(不含推免)', '(72)信息物理融合、智能人机交互、移动云计算  专业：2(不含推免)', '(73)柔性可穿戴器件  专业：2(不含推免)', '(74)柔性光电子材料及器件、拓扑光子学  专业：2(不含推免)', '(75)低维光电材料与器件  专业：2(不含推免)', '(76)电子信息材料及器件  专业：2(不含推免)', '(01)物联网服务计算、网络安全、大数据技术  专业：96(不含推免)', '(02)数据挖掘与大数据技术  专业：96(不含推免)', '(03)新型网络技术及网络空间信息处理技术  专业：96(不含推免)', '(04)嵌入式系统与移动智能技术、智能网络技术  专业：96(不含推免)', '(05)物联网与人工智能技术  专业：96(不含推免)', '(06)智能信息处理、智能搜索与挖掘、大数据分析  专业：96(不含推免)', '(07)物联网技术与安全、智能服务计算与大数据、智能硬件  专业：96(不含推免)', '(08)物联网与多媒体计算  专业：96(不含推免)', '(09)大数据、AI及医疗金融应用，未来无线网络  专业：96(不含推免)', '(10)自然语言处理、多模态信息处理、智能安全  专业：96(不含推免)', '(11)人工智能、软件工程、大数据  专业：96(不含推免)', '(12)云计算与大数据技术  专业：96(不含推免)', '(13)大数据与商业智能  专业：96(不含推免)', '(14)冬奥会赛时实习生项目  专业：96(不含推免)', '(15)不区分研究方向  专业：61(不含推免)', '(01)物联网与智能工程技术  专业：70(不含推免)', '(02)大数据与信息处理  专业：70(不含推免)', '(03)智能应用软件开发  专业：70(不含推免)', '(04)区块链软件/智慧医疗软件/可信软件测试  专业：70(不含推免)', '(05)移动互联网与大数据分析挖掘  专业：70(不含推免)', '(06)软件工程（人工智能、大数据）  专业：70(不含推免)', '(07)软件工程技术  专业：24(不含推免)', '(01)网络安全、数据挖掘、情报安全技术  专业：61(不含推免)', '(02)网络安全、云计算与可信服务、大数据分析  专业：61(不含推免)', '(03)网络安全攻防、大数据安全、移动互联网安全  专业：61(不含推免)', '(04)网络攻防、手机安全、人工智能、物联网安全  专业：61(不含推免)', '(05)密码学、智能安全、复杂网络安全、区块链  专业：61(不含推免)', '(06)智能信息处理  专业：61(不含推免)', '(07)漏洞挖掘与分析、车联网安全、大数据分析  专业：61(不含推免)', '(08)漏洞挖掘、渗透测试、固件安全、5G安全  专业：61(不含推免)', '(09)密码学技术、物联网安全技术、信息安全技术  专业：61(不含推免)', '(10)网络安全、大数据分析、无线安全、智能决策  专业：61(不含推免)', '(01)智慧云网络、人工智能与人机交互  专业：105(不含推免)', '(02)网络智能管理、能源互联网信息通信  专业：105(不含推免)', '(03)智能系统与应用/物联网/大数据/AR/软件测试  专业：105(不含推免)', '(04)移动互联网/云/物联网/机器学习相关安全  专业：105(不含推免)', '(05)面向网络协同计算的大数据与人工智能技术  专业：105(不含推免)', '(06)移动物联网，人工智能，大数据与云计算  专业：105(不含推免)', '(07)网络大数据与协同智慧计算  专业：105(不含推免)', '(08)下一代互联网及大数据分析  专业：105(不含推免)', '(09)分布式系统  专业：105(不含推免)', '(10)网络与信息安全  专业：105(不含推免)', '(11)工业互联网/大数据分析/区块链技术  专业：105(不含推免)', '(12)移动互联网、大数据与人工智能、区块链技术  专业：105(不含推免)', '(13)智慧5G、大数据和机器学习应用开发  专业：105(不含推免)', '(14)移动互联网安全技术  专业：105(不含推免)', '(15)移动媒体与文化计算  专业：105(不含推免)', '(01)光网络技术  专业：106(不含推免)', '(02)无线光通信与组网  专业：106(不含推免)', '(03)宽带通信与物联网技术  专业：106(不含推免)', '(04)宽带接入网与光纤传感  专业：106(不含推免)', '(05)光纤通信器件与系统技术  专业：106(不含推免)', '(06)信息处理与机器学习  专业：106(不含推免)', '(07)物联网技术研究与应用  专业：106(不含推免)', '(08)智能感知及物联网  专业：106(不含推免)', '(09)传感分析及控制技术  专业：106(不含推免)', '(10)机器学习与物联网技术  专业：106(不含推免)', '(11)光纤通信器件与系统技术  专业：106(不含推免)', '(12)光通信与光网络技术  专业：106(不含推免)', '(13)光通信和无线通信技术  专业：106(不含推免)', '(14)宽带互联网络  专业：106(不含推免)', '(15)光纤传感技术  专业：106(不含推免)', '(16)高速光传输与空间光通信  专业：106(不含推免)', '(17)三维显示与虚拟现实  专业：106(不含推免)', '(18)光信号处理  专业：106(不含推免)', '(19)新型光电子器件  专业：106(不含推免)', '(20)智能光电信息处理  专业：106(不含推免)', '(21)三维显示  专业：106(不含推免)', '(22)图形图像处理  专业：106(不含推免)', '(23)智慧无线电技术  专业：106(不含推免)', '(24)微波接收与测量  专业：106(不含推免)', '(25)微波光子技术应用  专业：106(不含推免)', '(26)光纤无线融合接入技术  专业：106(不含推免)', '(27)新型微纳光子器件及其智能设计  专业：106(不含推免)', '(28)新型光电子器件、系统与生物应用  专业：106(不含推免)', '(29)高速光通信与光成像技术  专业：106(不含推免)', '(30)光通信与宽带网技术  专业：106(不含推免)', '(31)量子信息网络与人工智能光联网  专业：106(不含推免)', '(32)区块链可信网络  专业：106(不含推免)', '(33)海洋信息网络与光通信  专业：106(不含推免)', '(34)通信系统与网络安全  专业：106(不含推免)', '(35)通信电子与网络安全  专业：106(不含推免)', '(36)光子晶体光纤及应用  专业：106(不含推免)', '(37)纳米光子技术与应用  专业：106(不含推免)', '(38)数据分析及应用  专业：106(不含推免)', '(39)数据网络技术  专业：106(不含推免)', '(40)高速宽带光交换与光网络  专业：106(不含推免)', '(41)数据中心光互联网络  专业：106(不含推免)', '(42)光无线融合资源管理与网络规划  专业：106(不含推免)', '(43)物联应用与智能网络  专业：106(不含推免)', '(44)量子信息技术  专业：106(不含推免)', '(45)机器学习及其嵌入式实现  专业：106(不含推免)', '(01)Web多媒体搜索与挖掘，网络智能信息处理  专业：203(不含推免)', '(02)未来通信与网络、智能信息处理与智能医疗  专业：203(不含推免)', '(03)宽带无线移动通信系统理论、技术及应用  专业：203(不含推免)', '(04)先进网络信息处理、空间通信与智能数据融合  专业：203(不含推免)', '(05)宽带无线移动通信、下一代网络及信息处理  专业：203(不含推免)', '(06)未来网络架构、软件定义网络、网络人工智能  专业：203(不含推免)', '(07)智能数据科学与应用  专业：203(不含推免)', '(08)宽带协同融合网络与智能安全控管技术  专业：203(不含推免)', '(09)无线大数据与泛在智能系统  专业：203(不含推免)', '(10)大数据、物联网、网络安全应用  专业：203(不含推免)', '(11)智慧5G、物联网和智能服务开发  专业：203(不含推免)', '(12)移动通信与网络大数据，视频智能计算及应用  专业：203(不含推免)', '(13)移动通信  专业：203(不含推免)', '(14)物联网智能应用及机器学习  专业：203(不含推免)', '(15)无线大数据、边缘计算系统和平台研发、天地一体化信息网络研发  专业：203(不含推免)', '(16)物联网与人工智能  专业：203(不含推免)', '(17)机器认知与智能视觉，数字广播  专业：203(不含推免)', '(18)宽带移动通信与物联网应用  专业：203(不含推免)', '(19)未来移动通信、机器学习与网络多媒体  专业：203(不含推免)', '(20)未来移动通信技术、智能计算与智慧物联网  专业：203(不含推免)', '(21)计算机视觉与图像识别  专业：203(不含推免)', '(22)物联网、区块链、频谱工程、人工智能  专业：203(不含推免)', '(23)物联网、移动互联网与人工智能技术  专业：203(不含推免)', '(24)信息系统与人工智能  专业：203(不含推免)', '(25)工业互联网、大数据分析及应用  专业：203(不含推免)', '(26)无线大数据与移动互联安全  专业：203(不含推免)', '(27)人工智能与大数据，区块链应用与物联网安全  专业：203(不含推免)', '(28)认知无线电通信工程  专业：203(不含推免)', '(29)车联网、智能医疗及大数据工程  专业：203(不含推免)', '(30)区块链与物联网技术，网络信息智能分析  专业：203(不含推免)']"

if __name__ == '__main__':
    main()