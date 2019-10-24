# coding=utf-8
import time
import binascii
import base64

class constitute:

        def commandconstitute(self,mac,pid,key,data):
                timestamp = int(time.time())
                did = "00000000000000000000" + mac
                _mac = mac[0:2]+":"+mac[2:4]+":"+mac[4:6]+":"+mac[6:8]+":"+mac[8:10]+":"+mac[10:12]
                cookie = '{"device":{"id":1,"key":"'+key+'","aeskey":"'+key+'","did":"'+did+'","pid":"'+pid+'","mac":"'+_mac+'"}}'
                cookie_base64 = base64.b64encode(cookie)
                cookie_str = "".join(cookie_base64)
                jsondata = '{"directive":{"header":{"namespace":"DNA.TransmissionControl","name":"commonControl","interfaceVersion":"2","messageId":"'+did+"-"+str(timestamp)+'"},"endpoint":{"devicePairedInfo":{"did":"'+did+'","pid":"'+pid+'","mac":"'+_mac+'","cookie":"'+cookie_str+'"},"endpointId":"'+did+'","cookie":{}},"payload":{"data":"'+data+'","notpadding":0}}}'
                return jsondata

	def lencal(self,data):
		len1 = len(data)
		len1 = hex(len1)
		datalen = 0
		if len(len1)== 3:
			datalen = int(len1[2:3],16)
		elif len(len1)== 4:
			datalen = int(len1[2:4],16)
		elif len(len1)== 5:
			datalen = int(len1[2:3],16)+int(len1[3:5],16)
		else:
			datalen = int(len1[2:4],16)+int(len1[4:6],16)
		return datalen
		
	def calsumdata(self,data):
		len1 = len(data)
		len2 = constitute().lencal(data)
		if(len1<16):
    			len1 = "0"+str(hex(len1))[2:]+"00"
		elif(len1>=16 and len1<256):
    			len1 = str(hex(len1))[2:]+"00"
		elif(len1>=256 and len1<4096):
    			len1 = str(hex(len1))[3:]+"0"+str(hex(len1))[2:3]
		else:
			len1 = str(hex(len1))[4:6]+str(hex(len1))[2:4]
		e = 0
		for i in data:
    			d = ord(i)
   			e = e + d
		calsum = 165+165+90+90+2+11+len2+e+48815
		calsum = str(hex(calsum))
		calsum = calsum[4:6]+calsum[2:4]
		returndata = "a5a55a5a"+calsum+"020b"+len1+"0000"
		returndata=binascii.a2b_hex(returndata)
		return returndata

	def calsumdata2(self,data):
                len1 = len(data)
                len2 = constitute().lencal(data)
                if(len1<16):
                        len1 = "0"+str(hex(len1))[2:]+"00"
                elif(len1>=16 and len1<256):
                        len1 = str(hex(len1))[2:]+"00"
                elif(len1>=256 and len1<4096):
                        len1 = str(hex(len1))[3:]+"0"+str(hex(len1))[2:3]
                else:
                        len1 = str(hex(len1))[4:6]+str(hex(len1))[2:4]
                e = 0
                for i in data:
                        d = ord(i)
                        e = e + d
                calsum = 165+165+90+90+1+11+len2+e+48815
                calsum = str(hex(calsum))
                calsum = calsum[4:6]+calsum[2:4]
                returndata = "a5a55a5a"+calsum+"010b"+len1+"0000"
                returndata=binascii.a2b_hex(returndata)
                return returndata


	def calsumdata1(self,data):
		len1 = len(data)
                len2 = constitute().lencal(data)
                if(len1<16):
                        len1 = "0"+str(hex(len1))[2:]+"00"
                elif(len1>=16 and len1<256):
                        len1 = str(hex(len1))[2:]+"00"
                elif(len1>=256 and len1<4096):
                        len1 = str(hex(len1))[3:]+"0"+str(hex(len1))[2:3]
                else:
                        len1 = str(hex(len1))[4:6]+str(hex(len1))[2:4]
                e = 0
                for i in data:
                        d = ord(i)
                        e = e + d
                calsum = 165+165+90+90+34+11+len2+e+48815
                calsum = str(hex(calsum))
                calsum = calsum[4:6]+calsum[2:4]
                returndata = "a5a55a5a"+calsum+"220b"+len1+"0000"
                returndata = binascii.a2b_hex(returndata)
                return returndata
