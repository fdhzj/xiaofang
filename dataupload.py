# coding=utf-8
import requests
import json
import sys
import time
import base64
import combile
reload(sys)
sys.setdefaultencoding('utf8')

MAC = "780f77e6781b"

PID = "00000000000000000000000068750000"

KEY = "82a4be1da34d071f1b71111693941b0d"

COUNT = 3

upload_url = "https://faqsupport-chn.ibroadlink.com/cybereye/queryissue"

upload_data = {"servicename":"serv_devmonitor_v2","start":"2019-10-22_18:30:33","end":"2019-10-23_18:30:33","queryCondition":[{"key":"mac","value":"780f77e6781b"}],"offset":0,"step":15}

CONTROL_URL = "https://e284310075456279d8ec73ee0e56279bappservice.ibroadlink.com/device/control/v2/sdkcontrol"

CONTROL_HEADER = {"lid":"e284310075456279d8ec73ee0e56279b","loginsession":"336bb1b38829bf9b551ec1112dbe381a","licenseid":"e284310075456279d8ec73ee0e56279b","userid":"000bc1360fce09b355243481eb037e81"}

OPENSTATUS = '\"pwr\":1'
CLOSESTATUS = '\"pwr\":0'

class httpResquest:

        def httpPost(self,_url,_data):
                r = requests.post(_url,data=json.dumps(_data))
                return r.text

        def httpPost1(self,_url,_data,_headers):
                r = requests.post(_url,data=json.dumps(_data),headers = _headers)
                return r.text 

class dataOut:

        def __init__(self,str,name):
                self.str = str
                self.name = name

        def index_find(self,str,name):
                spot = []
                len2 = len(name)
                address = 0
                count = 0
                while str.find(name)>0 :
                        count = count + 1
                        index = str.find(name) + len2
                        address = index + address
                        str = str[index:]
                        if(count%2==0):
                                spot.append(address-len2)
                return spot

        def index1_find(self,str,name):
                spot = []
                len2 = len(name)
                address = 0
                while str.find(name)>0:
                        index = str.find(name) + len2
                        address = address +index
                        str = str[index:]
                        spot.append(address-len2)
                return spot

        def data_need(self,str,index):
                len1 = len(index)
                data = []
                for i in range(0,len1):
                        address = index[i]
                        count = 0
                        head = 0
                        tail = 0

                        while tail==0:
                                if(str[address]==':')&(count==0):      
                                        head = address + 2
                                        count = 1
                                        address = address + 2
                                elif((str[address]=='"') & (count==1)):
                                        tail = address
                                else:
                                        address = address + 1 
                        data.append(str[head:tail])
                return data

        def data_int(self,str,index):
                len1 =len(index)
                data = []
                for i in range(0,len1):
                        address = index[i]
                        head = 0
                        tail = 0

                        while tail ==0:
                                if(str[address]==':'):
                                        head = address+1
                                        address = address + 1
                                elif(str[address]==','):
                                        tail = address
                                elif(str[address]=='}'):
                                        tail = address
                                else:
                                        address = address + 1
                        data.append(str[head:tail])
                return data

