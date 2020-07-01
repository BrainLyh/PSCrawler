---

---

title: 使用Selenium 编写爬虫动态爬取网站

date: 1/7/2020

---



# 使用 Selenium 编写爬虫动态爬取网站

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

手册：`https://phantomjs.org/quick-start.html`

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
4. 数据可视化

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
   
                   ul = driver.find_element_by_xpath("//ul[@class='ch-page']")
                   li = ul.find_elements_by_xpath("li")
                   li[-1].click()
                   pagenumber -= 1
   
           # print(name_list)
           return name_list, major_numbers_list, number_list, flag
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

数据可视化我们选择 [pyecharts](http://pyecharts.org/#/zh-cn/intro) ,原因在于它的高度抽象，极大的简化了我们对数据进行可视化的操作难度。

该项目中我们主要在三处使用了可视化相关操作，分别是：

1. 对相关高校在各省分布的全国地图绘制
2. 对选择城市开设目标专业的高校招生情况的折线图绘制
3. 对目标高校开设目标专业的招生情况柱状图绘制

数据可视化的关键在于 **数据的格式化** ，剔除无关数据，保证完整的数据关系

以绘制全国地图为例，在得到各个包含各个省市名称的列表之后，需要对这些名称进行格式化处理，只保留主要关键字：北京市->北京、新疆维吾尔族自治区 -> 新疆、黑龙江省 -> 黑龙江 等

```python
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
```

再将城市名称列表与数量列表合并之后，即可绘制地图

```python
map_1 = Map()
            map_1.set_global_opts(
                title_opts=opts.TitleOpts(title="2020高校分布"),
                visualmap_opts=opts.VisualMapOpts(max_=40)  # 最大数据范围
            )
            map_1.add("2020高校分布", list1, maptype="china")
            map_1.render('SchoolMap.html')
```

其他两个例子同理

## 功能划分

有了可视化之后，我们就可以尝试将代码功能划分的更细致。主要实现三个功能：

1. 根据输入的门类类别代码，学科类别代码来绘制符合条件的高校在全国各省的分布情况
2. 根据输入的省份、门类类别代码、学科类别代码来绘制符合条件的高校对应专业的拟招生人数等信息
3. 根据输入的高校名称、学科类别代码来绘制该高校开设的专业数量和对应的拟招生人数

### 面向对象

将功能抽象为三个类，分别为：`SchoolMap` 、 `ReserachDirections` 、 `RDsBySchoolName` 

`SchoolMap` 负责实现功能一，主要代码

```python
# 返回当前所选择城市开设目标专业的高校数量
    def count_city(self, driver):
        pagenumber = self.paging(driver)
        counts = 0
        self.FlagOfProcess = True

        if (pagenumber == 1):
            try:
                # 不用下一页操作
                numbers = driver.find_elements_by_xpath("//tbody//tr")
                counts = len(numbers)
            except:
                self.FlagOfProcess = False
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
```

`ReserachDirections` 主要实现功能二，主要代码为：

```python
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
```

`RDsBySchoolName` 主要负责功能三，主要代码为：

```python
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
```

## 完整代码

**CSCrawler.py**

```python
#!/usr/bin/env python
# encoding: utf-8
'''
@author: Brian
@file: CSCrawler.py
@time: 2020/6/30 14:42
@desc: 程序的主入口函数
'''

from SchoolMapByPyEcharts import SchoolMap
from ResearchDirectionsByPyEcharts import ReserachDirections
from RDsBySchoolName import RDsBySchoolName
import time

class CSCrawler(object):

    def __init__(self, url, yjxkdm):
        self.url = url
        self.yjxkdm = yjxkdm

    def SchoolMap(self, mldm):
        school_map = SchoolMap(self.url, mldm, self.yjxkdm)
        driver = school_map.set_driver()
        city_name, school_counts = school_map.select_major(driver)

        school_map.visulize(city_name, school_counts)

    def ResearchDirection(self, count, mldm):
        researdirection = ReserachDirections(self.url, count, mldm, self.yjxkdm)
        driver = researdirection.set_driver()

        x, y1, y2, flag = researdirection.select_option(driver)

        researdirection.stacked_area_chart(x, y1, y2, flag)

    def RDsBySchoolName(self, schoolname):
        rds = RDsBySchoolName(self.url, schoolname, self.yjxkdm)
        driver = rds.set_driver()
        x, y1, y2, flag = rds.select_school(driver)
        rds.stacked_area_chart(x, y1, y2, flag)


def main():
    print(""
          """
          -------欢迎来到研招网专业目录信息爬虫项目-------
                        你想做什么?
                [1]: 目标专业的全国分布地图
                [2]: 目标省份内个高校对相关专业的招收情况
                [3]: 目标院校对应专业的研究方向与拟招生人数情况
                [4]: 退出程序
          -----------请在下方输入相关操作代码------------
          """
          "")
    flag = True
    while(flag):
        code = input("请输入操作代码：").strip()

        if(code == str(1)):
            print("正在加载目标专业的全国分布地图的程序...")
            time.sleep(1)
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
            mldm = str(input("请输入门类类别代码： ")).strip()
            yjxkdm = str(input("请输入学科类别代码： ")).strip()
            url = "https://yz.chsi.com.cn/zsml/queryAction.do"
            crawler = CSCrawler(url,yjxkdm)
            crawler.SchoolMap(mldm)
            print("正在收集数据...")

        elif(code == str(2)):
            print("正在加载目标省份内个高校对相关专业的招收情况的程序...")
            time.sleep(1)
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
            count = str(input("请输入城市代码： ")).strip()
            mldm = str(input("请输入门类类别代码： ")).strip()
            yjxkdm = str(input("请输入学科类别代码： ")).strip()
            crawler = CSCrawler(url, yjxkdm)
            crawler.ResearchDirection(count,mldm)
            print("正在收集数据...")

        elif(code == str(3)):
            print("正在记载目标院校对应专业的研究方向与拟招生人数情况的程序...")
            time.sleep(1)
            print(""
                  """
        请分行输入完整的学校名称与学科类别代码，如：
            学校名称：北京大学
            专业类别代码：0202"""
                  )
            schoolname = str(input("请输入学校名称： ")).strip()
            yjxkdm = str(input("请输入学科类别代码： ")).strip()
            url = "https://yz.chsi.com.cn/zsml/queryAction.do"
            crawler = CSCrawler(url, yjxkdm)
            crawler.RDsBySchoolName(schoolname)

            print("正在收集数据...")
        elif(code == str(4)):
            print("正在退出...")
            time.sleep(1)
            break
        else:
            print("对不起，暂不支持此操作！请重新输入...")


if __name__ == '__main__':
    main()
```

**SchoolMapByPyEcharts.py**

```python
#!/usr/bin/env python
# encoding: utf-8
'''
@author: Brian
@file: SchoolMapByPyEcharts.py
@time: 2020/6/26 15:06
@desc: 重新选择爬取方法，更好的为可视化提供数据
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.commons.utils import JsCode


class SchoolMap(object):

    def __init__(self, url, mldm, yjxkdm):
        self.url = url
        self.mldm = mldm
        self.yjxkdm = yjxkdm
        self.FlagOfProcess = True

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
        self.FlagOfProcess = True

        if (pagenumber == 1):
            try:
                # 不用下一页操作
                numbers = driver.find_elements_by_xpath("//tbody//tr")
                counts = len(numbers)
            except:
                self.FlagOfProcess = False
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
        # print(city_name, city_value)

        # 遍历城市代码，传入统计高校数量的函数
        for count in city_value:
            counts = self.select_option(driver, count)
            school_counts.append(counts)
        # print(school_counts)

        driver.close()
        driver.quit()
        print("正在准备绘制图表...")
        return city_name, school_counts

    # 数据可视化
    def visulize(self, city_name, school_counts,):
        if(self.FlagOfProcess):
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
            # print(list1)

            map_1 = Map()
            map_1.set_global_opts(
                title_opts=opts.TitleOpts(title="2020高校分布"),
                visualmap_opts=opts.VisualMapOpts(max_=40)  # 最大数据范围
            )
            map_1.add("2020高校分布", list1, maptype="china")
            # map_1.add_js_funcs("window.confirm()")
            map_1.render('SchoolMap.html')
            print("绘制成功，请在同级目录下查看 SchoolMap.html 文件！")
        else:
            print("出现错误，停止绘制图表！")
```

**ResearchDirectionsByPyEcharts.py**

```python
#!/usr/bin/env python
# encoding: utf-8
'''
@author: Brian
@file: ResearchDirectionsByPyEcharts.py
@time: 2020/6/27 15:38
@desc: 对每个城市的高校开设的研究方向进行处理，并打印结果中的985&211院校
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
        list_211 = ['清华大学', '北京大学', '中国人民大学', '北京工业大学', '北京理工大学', '北京航空航天大学', '北京化工大学',
                    '北京邮电大学', '对外经济贸易大学', '中国传媒大学', '中央民族大学', '中国矿业大学', '中央财经大学',
                    '中国政法大学', '中央音乐学院', '北京体育大学', '北京外国语大学', '北京交通大学', '北京科技大学',
                    '北京林业大学', '中国农业大学', '北京中医药大学', '华北电力大学', '北京师范大学', '中国地质大学',
                    '复旦大学', '华东师范大学', '上海外国语大学', '上海大学', '同济大学', '华东理工大学', '东华大学',
                    '上海财经大学', '上海交通大学', '南开大学', '天津大学', '天津医科大学', '河北工业大学', '重庆大学',
                    '西南大学', '太原理工大学', '内蒙古大学', '大连理工大学', '东北大学', '辽宁大学', '大连海事大学',
                    '吉林大学', '东北师范大学', '延边大学', '东北农业大学', '东北林业大学', '哈尔滨工业大学', '哈尔滨工程大学',
                    '南京大学', '东南大学', '苏州大学', '河海大学', '中国药科大学', '南京师范大学', '南京理工大学',
                    '南京航空航天大学', '江南大学', '南京农业大学', '浙江大学', '安徽大学', '合肥工业大学', '中国科学技术大学',
                    '厦门大学', '福州大学', '南昌大学', '山东大学', '中国海洋大学', '中国石油大学', '郑州大学', '武汉大学',
                    '华中科技大学', '华中师范大学', '华中农业大学', '中南财经政法大学', '武汉理工大学', '湖南大学', '中南大学',
                    '湖南师范大学', '中山大学', '暨南大学', '华南理工大学', '华南师范大学', '广西大学', '四川大学', '西南交通大学',
                    '电子科技大学', '西南财经大学', '四川农业大学', '云南大学', '贵州大学', '西北大学', '西安交通大学',
                    '西北工业大学', '陕西师范大学', '西北农林科大', '西安电子科技大学', '长安大学', '兰州大学', '新疆大学',
                    '石河子大学', '海南大学', '宁夏大学', '青海大学', '西藏大学', '第二军医大学', '第四军医大学', '国防科学技术大学']

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

        empty = []
        for i in school_list:
            for j in list_211:
                if i == j:

                    empty.append(i)
                    break
        print("当前条件下，985&211 院校有：")
        print(empty)

        driver.close()
        driver.quit()
        # print(school_list, major_numbers_list, number_list)
        # ['黑龙江大学', '哈尔滨工业大学', '哈尔滨理工大学', '哈尔滨工程大学', '黑龙江科技大学', '东北石油大学', '黑龙江八一农垦大学', '东北林业大学', '哈尔滨师范大学', '齐齐哈尔大学']
        #  [8, 21, 15, 59, 6, 10, 2, 3, 10, 6]
        #  [78, 1549, 123, 201, 153, 149, 331, 221, 115, 520]

        print("正在准备绘制图表...")
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
            print("绘制成功，请在同级目录下查看 ReserachDirections.html 文件！")
        else:
            print("出现错误，停止绘制图表！")
```

**RDsBySchoolName.py**

```python
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
                    .render("ReserachDirections.html")
            )
            print("绘制成功，请在同级目录下查看 ReserachDirections.html 文件！")
        else:
            print("出现错误，停止绘制图表！")
```



## 参考链接

[AJAX-XMLHtppRequest 的前世今生](https://blog.csdn.net/J080624/article/details/84171917)

[Selenium和PhantomJS介绍](https://blog.csdn.net/qq_33689414/article/details/78631009)

[Pyhon爬虫教程](https://programmer.group/python-crawler-8-selenium-and-phantomjs-for-dynamic-html-processing.html)

[pyecharts官网](http://pyecharts.org/#/zh-cn/intro)