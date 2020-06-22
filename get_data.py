# coding=utf-8
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pyquery import PyQuery as pq
from selenium.webdriver.support.ui import Select
import wordcloud
import matplotlib.pyplot as plt
from pyecharts import Map

school_list = []
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
# driver = webdriver.Chrome(executable_path="E:/download/shenxing/BIN/chromedriver.exe")
driver = webdriver.Firefox()
wait = WebDriverWait(driver,10)
driver.get("https://yz.chsi.com.cn/zsml/zyfx_search.jsp")


Select(driver.find_element_by_xpath("//select[@id='mldm']")).select_by_value('zyxw')
Select(driver.find_element_by_xpath("//select[@id='yjxkdm']")).select_by_value("0854")

driver.find_element_by_xpath("//input[@name='button']").click()
def get_data():
    html = driver.page_source
    doc = pq(html)
    items = doc('.zsml-list-box .ch-table').items()
    for item in items:
        name = item.find('a').text().replace(' ','\n')
        address = item.find('td').text().replace('\ue664','').replace('省','').replace('市','').replace("壮族自治区",'').replace("维吾尔自治区",'').replace("回族自治区",'').replace("自治区",'').replace('(11)','').replace('(12)','').replace('(13)','').replace('(14)','').replace('(15)','').replace('(16)','').replace('(17)','').replace('(18)','').replace('(19)','').replace('(20)','').replace('(21)','').replace('(22)','').replace('(23)','').replace('(24)','').replace('(25)','').replace('(26)','').replace('(27)','').replace('(28)','').replace('(29)','').replace('(30)','').replace('(31)','').replace('(32)','').replace('(33)','').replace('(34)','').replace('(35)','').replace('(36)','').replace('(37)','').replace('(38)','').replace('(39)','').replace('(40)','').replace('(41)','').replace('(42)','').replace('(43)','').replace('(44)','').replace('(45)','').replace('(46)','').replace('(47)','').replace('(48)','').replace('(49)','').replace('(50)','').replace('(51)','').replace('(52)','').replace('(53)','').replace('(54)','').replace('(55)','').replace('(56)','').replace('(57)','').replace('(58)','').replace('(59)','').replace('(60)','').replace('(61)','').replace('(62)','').replace('(63)','').replace('(64)','').replace('(65)','')
        print(address)
        try:
            with open("school.txt", 'a', encoding="utf-8") as f:
                f.write(address + '\n')
        finally:
            f.close()



def next_page():
    num = 1
    while num !=12:
        print("第%s页" %str(num))
        wait.until(EC.presence_of_element_located((By.XPATH,".//*[@id='goPageNo']"))).clear()
        wait.until(EC.presence_of_element_located((By.XPATH,".//*[@id='goPageNo']"))).send_keys(num)
        driver.find_element_by_class_name("page-btn").click()
        num += 1
        get_data()

def word_cloud():
    f = open('school.txt', 'r', encoding='utf-8').read()
    w = wordcloud.WordCloud(width=1000, height=700, background_color='white', font_path='msyh.ttc')
    w.generate(f)
    w.to_file('output1.png')
    plt.imshow(w)
    plt.axis("off")
    plt.show()

def number():
    pass

if __name__ == '__main__':
    next_page()
    # word_cloud()
    driver.quit()