class dataupload_init:
         
        def control_init(self):
                cmd = combile.constitute().calsumdata2("{}")
                cmd = "".join(base64.b64encode(cmd))
                headcmd = cmd + "".join(base64.b64encode("{}"))
                headcmd = combile.constitute().commandconstitute(MAC,PID,KEY,headcmd)
		headcmd =json.loads(headcmd)
                init_data = httpResquest().httpPost1(CONTROL_URL,headcmd,CONTROL_HEADER)
                data1 = dataOut(init_data,"data")
                index = data1.index_find(init_data,"data")
                dataNeed = "".join(data1.data_need(init_data,index))
                return base64.b64decode(dataNeed)

        def control(self,f):
                returndata = dataupload_init().control_init()
                controltime = []
		controldata1 = ""
		controldata2 = ""
		controldata = ""
                if returndata.find(OPENSTATUS)>0:
                        cmd = combile.constitute().calsumdata('{"pwr":0}')
                        headcmd = "".join(base64.b64encode(cmd)) + "".join(base64.b64encode('{"pwr":0}'))
			headcmd = combile.constitute().commandconstitute(MAC,PID,KEY,headcmd)
                        controldata1 = headcmd
			cmd = combile.constitute().calsumdata('{"pwr":1}')
                        headcmd = "".join(base64.b64encode(cmd)) + "".join(base64.b64encode('{"pwr":1}'))
                        headcmd = combile.constitute().commandconstitute(MAC,PID,KEY,headcmd)
                        controldata2 = headcmd
			controldata = controldata1
                else:
                        cmd = combile.constitute().calsumdata('{"pwr":1}')
                        headcmd = "".join(base64.b64encode(cmd)) + "".join(base64.b64encode('{"pwr":1}'))
			headcmd = combile.constitute().commandconstitute(MAC,PID,KEY,headcmd)
                        controldata2 = headcmd
			cmd = combile.constitute().calsumdata('{"pwr":0}')
                        headcmd = "".join(base64.b64encode(cmd)) + "".join(base64.b64encode('{"pwr":0}'))
                        headcmd = combile.constitute().commandconstitute(MAC,PID,KEY,headcmd)
                        controldata1 = headcmd
			controldata = controldata2
                for i in range(0,3):
                        time.sleep(15)
                        data = "data"
                        count = 0
                        while count==0:
				controldata3 = json.loads(controldata)
				print(controldata3)
                                data = httpResquest().httpPost1(CONTROL_URL,controldata3,CONTROL_HEADER)
                                if(data.find("data")>0):
                                        count = 1
                        timestamp = time.time()
                        controltime.append(long(timestamp))
                        timeArray = time.localtime(timestamp)
                        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                        if controldata == controldata1:
                                controldata = controldata2
                        else:
                                controldata = controldata1
                        f.write("第"+str(i+1)+"次模块开关控制时间点："+ otherStyleTime+"\n")
                return controltime

        def upload_init(self):
                str1 = httpResquest().httpPost(upload_url,upload_data)
                data1 = dataOut(str1,"msgtype")
                msgtype_index = data1.index1_find(str1,"msgtype")
                msgtype = data1.data_int(str1,msgtype_index)
                len1 = len(msgtype)
                index = []
                for i in range(0,len1):
                        if msgtype[i]=="54":
                                index.append(i)
                        else:
                                pass
                return index

        def timeout(self,index,f):
                len1 = len(index)
                timeout = []
                str1 = httpResquest().httpPost(upload_url,upload_data)
                data1 = dataOut(str1,"occurtime")
                occurtime_index = data1.index_find(str1,"occurtime")
                occurtime = data1.data_need(str1,occurtime_index)
                for i in range(len1-1,-1,-1):
                        timeout.append(occurtime[index[i]])
                        f.write("第"+str(COUNT-i)+"次上报时间："+occurtime[index[i]]+"\n")
                return timeout

        def subindexout(self,index,f):
                len1 = len(index)
                subindexout = []
                str1 = httpResquest().httpPost(upload_url,upload_data)
                data1 = dataOut(str1,"subindex")
                subindex_index = data1.index1_find(str1,"subindex")
                subindex = data1.data_int(str1,subindex_index)
                for i in range(len1-1,-1,-1):
                        subindexout.append(subindex[index[i]])
                        f.write("第"+str(COUNT-i)+"次上报序号："+subindex[index[i]]+"\n")
                return subindexout

if __name__ == "__main__":
        timestamp = time.time()
        timeArray = time.localtime(timestamp)
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", timeArray)
        file = "/usr/local/error/dataupload/dataupload_" + otherStyleTime + MAC + ".txt"
        f = open(file,"a+")
        controltime = dataupload_init().control(f)
        time.sleep(120)
        index = dataupload_init().upload_init()
        occurtime = dataupload_init().timeout(index,f)
        subindex = dataupload_init().subindexout(index,f)
        f.close()
