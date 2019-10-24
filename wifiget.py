#coding=UTF-8
import time
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

AMOUNT = 50

URL = "http://192.168.10.1/wifiget"

class httpGet:
	
	def wifiget(self,URL):
		r = requests.get(URL)
		return r.text

if __name__ =="__main__":

	timestamp = time.time()
        timeArray = time.localtime(timestamp)
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", timeArray)
        filepath = "/usr/local/error/wifiget/wifiget_"+otherStyleTime+".log"
        f = open(filepath,"a+")
	count = 0
	for i in range(0,AMOUNT):
		count = count + 1
		time.sleep(2)
		str1 = httpGet().wifiget(URL)
		datalen = len(str1)
		s = json.loads(str1)
		s = s["list"]
		timestamp1 = time.time()
        	timeArray1 = time.localtime(timestamp1)
        	otherStyleTime1 = time.strftime("%Y_%m_%d %H:%M:%S", timeArray1)
		f.writelines(otherStyleTime1+" 第"+str(count)+"次ap列表扫描结果：\n")
		datacount = len(s)
		for i in range(0,datacount):
			ssid = s[i]
			ssid = json.dumps(ssid)
			ssid = json.loads(ssid)
			ssid = str(ssid["s"])
			print(ssid)
			f.writelines("ssid名称:" + ssid + "\n")
		f.writelines("扫描到的ap列表总长度："+str(datalen)+"\n")
