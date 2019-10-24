#coding=UTF-8
import time
import requests
import base64
import combile
import json

STARTTIME = "2019-9-16 20:00:00"

INTERVAL = 3

MAC = "780f77e6781b"

PID = "00000000000000000000000068750000"

KEY = "82a4be1da34d071f1b71111693941b0d"

TIMER_URL = "https://e284310075456279d8ec73ee0e56279bappservice.ibroadlink.com/device/control/v2/sdkcontrol"

TIMER_HEADER = {"lid":"e284310075456279d8ec73ee0e56279b","loginsession":"336bb1b38829bf9b551ec1112dbe381a","licenseid":"e284310075456279d8ec73ee0e56279b","userid":"000bc1360fce09b355243481eb037e81"}


class base64encode:

        def encode64(self,data):
                strdata = base64.b64encode(data)
                returndata = "".join(strdata)
                return returndata

	def totalindex(self,data):
		indexhead = data.find("total")
		data1 = data[indexhead+6:]
		indexfeet = data1.find(",")
		total = data1[:indexfeet]
		return total

        def totalnumber(self,data):
		strdata = json.loads(data)
		strdata = strdata["event"]["payload"]["data"]
                strdata1 = "".join(base64.b64decode(strdata[16:]))
                strdata1 = base64encode().totalindex(strdata1)
                return strdata1

class httpRequests:

        def httpPost(self,_url,_data,_headers):
                r = requests.post(_url,data=json.dumps(_data),headers=_headers)
                return r.text

class timerSet:

        def settime(self,i):
                stamp_array = time.strptime(STARTTIME,'%Y-%m-%d %H:%M:%S')
                stamp = int(time.mktime(stamp_array))+i*60*INTERVAL
                date = time.localtime(stamp)
                timer = time.strftime('%Y-%m-%d %H:%M:%S',date)
                return timer

        def timerMake(self,i):
                stamp_array = time.strptime(STARTTIME,'%Y-%m-%d %H:%M:%S')
                stamp = int(time.mktime(stamp_array))+i*60*INTERVAL
                date = time.localtime(stamp)
                timeyear = time.strftime('%Y',date)
                timemonth = time.strftime('%m',date)
                timeday = time.strftime('%d',date)
                timehour = time.strftime('%H',date)
                timeminute = time.strftime('%M',date)
                timesecond = time.strftime('%S',date)
                timelist = timesecond + "_" + timeminute + "_" + timehour + "_" + timeday + "_" + timemonth + "_*_" + timeyear 
                return timelist

        def commontimer(self,i,cmd,type):
                settime = timerSet().timerMake(i)
                com_time = '{"did":"00000000000000000000'+MAC+'","act":'+type+',"timerlist":[{"type":"comm","id":0,"en":1,"name":"comm","time":"'+settime+'","cmd":"'+cmd+'"}]}'
                com_time64 = base64.b64encode(com_time)
                return "".join(com_time64)


        def inquire(self,mac,pid,key):
                data = "paVaWrPBAQsCAAAAe30="
                inquire = combile.constitute().commandconstitute(mac,pid,key,data)
                return inquire

        def timerdata(self,i,cmd,mac,pid,key,type):
                data = timerSet().commontimer(i,cmd,type)
                data1 ="".join(base64.b64decode(data))
                data1 = combile.constitute().calsumdata1(data1)
                data = base64encode().encode64(data1) + data
                timerdata = combile.constitute().commandconstitute(mac,pid,key,data)
                return timerdata

        def maxtimerset(self,f):
                cmd1 = '{"pwr":1}'
                cmd2 = '{"pwr":0}'
                cmd = cmd1
                for i in range(1,49):
                        headercmd = base64encode().encode64(combile.constitute().calsumdata(cmd)) + base64encode().encode64(cmd)
                        data = timerSet().timerdata(i,headercmd,MAC,PID,KEY,"0")
			data = json.loads(data)
                        returnstr = ""
                        while(returnstr.find("data")<0):
				time.sleep(2)
                                returnstr = httpRequests().httpPost(TIMER_URL,data,TIMER_HEADER)
			f.writelines("第"+str(i)+"组定时设置成功，定时时间"+timerSet().settime(i)+" 执行动作："+cmd+"\n")
                        if(cmd==cmd1):
                                cmd = cmd2
                        else:
                                cmd = cmd1

        def deletetimer(self,f):
                for i in range(0,48):
                        data = '{"did":"00000000000000000000'+MAC+'","act":1,"timerlist":[{"type":"comm","id":'+str(i)+'}]}'
                        data1 = base64encode().encode64(combile.constitute().calsumdata1(data))+base64encode().encode64(data)
                        jsondata = combile.constitute().commandconstitute(MAC,PID,KEY,data1)
			jsondata = json.loads(jsondata)
                        returnstr = ""
                        while(returnstr.find("data")<0):
				time.sleep(2)
                                returnstr = httpRequests().httpPost(TIMER_URL,jsondata,TIMER_HEADER)
				print(returnstr)
                        f.writelines("第"+str(i+1)+"组定时删除成功\n")

        def inquiretimer(self,f):
                data = '{"did":"00000000000000000000'+MAC+'","act":3,"type":"comm","count":100,"index":0}'
                data1 = base64encode().encode64(combile.constitute().calsumdata1(data))+base64encode().encode64(data)
                jsondata = combile.constitute().commandconstitute(MAC,PID,KEY,data1)
		jsondata1 = json.loads(jsondata)
                returnstr = ""
                while(returnstr.find("data")<0):
			time.sleep(1)
                        returnstr = httpRequests().httpPost(TIMER_URL,jsondata1,TIMER_HEADER)
                total = base64encode().totalnumber(returnstr)
                f.writelines("一共添加了"+str(total)+"组定时\n")

        def modifytimer(self,f):
		cmd = '{"pwr":1}'
		headercmd = base64encode().encode64(combile.constitute().calsumdata(cmd)) + base64encode().encode64(cmd)
                data = timerSet().timerdata(49,headercmd,MAC,PID,KEY,"2")
		data = json.loads(data)
                returnstr = ""
                while(returnstr.find("data")<0):
                        returnstr = httpRequests().httpPost(TIMER_URL,data,TIMER_HEADER)
                f.writelines("第"+str(1)+"组定时修改成功，定时时间"+timerSet().settime(1)+" 执行动作："+cmd+"\n")

if __name__ == "__main__":
        timestamp = time.time()
        timearray = time.localtime(timestamp)
        logtime = time.strftime('%Y_%m_%d_%H_%M_%S',timearray)
        file = "/usr/local/error/common_timer/common_timer_"+logtime+MAC+".log"
        f = open(file,"a")
	timerSet().maxtimerset(f)
	time.sleep(2)
	timerSet().modifytimer(f)
	time.sleep(2)
	timerSet().inquiretimer(f)
	time.sleep(2)
	timerSet().deletetimer(f)
        f.close()
