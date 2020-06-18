# coding=utf-8
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pyquery import PyQuery as pq

driver = webdriver.Firefox()
filename = "DATA.txt"
# count = 0
product = {}
def search():
    driver.get("http://www.jd.com")
    driver.find_element_by_xpath(".//*[@id='key']").send_keys(u"华为手机")
    driver.find_element_by_xpath(".//*[@id='search']/div/div[2]/button").click()


def next_page(page_number):
    driver.find_element_by_xpath(".//*[@id='J_bottomPage']/span[2]/input").clear()
    driver.find_element_by_xpath(".//*[@id='J_bottomPage']/span[2]/input").send_keys('page_number')
    driver.find_element_by_xpath(".//*[@id='J_bottomPage']/span[2]/a").click()
    get_products()

def get_products():
    html = driver.page_source
    doc = pq(html)
    items = doc('#J_goodsList .gl-i-wrap').items()  # 先id，后class
    # for item in items:
    #     product = {
    #         'name' : item.find('em').text(),
    #         'price': item.find('.p-price').text(),
    #         'shop' : item.find('.p-shop').text(),
    #     }
    #     print(product)
    for item in items:
        name = item.find('em').text()
        price = item.find('.p-price').text()
        shop = item.find('.p-shop').text()
        try:
            with open("DATA.txt",'a',encoding="utf-8") as f:
                f.write(name+' '+price+' '+shop+'\n'+'\n')
        finally:
            f.close()

def page_num():
    for i in range(2,10):
        next_page(i)
if __name__ == '__main__':
    search()
    get_products()
    page_num()
    driver.quit()
