import os
import csv
import string
import time
import json

def building(ap):
    info = ap.split("-")
    return info[0]

def room(ap):
    info = ap.split("-")
    if len(info) >= 2:
        return info[1]
    else:
        return ""
    
    
def main():

    for root, dirs, files in os.walk('./5csv_realtime'):
        
        for filename in files:
            
            reader = csv.reader(open(root + '/' + filename))

            output = open('D:/workspace/Visualization/5json_realtime/' + filename + '.json', 'a')
            
            output.write('[')

            data_dict = {}

            reader.next()
            for AP_Name,associationTime,clientMacAdd in reader:


                if len(AP_Name) < 1:
                    continue
                    
                data_dict['clientMacAdd'] = clientMacAdd
                data_dict['associationTime'] = associationTime
                data_dict['building'] = building(AP_Name)
                data_dict['room'] = room(AP_Name)

                json.dump(data_dict, output)
                output.write(',')

            json.dump(data_dict, output)
            output.write(']')
            output.close()


if __name__ == '__main__':
    main()
