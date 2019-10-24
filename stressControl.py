#coding=UTF-8 
import requests
import time
import json
import sys

CONTROL_URL = "https://e284310075456279d8ec73ee0e56279bappservice.ibroadlink.com/device/control/v2/sdkcontrol"

CONTROL_HEADER = {"lid":"e284310075456279d8ec73ee0e56279b","loginsession":"2ac20f49b57eb076ae6cb98b7af3bfbf","licenseid":"e284310075456279d8ec73ee0e56279b","userid":"000bc1360fce09b355243481eb037e81"}

CONTROL_BODY = {"directive":{"header":{"namespace":"DNA.TransmissionControl","name":"commonControl","interfaceVersion":"2","messageId":"00000000000000000000c8f742fe2ba8-1568013657"},"endpoint":{"devicePairedInfo":{"did":"00000000000000000000c8f742fe2ba8","pid":"0000000000000000000000005e5f0000","mac":"c8:f7:42:fe:2b:a8","cookie":"eyJkZXZpY2UiOnsiaWQiOjEsImtleSI6ImNkNTdhZDMxODIyOGY1MTIzNWMyY2IxNjA4Y2U3OTNlIiwiYWVza2V5IjoiY2Q1N2FkMzE4MjI4ZjUxMjM1YzJjYjE2MDhjZTc5M2UiLCJkaWQiOiIwMDAwMDAwMDAwMDAwMDAwMDAwMGM4Zjc0MmZlMmJhOCIsInBpZCI6IjAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDVlNWYwMDAwIiwibWFjIjoiYzg6Zjc6NDI6ZmU6MmI6YTgifX0="},"endpointId":"00000000000000000000c8f742fe2ba8","cookie":{}},"payload":{"data":"paVaWsLDAgsJAAAAeyJwd3IiOjB9","notpadding":0}}}

MAC = "_c8f742fe2ba8"

count =0
sucess = 0
fail = 0
sucessprecent = 0
error = ""
timestamp = time.time()
timeArray = time.localtime(timestamp)
otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", timeArray)
file = "/usr/local/error/controlstress/control_" + otherStyleTime + MAC + ".txt" 
f = open(file,"a+")
amount = 0
for i in range(0,10):
	time.sleep(0.3)
	time1 = time.time()
	r = requests.post(CONTROL_URL,data=json.dumps(CONTROL_BODY),headers=CONTROL_HEADER)
	return_str = r.text
	time2 = time.time()
	interval = (time2 -time1)*1000
	count = count + 1
	if(return_str.find("data")>0):
		sucess = sucess + 1
	else:
		fail = fail + 1
		timestamp1 = time.time()
		timeArray1 = time.localtime(timestamp1)
		otherStyleTime1 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray1)
		print(otherStyleTime1)
                f.writelines(otherStyleTime1+"    ")
		errorlog = '第' + str(count) + '次控制失败返回' 
		f.writelines(errorlog)
		f.write("\n")
		f.writelines(r.text)
		f.write("\n")
	sucessprecent =round(float(sucess)/count,4)
	amount = interval + amount
avg = round(amount/count,2)
sum = '一共执行:' + str(count) + '次,' + '成功:' + str(sucess) +'次,' + '失败:' + str(fail) + '次,' + '成功率:' + str(sucessprecent*100) + '%，' + '平均响应时间：' + str(avg) + 'ms'
f.writelines(sum)
f.write("\n")
f.close()
