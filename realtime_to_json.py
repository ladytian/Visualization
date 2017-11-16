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

    for root, dirs, files in os.walk('./5csv_realtime/csv_realtime'):
        
        for filename in files:

            #lt = []  # methods 3: return a list or you can say a string.
            
            reader = csv.reader(open(root + '/' + filename))

            output = open('D:/workspace/Visualization/5json_realtime/' + filename[0:-4] + '.json', 'a')
            #output = open('D:/workspace/Visualization/5json_realtime' + "visualization" + '.json', 'w') # methods 2: only a fixed file.
            
            output.write('[')

            data_dict = {}

            reader.next()
            for AP_Name, associationTime, clientMacAdd, status in reader:

                if len(AP_Name) < 1:
                    continue
                    
                data_dict['clientMacAdd'] = clientMacAdd
                data_dict['associationTime'] = associationTime
                data_dict['building'] = building(AP_Name)
                data_dict['room'] = room(AP_Name)
                data_dict['status'] = status

                json.dump(data_dict, output)
                output.write(',')

                #lt.append(data_dict) #methods 3

            json.dump(data_dict, output)
            output.write(']')
            output.close()

            #return lt  #methods 3

# methods 1: return a file's content.
def to_web_file():
    for root, dirs, files in os.walk('./5json_realtime'):
        
        for filename in files:
            file = open(root + '/' + filename)
            return file

if __name__ == '__main__':
    main()
    #s = main() # methods 3
    #print s[0:10] # methods 3
    #sjson = to_web_file()  # methods 1
    #print type(sjson), sjson  # methods 1

