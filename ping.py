# coding=utf-8
import sys
import os
import time

MAC = "_34ea34189d2d"

IP = "192.168.8.1"

CMD = "ping "+IP+" -c 1"

class command:

	def __init__(self,cmd):
		self.cmd = cmd

	def cmdSend(self,cmd):
		returnstr = os.popen(cmd).read()
		strdata = ""
		if returnstr.find("ttl")>0:
			head = returnstr.find("64")
			tail = returnstr.find("ms") + 2
			data = returnstr[head:tail]
		else:
			data = "From "+IP+" icmp_seq=1 Destination Host Unreachable"
		return data

	def seqInc(self,str,count):
		index = str.find("icmp_seq") + 10
		str1 = str[:index-1] + count + str[index:]
		return str1

	def dataJudge(self,str):
		if(str.find("ms")>0):
			return true
		else:
			return false

if __name__ =="__main__":
	timestamp = time.time()
        timeArray = time.localtime(timestamp)
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", timeArray)
	file = "/usr/local/error/ping/ping_" + otherStyleTime  +  MAC + ".txt"
	file1 = "/usr/local/error/ping/ping_error_" + otherStyleTime + MAC + ".txt"
	f = open(file,"a+")
	f1 = open(file1,"a+")
	f1.writelines("掉线时间                                        上线时间                                        持续时间\n")
	head = 0
	tail = 0
	flag = 0
	starttime = 0
	duration = 0
	count = 0
	for i in range(0,100):
		count = count + 1
		cmd1 = command(CMD)
		linedata = cmd1.cmdSend(CMD)
		changedata = cmd1.seqInc(linedata,str(count))
		print(changedata)
		timestamp1 = time.time()
		timeArray1 = time.localtime(timestamp1)
		otherStyleTime1 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray1)
		f.writelines(otherStyleTime1+"  "+changedata +"\n")
		if changedata.find("ms")<0 and flag == 0:
			flag = 1
			f1.writelines(otherStyleTime1+"                            ")
			starttime = timestamp1
		elif changedata.find("ms")>0 and flag == 1:
			flag = 0    
                        f1.writelines(otherStyleTime1+"                            ")
			duration = timestamp1 - starttime
			f1.writelines(str(duration) + "\n")
		else:
			pass
		time.sleep(1)
	f.close()
	f1.close()
