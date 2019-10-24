# coding=utf-8
import requests
import time
import json

QUERYDATA = {"directive":{"header":{"namespace":"DNA.TransmissionControl","name":"commonControl","interfaceVersion":"2","messageId":"00000000000000000000c8f742fe2bae-1568265957"},"endpoint":{"devicePairedInfo":{"did":"00000000000000000000c8f742fe2bae","pid":"0000000000000000000000005e5f0000","mac":"c8:f7:42:fe:2b:ae","cookie":"eyJkZXZpY2UiOnsiaWQiOjEsImtleSI6ImRhZDkyNzY2OGZhYTZmNDdhMTlhY2MzNjU3NmIxNDE4IiwiYWVza2V5IjoiZGFkOTI3NjY4ZmFhNmY0N2ExOWFjYzM2NTc2YjE0MTgiLCJkaWQiOiIwMDAwMDAwMDAwMDAwMDAwMDAwMGM4Zjc0MmZlMmJhZSIsInBpZCI6IjAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDVlNWYwMDAwIiwibWFjIjoiYzg6Zjc6NDI6ZmU6MmI6YWUifX0="},"endpointId":"00000000000000000000c8f742fe2bae","cookie":{}},"payload":{"data":"paVaWrPBAQsCAAAAe30=","notpadding":0}}}

QUERYURL = "https://e284310075456279d8ec73ee0e56279bappservice.ibroadlink.com/device/control/v2/sdkcontrol"

QUERYHEADER = {"userid":"000bc1360fce09b355243481eb037e81","loginsession":"2ac20f49b57eb076ae6cb98b7af3bfbf","lid":"e284310075456279d8ec73ee0e56279b","licenseid":"e284310075456279d8ec73ee0e56279b"}

MAC = "_c8f742fe2bae"

class httpRequests:

	def __init__(self,url,data,body):
		self.url = url
		self.data = data
		self.body = body
	
	def httpPost(self,_url,_data,_headers):
		r = requests.post(_url,data=json.dumps(_data),headers=_headers)
                return r.text

if __name__ =="__main__":
        timestamp = time.time()
        timeArray = time.localtime(timestamp)
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", timeArray)
        file = "/usr/local/error/cloud/cloud_" + otherStyleTime  +  MAC + ".txt"
        file1 = "/usr/local/error/cloud/cloud_error_" + otherStyleTime + MAC + ".txt"
        f = open(file,"a+")
        f1 = open(file1,"a+")
        f1.writelines("掉线时间                                        上线时间                                        持续时间\n")
	count = 0
	sum = 0
	starttime = 0
	firsttime = ""
	for i in range(0,10000):
		count = count + 1
		http1 = httpRequests(QUERYURL,QUERYDATA,QUERYHEADER)
		str1 = http1.httpPost(QUERYURL,QUERYDATA,QUERYHEADER)
		if str1.find("data")>0 and sum >= 2:
			sum = 0
			timestamp1 = time.time()
        		timeArray1 = time.localtime(timestamp1)
        		otherStyleTime1 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray1)
			f1.writelines(otherStyleTime1+"                            ")
			f1.writelines(str(timestamp1-starttime))
		elif str1.find("data")>0 and sum == 1:
			sum = 0
		elif str1.find("data")<0:
			sum = sum + 1
			timestamp1 = time.time()
                        timeArray1 = time.localtime(timestamp1)
                        otherStyleTime1 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray1)
                        f.writelines(otherStyleTime1+"       第"+str(count)+"次查询在线情况：离线\n")
			if(sum == 1):
				starttime = timestamp1
				firsttime = otherStyleTime1
			elif(sum == 2):
				f1.writelines(firsttime+"                            ")
			else:
				pass
		else:
			pass
		time.sleep(3)
	f.close()
	f1.close()		  	
