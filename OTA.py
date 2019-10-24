#coding=UTF-8
import requests
import time
import json

OTA_URL = "https://e284310075456279d8ec73ee0e56279bappservice.ibroadlink.com/device/control/v2/sdkcontrol"

OTA_HEADER = {"loginsession":"2ac20f49b57eb076ae6cb98b7af3bfbf","lid":"e284310075456279d8ec73ee0e56279b","licenseid":"e284310075456279d8ec73ee0e56279b","userid":"000bc1360fce09b355243481eb037e81"}

#循环升级固件版本1 
OTA_BODYDATA1 = {"directive":{"header":{"namespace":"DNA.TransmissionControl","name":"commonControl","interfaceVersion":"2","messageId":"00000000000000000000c8f742fe2ba8-1568085454"},"endpoint":{"devicePairedInfo":{"did":"00000000000000000000c8f742fe2ba8","pid":"0000000000000000000000005e5f0000","mac":"c8:f7:42:fe:2b:a8","cookie":"eyJkZXZpY2UiOnsiaWQiOjEsImtleSI6ImNkNTdhZDMxODIyOGY1MTIzNWMyY2IxNjA4Y2U3OTNlIiwiYWVza2V5IjoiY2Q1N2FkMzE4MjI4ZjUxMjM1YzJjYjE2MDhjZTc5M2UiLCJkaWQiOiIwMDAwMDAwMDAwMDAwMDAwMDAwMGM4Zjc0MmZlMmJhOCIsInBpZCI6IjAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDVlNWYwMDAwIiwibWFjIjoiYzg6Zjc6NDI6ZmU6MmI6YTgifX0="},"endpointId":"00000000000000000000c8f742fe2ba8","cookie":{}},"payload":{"data":"agAAAGh0dHA6Ly80Mi4xNTkuMjI3Ljc4L1NNQVJUU09DS0VULTU0MDQ3LTU5ODEtQkwtRkMtMjM5OC51cGQuYmluAAAAAAAAAAAAAAAAAAA48SacEAAAAOgBJ5xAAAAAAAAAAADQqZxboNG2ANCpnLDqZVgVq8yyggEAAA==","notpadding":1}}}

RETURNDATA1 = "aAAAAB/TAAAf0wAAAAAAAA=="

#循环升级固件版本2
OTA_BODYDATA2 = {"directive":{"header":{"namespace":"DNA.TransmissionControl","name":"commonControl","interfaceVersion":"2","messageId":"00000000000000000000c8f742fe2ba8-1568096055"},"endpoint":{"devicePairedInfo":{"did":"00000000000000000000c8f742fe2ba8","pid":"0000000000000000000000005e5f0000","mac":"c8:f7:42:fe:2b:a8","cookie":"eyJkZXZpY2UiOnsiaWQiOjEsImtleSI6ImNkNTdhZDMxODIyOGY1MTIzNWMyY2IxNjA4Y2U3OTNlIiwiYWVza2V5IjoiY2Q1N2FkMzE4MjI4ZjUxMjM1YzJjYjE2MDhjZTc5M2UiLCJkaWQiOiIwMDAwMDAwMDAwMDAwMDAwMDAwMGM4Zjc0MmZlMmJhOCIsInBpZCI6IjAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDVlNWYwMDAwIiwibWFjIjoiYzg6Zjc6NDI6ZmU6MmI6YTgifX0="},"endpointId":"00000000000000000000c8f742fe2ba8","cookie":{}},"payload":{"data":"agAAAGh0dHA6Ly80Mi4xNTkuMjI3Ljc4L1NNQVJUU09DS0VULTQ2MDQ3LTU5ODEtQkwtRkMtMjM5My51cGQuYmluAAAAAAAAAAAAAAAAAAA4kYGcEAAAAOihgZxAAAAAAAAAAACQ3JxboNG2AJDcnLDqZVgVW8yyggEAAA==","notpadding":1}}}

RETURNDATA2 = "aAAAAN+zAADfswAAAAAAAA=="

#查询固件版本号
QUERYDATA = {"directive":{"header":{"namespace":"DNA.TransmissionControl","name":"commonControl","interfaceVersion":"2","messageId":"00000000000000000000c8f742fe2ba8-1568098206"},"endpoint":{"devicePairedInfo":{"did":"00000000000000000000c8f742fe2ba8","pid":"0000000000000000000000005e5f0000","mac":"c8:f7:42:fe:2b:a8","cookie":"eyJkZXZpY2UiOnsiaWQiOjEsImtleSI6ImNkNTdhZDMxODIyOGY1MTIzNWMyY2IxNjA4Y2U3OTNlIiwiYWVza2V5IjoiY2Q1N2FkMzE4MjI4ZjUxMjM1YzJjYjE2MDhjZTc5M2UiLCJkaWQiOiIwMDAwMDAwMDAwMDAwMDAwMDAwMGM4Zjc0MmZlMmJhOCIsInBpZCI6IjAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDVlNWYwMDAwIiwibWFjIjoiYzg6Zjc6NDI6ZmU6MmI6YTgifX0="},"endpointId":"00000000000000000000c8f742fe2ba8","cookie":{}},"payload":{"data":"aAAAAA==","notpadding":1}}}

VERSION1 = "57048"
VERSION2 = "46047"
MAC = "_c8f742fe2ba8"

class httpResquests:
	
	def __init__(self,url,data,headers):
		self.url = url
		self.data = data
		self.headers = headers
	def httpPost(self,_url,_data,_headers):
		r = requests.post(_url,data=json.dumps(_data),headers=_headers)
		return r.text


if __name__ == "__main__":

	timestamp = time.time()
	timeArray = time.localtime(timestamp)
	otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", timeArray)
	file = "/usr/local/error/OTA/ota_" + otherStyleTime + MAC + ".txt"
	f = open(file,"a+")
	version = ""
	returnstr = ""
	currentversion = ""
	otaversion = ""
	count = 0
	for i in range(0,2):
		count = count + 1
		if(count%2):
			ota1 = httpResquests(OTA_URL,OTA_BODYDATA2,OTA_HEADER)
			returnstr = ota1.httpPost(OTA_URL,OTA_BODYDATA2,OTA_HEADER)
			version = RETURNDATA2
			currentversion = VERSION1
			otaversion = VERSION2	
		else:
			ota2 = httpResquests(OTA_URL,OTA_BODYDATA1,OTA_HEADER)
			returnstr = ota2.httpPost(OTA_URL,OTA_BODYDATA1,OTA_HEADER)
			version = RETURNDATA1
			currentversion = VERSION2
                        otaversion = VERSION1
		time.sleep(60)
		query = httpResquests(OTA_URL,QUERYDATA,OTA_HEADER)
		querystr = query.httpPost(OTA_URL,QUERYDATA,OTA_HEADER)
		timestamp1 = time.time()
		timeArray1 = time.localtime(timestamp1)
		otherStyleTime1 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray1)
		f.writelines(otherStyleTime1+"\n")
		f.writelines("第"+str(count)+"次升级：\n")
		f.writelines("当前版本："+currentversion+"      ")
		f.writelines("升级版本："+otaversion+"\n")		
		if querystr.find(version)>0:
			f.writelines("升级结果：成功\n")
		else:
			f.writelines("升级结果：失败\n")
		time.sleep(10)
