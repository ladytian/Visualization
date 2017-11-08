#coding:utf-8
import urllib2
import base64
import ssl
from xml.etree import ElementTree as ET
import pandas as pd


# to get the XML files when given a url and return the string of the files content.    
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
    root = ET.fromstring(text)
   
    for entityId in root.findall(tag):
        lt_1.append(entityId.get(attribute))
    #print len(lt_1)
    
    return lt_1


# to parse the file to get the desired data field when given a list of urls and return a tuple of several lists.
def read_data(lt):
    
    #lt_clientmac = []
    #lt_assotime = []
    #lt_apname = []
    #lt_throughput = []
    #lt_bytesreveived = []
    #lt_bytessent = []
    #lt_rssi = []
   
    #for j in range(0,10):
    for j in range(len(lt)):
        
        page = get_xml(lt[j])
        print j, lt[j]
        #print page

        root = ET.fromstring(page)
        #print j, root.tag, root.text

        dirs = 'entity/clientDetailsDTO/'
        #fields = ['macAddress', 'associationTime', 'apName', 'throughput', 'rssi'] # for v1/data/ClientDetails/****
        fields = ['macAddress', 'associationTime', 'apName'] # for v1/data/ClientDetails/****

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
                 #   lt_rssi.append(item.text)
                    
    #print [lt_clientmac, lt_assotime, lt_apname, lt_throughput, lt_rssi]
    #return [lt_clientmac, lt_assotime, lt_apname, lt_throughput, lt_rssi]
    #print [lt_clientmac, lt_assotime, lt_apname]
    return [lt_clientmac, lt_assotime, lt_apname]


# to store the data in the CSV file according to the field given the tuple of data lists.
def get_csv(lt):
    
    #if len(lt[0]) == len(lt[1]) == len(lt[2]) == len(lt[3]) == len(lt[4]): # for v1
    if len(lt[0]) == len(lt[1]) == len(lt[2]): # for v2
        
        #df = pd.DataFrame({'clientMacAdd':lt[0], 'associationTime':lt[1], 'AP_Name':lt[2], 'throughput':lt[3], 'rssi':lt[4]})
        df = pd.DataFrame({'clientMacAdd':lt[0], 'associationTime':lt[1], 'AP_Name':lt[2]})

        #df.to_csv(r".\test" + "\\" + str(k) + "test.csv",index=False,sep=',', mode='w')
        df.to_csv(r".\5csv_realtime" + "\\" + "test.csv",index=False,sep=',', mode='a')
        
        #print df.head(5)
    
    else:
        print "Read false!"
    
    #return df
        
if __name__ == '__main__':
    
    #theurl = "https://192.168.16.203/webacs/api/v2/data/ClientDetails/"
    #theurl = 'https://192.168.16.203/webacs/api/v2/data/ClientDetails?.sort=-associationTime&status="ASSOCIATED"'
    #theurl = 'https://192.168.16.203/webacs/api/v1/data/ClientDetails?id=gt(3302954)'
    
    #print get_xml(theurl)
    #read_data(url_list)    
    #get_csv(read_data(url_list))
    
    k = 0
    lt_clientmac = []
    lt_assotime = []
    lt_apname = []
    #lt_throughput = []
    #lt_bytesreveived = []
    #lt_bytessent = []
    #lt_rssi = []

    while(k <= 2):
        
        print k
        k = k+1
        
        url_list = read_xml(get_xml(theurl), "entityId", "url")
        print len(url_list)
        
        #get_csv(read_data(url_list))
        data_tuple = read_data(url_list)
        
    get_csv(data_tuple)