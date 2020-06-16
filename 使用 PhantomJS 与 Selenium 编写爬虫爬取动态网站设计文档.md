---

---

title: 使用 PhantomJS 与 Selenium 编写爬虫爬取动态网站

date: 29/5/2020

---



# 使用 PhantomJS 与 Selenium 编写爬虫爬取动态网站

## Intro

传统的浏览器请求响应方式是：我们在一个网站上点击了一个请求资源的按钮，就会对服务器发起一次请求，然后响应再返回到浏览器。该请求是一个完整的 HTML 页面，因此当浏览器用到新的 HTML 页面重绘时，可能会看到闪烁，这一方面增加了服务器的压力，同时降低了用户的体验度。

Web 2.0 很大程度上消除了这种看得见的交互。虽然仍有请求和相应，只不过都隐藏到了幕后，作为用户，体验更加舒适。

如何实现呢？我们需要发送和请求的数据只包含我们需要的，而不是整个 HTML 页面。这种情况下 Ajax 允许在不更新整个 HTML 页面的情况下发送和接收数据。

## 如何爬取动态加载的资源？

这种方式方便了用户，可是对我们爬取网页内容缺造成了不便。

相对于传统的静态页面，我们在爬取页面内容时只需要简单的获取整个 HTML 文本然后对其中的内容进行匹配、提取即可。

对于采用动态记载内容的网站来说，我们查看网页源代码会发现许多我们需要的资源是需要加载请求才能从服务器返回的。比如百度首页



### Selenium & PhantomJS简介

Selenium 是一个 Web 的自动化测试工具，最初是为了网站自动化测试开发的， Selenium 测试直接运行在浏览器中，就像真正的用户在操作一样。支持的浏览器包括IE（7, 8, 9, 10, 11），Mozilla Firefox，Safari，Google Chrome，Opera等。也包括 PhantomJS 。

Selenium 可以根据我们的指令，让浏览器自动加载页面，获取需要的数据，甚至是页面截屏。
安装：`pip install selenium`

官方文档：`http://selenium-python.readthedocs.io/index.html`

PhantomJS 是一个基于 Webkit 的“无界面”( headless )浏览器，它会把网站加载到内存并执行页面上的 JavaScript，因为不会展示图形界面，所以运行起来比完整的浏览器要高效。

如果我们把 Selenium 和 PhantomJS 结合在一起，就可以运行一个非常强大的网络爬虫了，这个爬虫可以处理 JavaScript、Cookie、headers，以及任何我们真实用户需要做的事情。

官方文档：`http://phantomjs.org/documentation`

下载地址： ` http://phantomjs.org/download.html`

我们可以通过下面的方式来获得一个 **chromedriver** 驱动的浏览器([需要安装对应驱动](https://sites.google.com/a/chromium.org/chromedriver/home))

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=chrome_options)
```

当然你也可以使用 **PhantomJS** 但是存在的问题是由于两种驱动请求页面的方式不同，后者在页面没有完全记载时就会尝试早期请求，这常常会导致 `InvalidElementStateException` 错误，当然，我们可以在请求页面第一个元素之前就调用 `time` 函数，进行 `sleep(2)` 等待。

除此之外，**PhantomJS** 也已经不再更新，这也驱使我们使用新的驱动程序。

### 简单使用

```python
# 导入 webdriver
from selenium import webdriver

# 调用键盘按键操作时需要引入的Keys包
from selenium.webdriver.common.keys import Keys

# 调用环境变量指定的PhantomJS浏览器创建浏览器对象
driver = webdriver.PhantomJS()

# 如果没有在环境变量指定PhantomJS位置
# driver = webdriver.PhantomJS(executable_path="./phantomjs"))

# get方法会一直等到页面被完全加载，然后才会继续程序，通常测试会在这里选择 time.sleep(2)
driver.get("http://www.baidu.com/")

# 获取页面名为 wrapper的id标签的文本内容
data = driver.find_element_by_id("wrapper").text

# 打印页面标题 "百度一下，你就知道"
print driver.title

# 生成当前页面快照并保存
driver.save_screenshot("baidu.png")

# id="kw"是百度搜索输入框，输入字符串"长城"
driver.find_element_by_id("kw").send_keys(u"长城")

# id="su"是百度搜索按钮，click() 是模拟点击
driver.find_element_by_id("su").click()

# ctrl+a 全选输入框内容
driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'a')

# ctrl+x 剪切输入框内容
driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'x')

# 获取href值
driver.find_element_by_xpath("html/body/div/div[1]/div[2]/a[1]").get_attribute('href')

# 模拟Enter回车键，替代点击操作
driver.find_element_by_id("su").send_keys(Keys.RETURN)

# 清除输入框内容
driver.find_element_by_id("kw").clear()

# 关闭当前页面，如果只有一个页面，会关闭浏览器
# driver.close()

# 关闭浏览器
driver.quit()
```

[简单操作文档](https://dengxj.blog.csdn.net/article/details/104322155)

[selenium官方文档](https://selenium-python.readthedocs.io/index.html)

[PhantomJS手册](https://phantomjs.org/quick-start.html)

使得截图截取到最大屏幕

```python
# 接下来是全屏的关键，用js获取页面的宽高，如果有其他需要用js的部分也可以用这个方法
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    print(width, height)
    # 窗口最大化
    driver.set_window_size(width, height)
```

### 切换页面

当有许多 Tab 时我们需要判断我们当前处于哪个页面，使用 `window_handles` 来操作

```python
	# Store the ID of the original window
	original_window = driver.current_window_handle

    # Check we don't have other windows open already
    assert len(driver.window_handles) == 1
    
    # Wait for the new window or tab
    wait.until(EC.number_of_windows_to_be(2))

    # Loop through until we find a new window handle
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
            
    wait.until(EC.title_is("title"))
```



### 复选框选择

选择一个实际场景进行测试，[以研招网硕士专业目录为例](https://yz.chsi.com.cn/zsml/zyfx_search.jsp) 

![image-20200616164407200](C:\Users\brian\AppData\Roaming\Typora\typora-user-images\image-20200616164407200.png)

这有一个 `select` 标签下的复选框，用常规的方法解析 `Xpath` 路径可以获取到想要的元素，但是没办法进行选择，这里采用 `Selenium` 提供的 `Select` 库进行选择，[文档在这里](https://selenium-python-zh.readthedocs.io/en/latest/api.html)

```python
# 使用 Select 处理下拉框的选项
# 先通过 Xpath 找到 select 标签，然后通过 value 找到对应值即可选择
Select(driver.find_element_by_xpath("//select[@id='mldm']")).select_by_value('zyxw')
Select(driver.find_element_by_xpath("//select[@id='yjxkdm']")).select_by_value("0854")
```

这样，我们就成功的选择到想要的元素，之后进行查询跳转即可。

## 参考链接

[AJAX-XMLHtppRequest 的前世今生](https://blog.csdn.net/J080624/article/details/84171917)

[Selenium和PhantomJS介绍](https://blog.csdn.net/qq_33689414/article/details/78631009)

[Pyhon爬虫教程](https://programmer.group/python-crawler-8-selenium-and-phantomjs-for-dynamic-html-processing.html)

[廖雪峰的官方网站](https://www.liaoxuefeng.com/wiki/1022910821149312/1023022332902400)