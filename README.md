# PSCrawler
 Web Crawler by Selenium
## 爬虫功能

设计思路：

作者认为在考研目标院校的选择中，地理位置占了很大一部分因素，因此

1. 查看全国各个省开设有用户目标专业的院校数量
2. 选择完地理位置之后查看这个省里各高校的大致招生情况，看看哪些是 985&211 院校
3. 选择具体高校查看都有哪些研究方向，有没有自己感兴趣的

当然，不一定要按步骤来。

 对研招网硕士目录进行爬取，三级功能实现：
 1. 全国地图：根据输入的门类类别代码，学科类别代码来绘制符合条件的高校在全国各省的分布情况

    ![img](https://wx4.sinaimg.cn/mw690/006boCb9ly1ggjyzi6tp0j30p30hc0vo.jpg)

 2. 特定省份：根据输入的省份、门类类别代码、学科类别代码来绘制符合条件的高校对应专业的拟招生人数等信息，并在控制台输出结果中的 985&211 高校名单

    ![img](https://wx3.sinaimg.cn/mw690/006boCb9ly1ggjyzlsi5kj30v60gimyy.jpg)

 3. 特定高校：根据输入的高校名称、学科类别代码来绘制该高校开设的专业数量和对应的拟招生人数

    ![img](https://wx4.sinaimg.cn/mw690/006boCb9ly1ggjyzoqyztj30vd0h1ab4.jpg)

使用环境：

selenium: `pip install selenium`

chrome driver: [需要安装对应驱动](https://sites.google.com/a/chromium.org/chromedriver/home)

pyecharts: `pip install pyecharts`
