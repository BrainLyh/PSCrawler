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




## 参考链接

[AJAX-XMLHtppRequest 的前世今生](https://blog.csdn.net/J080624/article/details/84171917)

[Selenium和PhantomJS介绍](https://blog.csdn.net/qq_33689414/article/details/78631009)

[Pyhon爬虫教程](https://programmer.group/python-crawler-8-selenium-and-phantomjs-for-dynamic-html-processing.html)

[廖雪峰的官方网站](https://www.liaoxuefeng.com/wiki/1022910821149312/1023022332902400)