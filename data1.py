import os
import csv
import pylab as plt


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


def main():
	personinfo = []
	reader = csv.reader(open(r"D:\workspace\Visualization\Teachers_roaming_day_0307_0414\20170406.csv"))
	reader.next()
	for Client_Username,ClientIPAddress,clientMacAdd,associationTime,vendor,AP_Name,Device_Name,SSID,Profile,vlanID,protocol,sessionDuration,avgThroughput,byteSent,byteReceived,Mobility_Status,RSSI,APIPAddress,ClientType in reader:
				
		data_dict = {}

		data_dict['clientMacAdd'] = clientMacAdd
		data_dict['AP_Name'] = AP_Name
		data_dict['associationTime'] = associationTime
		data_dict['vlanID'] = vlanID
		data_dict['protocol'] = protocol
		data_dict['avgThroughput'] = avgThroughput
		data_dict['byteSent'] = byteSent
		data_dict['byteReceived'] = byteReceived
		data_dict['RSSI'] = RSSI
		data_dict['sessionDuration'] = sessionduration2num(sessionDuration)
		try:
			_throughput = float(avgThroughput)
			data_dict['avgThroughput'] = _throughput
		except Exception, e:
			data_dict['avgThroughput'] = 0.1
		personinfo.append(data_dict)
		
	output = open('D:\workspace\Visualization\complete data\ing\out1.csv', 'a')
	for i in personinfo[0]:
		output.write(','+str(i))
	output.write('\n')
	for info in personinfo:
		for i in info:
			output.write(','+str(info[i]))
		output.write('\n')

if __name__ == '__main__':
	main()