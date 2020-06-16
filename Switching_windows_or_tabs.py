#coding = utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
# Start the driver
with webdriver.Chrome(executable_path="E:/Program Files/chromedriver_win32/chromedriver.exe",
                          chrome_options=chrome_options) as driver:

    # Open URL
    driver.get("https://www.baidu.com/")

    # 接下来是全屏的关键，用js获取页面的宽高，如果有其他需要用js的部分也可以用这个方法
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    print(width, height)
    # 窗口最大化
    driver.set_window_size(width, height)
    # Setup wait for later
    # 在出现TimeoutException 异常之前将等待十秒或在十秒内发现了查找的元素
    wait = WebDriverWait(driver, 10)

    # Store the ID of the original window
    original_window = driver.current_window_handle

    print(original_window)
    # Check we don't have other windows open already
    assert len(driver.window_handles) == 1

    # Click the link which opens in a new window
    # line text 就是跳转链接上面的文字
    driver.find_element_by_link_text("地图").click()

    # Wait for the new window or tab
    wait.until(EC.number_of_windows_to_be(2))

    # Loop through until we find a new window handle
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
    print(driver.current_window_handle)
    print(driver.current_url)
    driver.save_screenshot("new-tab.jpg")

    # Wait for the new tab to finish loading content
    # 等待，直到跳转页面的title对了，也就是内容加载完成
    wait.until(EC.title_is("百度地图"))

    # 页面后退
    driver.back()
    print(driver.current_url)
