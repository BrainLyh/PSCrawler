---

---

title: 使用 PhantomJS 与 Selenium 编写爬虫爬取动态网站

date: 29/5/2020

---



# 使用 Selenium 编写爬虫爬取动态网站

## Intro

传统的浏览器请求响应方式是：我们在一个网站上点击了一个请求资源的按钮，就会对服务器发起一次请求，然后响应再返回到浏览器。该请求是一个完整的 HTML 页面，因此当浏览器用到新的 HTML 页面重绘时，可能会看到闪烁，这一方面增加了服务器的压力，同时降低了用户的体验度。

Web 2.0 很大程度上消除了这种看得见的交互。虽然仍有请求和相应，只不过都隐藏到了幕后，作为用户，体验更加舒适。

如何实现呢？我们需要发送和请求的数据只包含我们需要的，而不是整个 HTML 页面。这种情况下 Ajax 允许在不更新整个 HTML 页面的情况下发送和接收数据。

## 如何爬取动态加载的资源？

这种方式方便了用户，可是对我们爬取网页内容缺造成了不便。

相对于传统的静态页面，我们在爬取页面内容时只需要简单的获取整个 HTML 文本然后对其中的内容进行匹配、提取即可。

对于采用动态记载内容的网站来说，我们查看网页源代码会发现许多我们需要的资源是需要加载请求才能从服务器返回的。



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

使用JS取得最大屏幕

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

![研招网首页](F:\all_kinds_file\课设\大三下\文档图片\研招网首页.png)

