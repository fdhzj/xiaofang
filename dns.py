#coding=UTF-8
import time
import requests 

dnslist = ["http://www.apple.com","http://captive.apple.com","http://hotspot-detect.html","http://app.com/rsp204","http://app.com/generate_204","http://com.android.captiveportallogin","http://app.com/wifi.html"]

class httpResquest:
	def httpGet(self,_url):
		r = requests.get(_url)
		return r.url

if __name__ == "__main__":
	count = len(dnslist)
	timestamp = time.time()
        timeArray = time.localtime(timestamp)
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", timeArray)	
	filepath = "/usr/local/error/dns_"+otherStyleTime+".log"
	f = open(filepath,"a+")
	for i in range(0,count):
		f.writelines("当前劫持的域名是："+dnslist[i]+"\n")
		sum=1
		success = 0
		fail = 0
		while(sum<3):
			time.sleep(3)
			timef = time.time()
			timeArrayf = time.localtime(timef)
                        otherStyleTimef = time.strftime("%Y_%m_%d_%H_%M_%S", timeArrayf)
			f.writelines("第"+str(sum)+"次H5页面请求时间："+otherStyleTimef+"\n")
			str1 = httpResquest().httpGet(dnslist[i])
			print(str1)
			if(str1.find("apconfig.html")>0):
				success = success + 1
				time2 = str(time.time()-timef)[:4]
				f.writelines("第"+str(sum)+"次H5页面获取成功响应时间："+time2+"\n")	
			else:
				print(str1)
				fail = fail + 1
				timestamp1 = time.time()
        			timeArray1 = time.localtime(timestamp1)
				otherStyleTime1 = time.strftime("%Y_%m_%d_%H_%M_%S", timeArray1)
				f.writelines("第"+str(sum)+"次H5页面获取失败\n")
			sum = sum + 1
		f.writelines("一共测试："+str(sum-1)+"次，成功获取H5页面："+str(success)+"次，失败："+str(fail)+"次\n")
