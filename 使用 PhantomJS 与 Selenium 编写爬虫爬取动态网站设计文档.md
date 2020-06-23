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

### 什么是AJAX？如何判断一个目标网站是否采用AJAX？

balabala

## 如何爬取动态加载的资源？

这种方式方便了用户，可是对我们爬取网页内容缺造成了不便。

相对于传统的静态页面，我们在爬取页面内容时只需要简单的获取整个 HTML 文本然后对其中的内容进行匹配、提取即可。

对于采用 AJAX 的网站来说，我们查看网页源代码会发现许多我们需要的资源是需要加载请求才能从服务器返回的。比如豆瓣的电影页面：



### Selenium & PhantomJS简介

Selenium 是一个 Web 的自动化测试工具，最初是为了网站自动化测试开发的， Selenium 测试直接运行在浏览器中，就像真正的用户在操作一样。支持的浏览器包括IE（7, 8, 9, 10, 11），Mozilla Firefox，Safari，Google Chrome，Opera等。也包括 PhantomJS 。

Selenium 可以根据我们的指令，让浏览器自动加载页面，获取需要的数据，甚至是页面截屏。
安装：`pip install selenium`

官方文档：`http://selenium-python.readthedocs.io/index.html`

PhantomJS 是一个基于 Webkit 的“无界面”( headless )浏览器，它会把网站加载到内存并执行页面上的 JavaScript，因为不会展示图形界面，所以运行起来比完整的浏览器要高效。

如果我们把 Selenium 和 PhantomJS 结合在一起，就可以运行一个非常强大的网络爬虫了，这个爬虫可以处理 JavaScript、Cookie、headers，以及任何我们真实用户需要做的事情。

官方文档：`http://phantomjs.org/documentation`

下载地址： ` http://phantomjs.org/download.html`

### Selenium & PhantomJS 简单使用
#### 代码分析
```
###定位并选择门类类别和学科类别
Select(driver.find_element_by_xpath("//select[@id='mldm']")).select_by_value('zyxw')
Select(driver.find_element_by_xpath("//select[@id='yjxkdm']")).select_by_value("0854")
###点击查询按钮
driver.find_element_by_xpath("//input[@name='button']").click()
###定义爬取内容的函数，采用pyquery方法，因为研招网的学校名称和省市都在<td>标签，所以直接用<td>标签；这样虽然爬取到了有用的信息，但是也包含了许多不必要的信息，比如两个学校之间的'\ue664'；至于为什么要把'省'，'市'，"壮族自治区"等这些东西去掉，是因为后面做数据可视化的时候，'map'要求直接写省市名称不必要带省市或自治区，否则不会在地图上显示出来；最后把爬取到的信息写入txt文件
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
###定义翻页的函数，用的是xpath定位的方式，找到页码的输入位置，初始化为1，并循环执行加1操作            
def next_page():
    num = 1
    while num !=12:
        print("第%s页" %str(num))
        wait.until(EC.presence_of_element_located((By.XPATH,".//*[@id='goPageNo']"))).clear()
        wait.until(EC.presence_of_element_located((By.XPATH,".//*[@id='goPageNo']"))).send_keys(num)
        driver.find_element_by_class_name("page-btn").click()
        num += 1
        get_data()
```

```
###定义读取文件的函数，把爬取到的数据做初步整理
def read_file():
    # 在windows环境中的编码问题，指定utf-8
    with open('school.txt', 'r', encoding='utf-8') as f:
        word = []  # 空列表用来存储文本中的内容

        # readlins为分行读取文本，且返回的是一个列表，每行的数据作为列表中的一个元素：
        for word_str in f.readlines():
            # strip去除每行字符串数据两边的空白字符
            word_str = word_str.strip()
            # 对单行字符串通过空格进行分割，返回一个列表
            word_list = word_str.split(' ')
            # 将分割后的列表内容，添加到word空列表中
            word.extend(word_list)
            # print(word_list)
        return word
###定义一个空字典，并统计词语出现的次数
def clear_account(lists):
    # 定义空字典，用来存放词语和对应的出现次数
    count_dict = {}
    count_dict = count_dict.fromkeys(lists)  # 现在的lists是一个没有去重，包含所有单词的列表；fromkeys()是把列表的内容当作键值
    # 取出字典中的key，放到word_list1（去重操作）
    word_list1 = list(count_dict.keys())

    # 然后统计词语出现的次数,并将它存入count_dict字典中
    for i in word_list1:
        # lists为没有去重的那个列表，即包含所有重复单词的列表，使用count得到单词出现次数，作为value
        count_dict[i] = lists.count(i)#统计次数
    print(count_dict)
    return count_dict
###定义排序函数，并按降序排列；绘制可视化地图信息；m.add里的内容属于通用配置项，具体信息可以去查看https://05x-docs.pyecharts.org/#/zh-cn/charts_base?id=map%EF%BC%88%E5%9C%B0%E5%9B%BE%EF%BC%89
def sort_dict(count_dict):
    # 删除字典中''单词
    del [count_dict['']]
    # 排序,按values进行排序，如果是按key进行排序用sorted(wokey.items(),key=lambda d:d[0],reverse=True)

    # 使用lambda匿名函数用value排序,返回列表[('the', 45), ('function', 38)...这种形式]
    my_dict = sorted(count_dict.items(), key=lambda d: d[1], reverse=True)  # sorted函数的固定用法
    # 将列表转成字典<class 'dict'>
    my_dict = dict(my_dict)
    print(my_dict)
    value = list(my_dict.values())
    keys = list(my_dict.keys())
    # print(value)
    print(keys)
    m = Map("全国省份地图", width=600, height=400)
    m.add("", keys, value, maptype='china',
          is_visualmap=True,
          is_piecewise=True,
          visual_text_color="#000",
          visual_range_text=["", ""],
          pieces=[
              {"max": 40, "min": 20, "label": "多"},
              {"max": 20, "min": 11, "label": "中"},
              {"max": 10, "min": 0, "label": "少"},
          ])
    m
    m.render("map.html")
    return my_dict
```

## 参考链接

[AJAX-XMLHtppRequest 的前世今生](https://blog.csdn.net/J080624/article/details/84171917)

[Selenium和PhantomJS介绍](https://blog.csdn.net/qq_33689414/article/details/78631009)

[Pyhon爬虫教程](https://programmer.group/python-crawler-8-selenium-and-phantomjs-for-dynamic-html-processing.html)

[廖雪峰的官方网站](https://www.liaoxuefeng.com/wiki/1022910821149312/1023022332902400)
