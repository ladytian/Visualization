import os
import csv
import time

def main():
	personinfo = []
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
	list_vid = []
	list_pro = []

	reader = csv.reader(open(r"D:\workspace\Visualization\complete data\ing\out3.csv"))
	reader.next()
	for clientMacAdd,associationTime,sessionDuration,breakingTime,building,room,avgThroughput,byteSent,byteReceived,RSSI,vlanID,protocol in reader:
				
		if clientMacAdd not in mac:
			data_dict['clientMacAdd'] = clientname
			data_dict['associationTime'] = list_at1
			data_dict['building'] = list_b
			data_dict['room'] = list_r
			data_dict['avgThroughput'] = list_avg
			data_dict['byteSent'] = list_bs
			data_dict['byteReceived'] = list_br
			data_dict['RSSI'] = list_rssi
			data_dict['vlanID'] = list_vid
			data_dict['protocol'] = list_pro

			print data_dict

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
			list_vid = []
			list_pro = []

			clientname = clientMacAdd

			list_at2 = []
			list_at2.append(int(time.mktime(time.strptime(associationTime,"%Y/%m/%d %H:%M"))))
			list_at2.append(int(time.mktime(time.strptime(breakingTime,"%Y/%m/%d %H:%M"))))
			list_at1.append(list_at2)
			list_b.append(building)
			list_r.append(room)
			list_avg.append(float(avgThroughput))
			list_bs.append(float(byteSent))
			list_br.append(float(byteReceived))
			list_rssi.append(RSSI)
			list_vid.append(vlanID)
			list_pro.append(protocol)


		elif clientMacAdd in mac:
			list_at2 = []
			list_at2.append(int(time.mktime(time.strptime(associationTime,"%Y/%m/%d %H:%M"))))
			list_at2.append(int(time.mktime(time.strptime(breakingTime,"%Y/%m/%d %H:%M"))))
			list_at1.append(list_at2)
			list_b.append(building)
			list_r.append(room)
			list_avg.append(float(avgThroughput))
			list_bs.append(float(byteSent))
			list_br.append(float(byteReceived))
			list_rssi.append(RSSI)
			list_vid.append(vlanID)
			list_pro.append(protocol)


		#personinfo.append(data_dict)
		
'''		
	output = open('D:\workspace\Visualization\complete data\ing\out4.csv', 'a')
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