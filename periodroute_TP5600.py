
m selenium import webdriver
from selenium.webdriver.support.select import Select
import socket
import math
import time

class test:
	def __init__(self):
		self.addr = '192.168.0.1'
	def get_ip(self):  #获取本机IP地址
		self.hostname = socket.gethostname()
		self.addr = socket.gethostbyname(self.hostname)
	def get_getway(self):   #获取本机网关地址
		self.getway = self.addr[::-1]
		location = self.getway.index(".")
		self.getway = self.getway[::-1]
		self.getway = self.getway[:(-location-1)]+".1"
		return self.getway

class webtest:
	def __init__(self):
		self.url = "http://192.168.48.1/login.html"
	def get_url(self,getway):
		self.url="http://192.168.8.1/cgi-bin/luci"  #路由器设置页面
	def login(self):
		self.driver = webdriver.Chrome()
		self.driver.get(self.url)
		time.sleep(5)
		try:
			self.driver.find_element_by_id("lgPwd").clear() 
			#self.driver.find_element_by_id("loginpassword").clear()  #判断是否需要登录密码
		except Exception as a:
			pass
		else:
			self.driver.find_element_by_id("lgPwd").send_keys("12345678") #如果需要密码输入12345678
			self.driver.find_element_by_id("loginSub").click()
			time.sleep(3)
	def test_fang(self):
		driver = self.driver
		driver.find_element_by_class_name("menu4").click()
		time.sleep(3)
		driver.find_element_by_class_name("menuLbl").click()
		time.sleep(3)
		driver.find_element_by_id("wireless2G_rsMenu").click()
		time.sleep(3)
		driver.find_element_by_id("ssid").clear()
		driver.find_element_by_id("ssid").send_keys("HeiHei")
		time.sleep(5)
		driver.find_element_by_id("save").click()
	def test_fang1(self):
		driver = self.driver
		driver.find_element_by_class_name("menu4").click()
		time.sleep(3)
		driver.find_element_by_class_name("menuLbl").click()
		time.sleep(3)
		driver.find_element_by_id("wireless2G_rsMenu").click()
		time.sleep(3)
		driver.find_element_by_id("ssid").clear()
		driver.find_element_by_id("ssid").send_keys("Fang")
		time.sleep(5)
		driver.find_element_by_id("save").click()

if __name__ == "__main__":
	address = test()
	address.get_ip()
	getway = address.get_getway()
	web_test =webtest()
	web_test.get_url(getway)
	web_test.login()
	for i in range(1, 10000):
		if(i%2==0):
			web_test.test_fang()
			time.sleep(240)
		else:
			web_test.test_fang1()
			time.sleep(240)

