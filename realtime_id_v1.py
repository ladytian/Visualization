#coding:utf-8
import urllib2
import base64
import ssl
from xml.etree import ElementTree as ET
import pandas as pd
from datetime import datetime
#import time
import argparse

#to get the XML files when given a url and return the string of the files content.
def get_xml(url):
    
    req=urllib2.Request(url)

    username = 'prog'
    password = 'Jsj60216926'
    base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
    authheader =  "Basic %s" % base64string
    req.add_header("Authorization", authheader)

    context = ssl._create_unverified_context()
    handle = urllib2.urlopen(req, context=context)
    thepage = handle.read() 
    #print thepage
    
    return thepage


# to get a specific property content in a XML file when given the text，label path and attribute name and return a list.
def read_xml(text, tag, attribute):
    
    lt_1 = []
    root = ET.fromstring(text)  # read the xml file
    #print root.tag, "---", root.attrib
    
    for item in root.findall(tag):
        lt_1.append(item.get(attribute))
    #print len(lt_1)
    
    return lt_1


# to parse the file when given a list of urls to get the desired data field and return a tuple of several lists.
def read_data(lt):
    
    dirs = 'entity/clientDetailsDTO/'
    fields = ['macAddress', 'associationTime', 'apName', 'throughput', 'rssi', 'status'] # for v1
    #fields = ['macAddress', 'associationTime', 'apName', 'status'] # for v2
   
    #for j in range(0,10):
    for j in range(len(lt)): 
        try:
            page = get_xml(lt[j])
            #print page
            #print j, lt[j]

            root = ET.fromstring(page)
            #print j, root.tag, root.text

            for i in range(len(fields)):
                for item in root.findall(dirs + fields[i]):
                    if i == 0:
                        lt_clientmac.append(item.text)
                    elif i == 1:
                        lt_assotime.append(item.text)
                    elif i == 2:
                        lt_apname.append(item.text)
                    elif i == 5:
                        lt_status.append(item.text)
                    elif i == 3:
                        lt_throughput.append(item.text)
                    elif i == 4:
                        lt_rssi.append(item.text)

            if lt_clientmac[-1] == "" or lt_assotime[-1] == "" or lt_apname[-1] == "" or lt_status[-1]== "" or lt_throughput[-1] == "" or lt_rssi[-1] == "":
                print "Warning: None value! The error url is " + lt[j] + " The data I have got is [" + lt_clientmac[-1] + "," + lt_assotime[-1] + "," + lt_apname[-1] + "," + lt_status[-1] + "," + lt_throughput[-1] + "," + lt_rssi[-1] + "]" 
                
                lt_clientmac.pop(-1)
                lt_assotime.pop(-1)
                lt_apname.pop(-1)
                lt_status.pop(-1)
                lt_throughput.pop(-1)
                lt_rssi.pop(-1)

            #raise Exception("Test error!", j)
            
        except Exception:
            print "Warning: Read false! An error occurred in the url " + lt[j] 
                    
    last_id = read_xml(page, 'entity/clientDetailsDTO', 'id')[0]
                    
    #print [lt_clientmac, lt_assotime, lt_apname, lt_throughput, lt_rssi]
    return [lt_clientmac, lt_assotime, lt_apname, lt_throughput, lt_rssi, lt_status],last_id


# to store the data in the CSV file according to the field given the tuple of data lists.
def get_csv(lt):

    if len(lt[0]) == len(lt[1]) == len(lt[2]) == len(lt[3]) == len(lt[4]) == len(lt[5]):
    #if len(lt[0]) == len(lt[1]) == len(lt[2]) == len(lt[3]):
        
        df = pd.DataFrame({'clientMacAdd':lt[0], 'associationTime':lt[1], 'AP_Name':lt[2], 'throughput':lt[3], 'rssi':lt[4], 'status':lt[5]}) # for v1
      
        #df.sort_values(by=['associationTime'], ascending=True)

        #df.to_csv(r".\5csv_realtime" + "\\" + str(datetime.now().strftime('%Y%m%d%H%M%S')) + ".csv",index=False,sep=',', mode='w')
        df.to_csv(r"./csv_realtime" + "/" + str(datetime.now().strftime('%Y%m%d%H%M%S')) + ".csv",index=False,sep=',', mode='w')         
        #print df.head(5)

    else:
        print "Warning: Lists have different length!"
    
    #return dfs
    

def main():
    
    try:
        n_k = 0 if args.n_k == None else args.n_k
        n_count = 100 if args.n_count == None else args.n_count
        maxid = 3002692800 if args.n_count == None else args.maxid
        
        #v1:slow and v2:fast
        #theurl = 'https://192.168.16.203/webacs/api/v2/data/ClientDetails/'
        theurl = 'https://192.168.16.203/webacs/api/v1/data/ClientDetails/'
        #<queryResponse last="99" first="0" count="33863" maxid=2993645213 3002692911 minid=3302954
       
        k = 0
        while(True): # counts = k * counts, n_files = k
            
            print "k=%d" % k
            
            count = 0
            data_list = []
            read_last_id = ""
            param = '?id=gt(0)'
            #param = '?id=gt(0)&status="ASSOCIATED"'
            #param = '?.sort=+id'
            
            global lt_clientmac
            lt_clientmac = []
            global lt_assotime
            lt_assotime = []
            global lt_apname
            lt_apname = []
            global lt_status
            lt_status = []
            global lt_throughput
            lt_throughput = []
            global lt_rssi
            lt_rssi = []
          
            while(count < n_count): # counts = count*100
                
                print "count=%d" % count
                print "read_last_id=" + str(read_last_id)
                #print theurl + param
                print datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                url_list = read_xml(get_xml(theurl + param), "entityId", "url")
                #print len(url_list), url_list
                data_list, read_last_id = read_data(url_list)

                if int(read_last_id) >= maxid:
                    break
                
                #param = '?id=gt(' + read_last_id + ')&status="ASSOCIATED"'
                param = '?id=gt(' + read_last_id + ')'  
                count = count + 1
                
            get_csv(data_list)
            
            k = k+1
            if k == n_k:
                break

            #raise Exception()

    except Exception:
        print "Warning: An error occurred in the k=" + str(k) + " and count=" + str(count) + " and maybe there was an error when writing a csv file!"
    else:
        print "Congratulations! Success!"

if __name__ == '__main__':
    
    global args
    lt_clientmac = []
    lt_assotime = []
    lt_apname = []
    lt_status = []
    lt_throughput = []
    lt_rssi = []
    
    argsparser =  argparse.ArgumentParser()
    argsparser.add_argument("-n_count",type=int,default=100)
    argsparser.add_argument("-n_k",type=int,default=0)
    argsparser.add_argument("-maxid",type=int,default=3002692800)
    args = argsparser.parse_args()

    main()
