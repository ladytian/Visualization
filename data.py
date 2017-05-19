import os
import csv
import pylab as plt
import string
import time
import json

def sessionduration2num(session_duration):
	info = session_duration.replace("hrs", " "+"hrs"+" ").replace("min", " "+"min").replace("sec", " "+"sec").split(" ")
	retval = 0
	if len(info) == 6:
		retval = int(info[0]) * 60 *60 + int(info[2]) * 60 + int(info[4])
	elif len(info) == 4:
		retval = int(info[0]) * 60 + int(info[2])
	elif len(info) == 2:
		retval = int(info[0])
	return retval

def building(ap):
	info = ap.split("-")
	return info[0]

def room(ap):
	info = ap.split("-")
	if len(info) >= 2:
		return info[1]
	else:
		return ""

def cal_time(at):
	a = at.replace(' CST ', ' ')
	info = time.mktime(time.strptime(a,"%a %b %d %H:%M:%S %Y"))
	return int(info)

def main():
	#personinfo = []


	for root, dirs, files in os.walk('./Teachers_roaming_day_0307_0414'):
		for filename in files:

			reader = csv.reader(open(root + '/' + filename))

			output = open('D:/workspace/Visualization/complete data/' + filename[0:-4] + '.json', 'a')
			output.write('[')

			data_dict = {}
			clientname =""

			mac = []
			list_at1 = []
			list_at2 = []
			list_sd = []
			list_b = []
			list_r = []
			list_avg = []
			list_bs = []
			list_br = []
			list_rssi = []
			#reader = csv.reader(open(r"D:\workspace\Visualization\Teachers_roaming_day_0307_0414\20170407.csv"))
			reader.next()
			for Client_Username,ClientIPAddress,clientMacAdd,associationTime,vendor,AP_Name,Device_Name,SSID,Profile,vlanID,protocol,sessionDuration,avgThroughput,byteSent,byteReceived,Mobility_Status,RSSI,APIPAddress,ClientType in reader:
						
				#data_dict = {}

				if len(AP_Name) < 1:
					continue

				if clientMacAdd not in mac:
					data_dict['clientMacAdd'] = clientname
					data_dict['associationTime'] = list_at1
					data_dict['sessionDuration'] = list_sd
					data_dict['building'] = list_b
					data_dict['room'] = list_r
					data_dict['avgThroughput'] = list_avg
					data_dict['byteSent'] = list_bs
					data_dict['byteReceived'] = list_br
					data_dict['RSSI'] = list_rssi

					if data_dict['clientMacAdd'] != '':
						print 1
						json.dump(data_dict, output)
						output.write(',')

					#personinfo.append(data_dict)

					mac.append(clientMacAdd)

					list_at1 = []
					list_at2 = []
					list_sd = []
					list_b = []
					list_r = []
					list_avg = []
					list_bs = []
					list_br = []
					list_rssi = []

					clientname = clientMacAdd
					
					list_sd.append(sessionduration2num(sessionDuration))
					list_at2.append(cal_time(associationTime))
					list_at2.append(cal_time(associationTime) + list_sd[-1])
					list_at1.append(list_at2)
					list_b.append(building(AP_Name))
					list_r.append(room(AP_Name))
					list_bs.append(float(byteSent))
					list_br.append(float(byteReceived))
					list_rssi.append(RSSI)

					try:
						_throughput = float(avgThroughput)
						list_avg.append(float(_throughput))
					except Exception, e:
						list_avg.append(float(0.1))


				elif clientMacAdd in mac:
					list_at2 = []
					list_sd.append(sessionduration2num(sessionDuration))			
					list_at2.append(cal_time(associationTime))
					list_at2.append(cal_time(associationTime) + list_sd[-1])
					list_at1.append(list_at2)
					list_b.append(building(AP_Name))
					list_r.append(room(AP_Name))
					list_bs.append(float(byteSent))
					list_br.append(float(byteReceived))
					list_rssi.append(RSSI)

					try:
						_throughput = float(avgThroughput)
						list_avg.append(float(_throughput))
					except Exception, e:
						list_avg.append(float(0.1))

			#print personinfo

			#	output = open('D:\workspace\Visualization\complete data\ing\out.json', 'a')
			#	for info in personinfo:
			#		json.dump(info, output)
			#		output.write('\n')
			output.write(']')
			output.close()

			'''
				data_dict['clientMacAdd'] = clientMacAdd
				data_dict['associationTime'] = cal_time(associationTime)
				#data_dict['vlanID'] = vlanID
				#data_dict['protocol'] = protocol
				data_dict['avgThroughput'] = avgThroughput
				data_dict['byteSent'] = byteSent
				data_dict['byteReceived'] = byteReceived
				data_dict['RSSI'] = RSSI

				data_dict['sessionDuration'] = sessionduration2num(sessionDuration)
				data_dict['breakingTime'] = cal_time(associationTime) + data_dict['sessionDuration']
'''
'''	
	output = open('D:\workspace\Visualization\complete data\ing\out.json', 'a')
	for i in personinfo[0]:
		output.write(','+str(i))
	output.write('\n')
	for info in personinfo:
		for i in info:
			output.write(','+str(info[i]))
		output.write('\n')

'''



if __name__ == '__main__':
	main()
