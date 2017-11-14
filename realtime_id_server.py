#coding:utf-8
import urllib2
import base64
import ssl
from xml.etree import ElementTree as ET
import pandas as pd
from datetime import datetime
import time
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
    #fields = ['macAddress', 'associationTime', 'apName', 'throughput', 'rssi'] # for v1
    fields = ['macAddress', 'associationTime', 'apName'] # for v2
   
    #for j in range(0,3):
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
                    #elif i == 3:
                    #    lt_throughput.append(item.text)
                    #elif i == 4:
                    #    lt_rssi.append(item.text)
                    
            #raise Exception("Test error!", j)
            
        except Exception:
            print "Error: Read false!"
                    
    last_id = read_xml(page, 'entity/clientDetailsDTO', 'id')[0]
                    
    #print [lt_clientmac, lt_assotime, lt_apname, lt_throughput, lt_rssi]
    #return [lt_clientmac, lt_assotime, lt_apname, lt_throughput, lt_rssi]
    #print [lt_clientmac, lt_assotime, lt_apname]
    return [lt_clientmac, lt_assotime, lt_apname], last_id


# to store the data in the CSV file according to the field given the tuple of data lists.
def get_csv(lt):
    
    #if len(lt[0]) == len(lt[1]) == len(lt[2]) == len(lt[3]) == len(lt[4]):
    if len(lt[0]) == len(lt[1]) == len(lt[2]):
        
        #df = pd.DataFrame({'clientMacAdd':lt[0], 'associationTime':lt[1], 'AP_Name':lt[2], 'throughput':lt[3], 'rssi':lt[4]}) # for v1
        df = pd.DataFrame({'clientMacAdd':lt[0], 'associationTime':lt[1], 'AP_Name':lt[2]}) # for v2
        
        #df.sort_values(by=['associationTime'], ascending=True)

        #df.to_csv(r".\5csv_realtime" + "\\" + str(k) + "v2_id_test.csv",index=False,sep=',', mode='w')
        #df.to_csv(r".\5csv_realtime" + "\\" + "test6.csv",index=False,sep=',', mode='a')
        #df.to_csv(r".\5csv_realtime" + "\\" + str(time.strftime('%Y%m%d%H%M%S')) + "_test.csv",index=False,sep=',', mode='w')
        df.to_csv(r"./csv_realtime" + "/" + str(time.strftime('%Y%m%d%H%M%S')) + "_test.csv",index=False,sep=',', mode='w')         
        #print df.head(5)
    
    else:
        print "Lists have different length, False!"
    
    #return df
    

def main():
    
    n_k = 0 if args.n_k == None else args.n_k
    n_count = 100 if args.n_count == None else args.n_count
    
    #v1:slow and v2:fast
    #theurl = "https://192.168.16.203/webacs/api/v2/data/ClientDetails?status="ASSOCIATED"
    #theurl = 'https://192.168.16.203/webacs/api/v2/data/ClientDetails?.sort=-associationTime&status="ASSOCIATED"'
    theurl = 'https://192.168.16.203/webacs/api/v2/data/ClientDetails/'
    #<queryResponse last="99" first="0" count="33863" 
       
    #print get_xml(theurl)
    #read_data(url_list)    
    #get_csv(read_data(url_list))
   
    k = 0
    while(True): # counts = k * counts, n_files = k
        
        print k
        
        count = 0
        data_list = []
        read_last_id = ""
        param = '?id=gt(0)&status="ASSOCIATED"'
        
        global lt_clientmac
        lt_clientmac = []
        global lt_assotime
        lt_assotime = []
        global lt_apname
        lt_apname = []
      
        while(count < n_count): # counts = count*100
            
            print count
            print datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            url_list = read_xml(get_xml(theurl + param), "entityId", "url")
            #print len(url_list)
            data_list, read_last_id = read_data(url_list)
            param = '?id=gt(' + read_last_id + ')&status="ASSOCIATED"'  
            count = count + 1
            
        get_csv(data_list)
        
        k = k+1
        if k == n_k:
            break
        
if __name__ == '__main__':
    
    global args
    lt_clientmac = []
    lt_assotime = []
    lt_apname = []
    #lt_throughput = []
    #lt_bytesreveived = []
    #lt_bytessent = []
    #lt_rssi = []
    
    argsparser =  argparse.ArgumentParser()
    argsparser.add_argument("-n_count",type=int,default=100)
    argsparser.add_argument("-n_k",type=int,default=0)
    args = argsparser.parse_args()

    main()
