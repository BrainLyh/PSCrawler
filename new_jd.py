# coding=utf-8
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pyquery import PyQuery as pq
import csv
import json

driver = webdriver.Firefox()
wait = WebDriverWait(driver,10)
keyword = 'iphone'
data_list = []#存放数据
product = {}
def search():
    try:
        driver.get("http://www.jd.com")
        input = wait.until(EC.presence_of_element_located((By.XPATH,'.//*[@id="key"]')))#等待条件完成后再执行操作
        button = wait.until(EC.element_to_be_clickable((By.XPATH,'.//*[@id="search"]/div/div[2]/button')))
        input.send_keys(keyword)
        button.click()
        total = wait.until(EC.presence_of_element_located((By.XPATH,'.//*[@id="J_bottomPage"]/span[2]/em[1]/b'))).text
        print(total)
        # return total
        print("第1页:")
        get_products()
        return total
    except TimeoutError:
        search()

def get_products():
    try:
        html = driver.page_source
        doc = pq(html)
        items = doc('#J_goodsList .gl-i-wrap').items()  # 先id，后class
        ####字典形式存储####
        for item in items:
            product = {
                'name' : item.find('em').text(),
                'price': item.find('.p-price').text(),
                'shop' : item.find('.p-shop').text(),
            }
            print(product)
            data_list.append(product)
    except TimeoutError:
        get_data()

def next_page():
    totalnum = search()
    num = 1
    while num !=10:
        print("第%s页" %str(num+1))
        num += 1
        wait.until(EC.presence_of_element_located((By.XPATH,".//*[@id='J_bottomPage']/span[2]/input"))).clear()
        wait.until(EC.presence_of_element_located((By.XPATH,".//*[@id='J_bottomPage']/span[2]/input"))).send_keys(num)
        wait.until((EC.presence_of_element_located((By.XPATH,".//*[@id='J_bottomPage']/span[2]/a")))).click()
        # driver.find_element_by_xpath(".//*[@id='J_bottomPage']/span[2]/input").clear()
        # driver.find_element_by_xpath(".//*[@id='J_bottomPage']/span[2]/input").send_keys(num)
        # driver.find_element_by_xpath(".//*[@id='J_bottomPage']/span[2]/a").click()
        time.sleep(1)
        get_products()


# def page_num():
#     # total = wait.until(EC.presence_of_element_located((By.XPATH, './/*[@id="J_bottomPage"]/span[2]/em[1]/b'))).text
#     for i in range(2,10):
#         next_page(i)

def save_data():
    with open('DATA.csv','a',newline='') as f:
        title = data_list[0].keys()#获取头部标签
        writer = csv.DictWriter(f,title)
        writer.writeheader()
        writer.writerows(data_list)
    print('csv文件写入成功！')

if __name__ == '__main__':
    # search()
    # get_products()
    next_page()
    # page_num()
    save_data()
    driver.quit()
