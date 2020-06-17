import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PythonOrgSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS(executable_path=r"E:\download\PhantomJS\phantomjs-2.1.1-windows\bin\phantomjs.exe")

    def test_search_in_python_org(self):#以test开头为命名
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python",driver.title)#使用assert断言的方法判断在页面标题中是否包含 “Python”
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No result found." not in driver.page_source
    def tearDown(self):
        self.driver.close()#quit 将关闭整个浏览器，而`close`只会关闭一个标签页
if __name__ == "__main__":
    unittest.main()