这有一个 `select` 标签下的复选框，用常规的方法解析 `Xpath` 路径可以获取到想要的元素，但是没办法进行选择，这里采用 `Selenium` 提供的 `Select` 库进行选择，[文档在这里](https://selenium-python-zh.readthedocs.io/en/latest/api.html)

```python
# 使用 Select 处理下拉框的选项
# 先通过 Xpath 找到 select 标签，然后通过 value 找到对应值即可选择
Select(driver.find_element_by_xpath("//select[@id='mldm']")).select_by_value('zyxw')
Select(driver.find_element_by_xpath("//select[@id='yjxkdm']")).select_by_value("0854")
```

这样，我们就成功的选择到想要的元素，之后进行查询跳转即可。

## 爬虫设计

我们将本次爬虫分为几大部分

1. 逻辑分析
2. 代码实现
4. 数据可视化分析

### 逻辑分析

此次爬虫我们的设计目标是爬取研招网2020年的考研相关数据，我们需要先认为的对目标网站进行查询操作，明确操作流程之后，再进行下一步。

1. **选择我们要使用的浏览器**，进入查询网址，[研招网硕士专业目录查询](https://yz.chsi.com.cn/zsml/queryAction.do)
2. 打开研招网的硕士目录后需要先至少选择两项条件，且学科类别为必选项，**选择好条件**之后才能进行查询

![研招网首页](F:\all_kinds_file\课设\大三下\文档图片\研招网首页.png)

2. 我们以 专业学位、电子信息 为筛选条件，选择好条件后会**进行一次页面跳转**，进入包含所有符合我们选择条件的院校列表页面，可以看到，符合条件的院校非常多，有十几页的内容。
3. 对于这些院校，我们的关注点可能在于所在城市，以及所开设的研究方向等信息。我们选择一所院校进行点击之后，**会打开一个新的窗口** ，里面包含了该校在本学科类别下开设的所有研究方向与计划招收人数等信息，有些学校的研究方向非常多，可能会有十几页内容。
4. 查看完一个学校，**记录我们需要的信息**之后，我们可能会查看其他学校。于是，为了避免打开窗口过多，我们会**关闭新打开的窗口**，回到院校列表页面，重新打开一个学校的研究方向窗口。
5. 查询完成，**关闭浏览器**。

### 代码实现

针对上文的逻辑分析，我们编写代码时也主要完成上述动作。

1. 选择浏览器，并进行配置

   ```python
   # 配置 driver
   def set_driver(url):
       chrome_options = Options()
       chrome_options.add_argument("--headless") # 即所谓 无头 模式
       chrome_options.add_argument("--disable-gpu")
       driver = webdriver.Chrome(executable_path="E:/Program Files/chromedriver_win32/chromedriver.exe",
                                 chrome_options=chrome_options)
       driver.get(url)
       driver = set_height_width(driver)
   
       return driver
   
   
   # 将设置屏幕大小独立出来，方便每次跳转完使用
   def set_height_width(driver): 
       width = driver.execute_script("return document.documentElement.scrollWidth")
       height = driver.execute_script("return document.documentElement.scrollHeight")
       driver.set_window_size(width, height) # 将屏幕大小设置为最大，防止部分信息加载不完全
       return driver
   ```

2. 条件选择与页面跳转

   ```python
   # 选择目标专业
   def select_major(driver):
       original_window = driver.current_window_handle
       assert len(driver.window_handles) == 1
   
       try:
           # https://selenium-python-zh.readthedocs.io/en/latest/api.html
           # 使用 Select 处理下拉框的选项
           # 先通过 Xpath 找到 select 标签，然后通过 value 找到对应值即可选择
           Select(driver.find_element_by_xpath("//select[@id='mldm']")).select_by_value('zyxw') # 选择专业学位
           Select(driver.find_element_by_xpath("//select[@id='yjxkdm']")).select_by_value("0854") # 电子信息的专业代码
   
       except Exception as e:
           print("wrong " + str(e))
   
       driver.find_element_by_xpath("//input[@name='button']").click() # 找到查询按钮进行点击
   
       # 等待时间过长，超时
       # wait.until(EC.number_of_windows_to_be(2))
   	
       # 判断当前页面
       for window_handle in driver.window_handles:
           if window_handle != original_window:
               driver.switch_to.window(window_handle)
               break
       # 成功跳转到目标网页
       driver = set_height_width(driver)
       return driver
   ```

3. 选取该页面上的所有院校

   ```python
   # 获得所有院校列表
   def get_school_name(driver):
       # 记录院校列表页面的 handle
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
                                 "tr:nth-child({}) " \
                                 "td:nth-child(1) " \
                                 "form:nth-child(1) > a:nth-child(1)"
       css_selector_cityname = "body.ch-sticky:nth-child(2) " \
                               "div.main-wrapper:nth-child(2) " \
                               "div.container.clearfix:nth-child(4) " \
                               "div.zsml-row.clearfix div.zsml-list-box " \
                               "table.ch-table " \
                               "tbody:nth-child(2) " \
                               "tr:nth-child({}) > td:nth-child(2)"
       css_selector_pagenumbers = "body.ch-sticky:nth-child(2) " \
                                  "div.main-wrapper:nth-child(2) " \
                                  "div.container.clearfix:nth-child(4) " \
                                  "div.zsml-row.clearfix " \
                                  "div.zsml-page-box ul.ch-page li.lip:nth-child(8) > a:nth-child(1)"
       # 翻页数
       number = driver.find_element_by_css_selector(css_selector_pagenumbers).get_attribute("textContent")
   	# 下一页的页码
       flag = 2
       while (flag <= int(number) + 1):
           for i in range(1, 32):
               if i == 31:
                   try:
                       driver.find_element_by_css_selector("#goPageNo").send_keys(str(flag))  # 输入页码跳转
                       driver.find_element_by_xpath("//input[@class='page-btn']").click()  # 点击 Go，仍然同是一个 window_handle
                       flag += 1
                   except:
                       print("已经是最后一页啦".center(100, "-"))
                   break
               else:
                   try:
                       school_name = driver.find_element_by_css_selector(css_selector_schoolname.format(i)).get_attribute(
                           "textContent")
                       city_name = driver.find_element_by_css_selector(css_selector_cityname.format(i)).get_attribute("textContent")
   
                       # 跳转到每个学校对应的研究方向信息页面
                       driver.find_element_by_link_text(school_name).click()
                       for window_handle in driver.window_handles:
                           if window_handle != original_window:
                               driver.switch_to.window(window_handle)
                               break
                       driver = set_height_width(driver)
   
                       # 得到该学校各个研究方向的列表
                       major_list = get_major_info(driver)
                       major_list.insert(0, school_name)
   
                       print(major_list)
   
                       # 关闭信息页面，转到学校列表页面
                       driver.close()
                       driver.switch_to.window(original_window)
                       driver = set_height_width(driver)
   
                       school_and_city = school_name + "     " + city_name
                       school_name_list.append(school_and_city)
                       # print(school_name_list)
   
                   except Exception as e:
                       print(e)
                       # print("全部学校爬取完毕！".center(100, "-"))
   
       print(school_name_list)
       save_data(school_name_list)
       # 结果如下
       # ['(10002)中国人民大学', '(01)不区分研究方向  专业：17(不含推免)', '(02)不区分研究方向  专业：44(不含推免)']
   ```

4. 翻页处理

   ```python
   # 如果需要翻页就翻页
   def paging(driver):
   
       css_selector_pages = "body.ch-sticky:nth-child(2) " \
                            "div.main-wrapper:nth-child(2) " \
                            "div.container.clearfix:nth-child(5) " \
                            "div.zsml-row.clearfix div.zsml-page-box > ul.ch-page"
   
       ul = driver.find_element_by_css_selector(css_selector_pages)
       li = ul.find_elements_by_xpath("li") 
       # print(len(li))
       # 第一页右下角的标签数量最大为10，小于10时没有 Go 输入跳转框
       if(len(li) < 10):
           pagenumber = int(li[-2].text)
       # print(pagenumber)
       else:
           pagenumber = int(li[-3].text)
       return pagenumber
   
   ```

5. 获取研究方向等信息

   与院校列表页面不同，各个学校对应的研究方向的数量不同，存在研究方向页面数量不同的情况，这也造成了我们无法通过一种固定的方法来对所用的情况进行处理，于是，在这段代码里增加了数量判断。

   ```python
   # 获得院校在目标专业下的研究方向等信息
   def get_major_info(driver):
       # 当前页面有多少条数据
       major_list = []
       # 当前 Tab 里有多少个页面
       pagenumber = paging(driver)
       # print(pagenumber)
   
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
               # 定位页码
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
   
       # print(len(major_list))
       # print(major_list)
   
       return major_list
   ```

6. 保存数据

   ```python
   # 保存数据
   def save_data(data_list):
       with open("../major_info.txt", "w") as f:
           for line in data_list:
               f.write(line + "\r")
   ```

7. 关闭浏览器

   ```python
   driver.close()
   driver.quit()
   ```

### 数据可视化分析



## 参考链接

[AJAX-XMLHtppRequest 的前世今生](https://blog.csdn.net/J080624/article/details/84171917)

[Selenium和PhantomJS介绍](https://blog.csdn.net/qq_33689414/article/details/78631009)

[Pyhon爬虫教程](https://programmer.group/python-crawler-8-selenium-and-phantomjs-for-dynamic-html-processing.html)

[廖雪峰的官方网站](https://www.liaoxuefeng.com/wiki/1022910821149312/1023022332902400)