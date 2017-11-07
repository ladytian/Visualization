#coding:utf-8
import urllib2
import base64
import ssl
from xml.etree import ElementTree as ET
import pandas as pd

    
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

def read_xml(text, tag, attribute):
    
    lt_1 = []
    root = ET.fromstring(text)  # read the xml file
    #print root.tag, "---", root.attrib
    
    for entityId in root.findall(tag):
        lt_1.append(entityId.get(attribute))
    #print len(lt_1)
    
    return lt_1

def read_data(lt):
    
    lt_clientmac = []
    lt_assotime = []
    lt_apname = []
    lt_throughput = []
    lt_bytesreveived = []
    lt_bytessent = []
    lt_rssi = []
   
    for j in range(0,2):
    #for j in range(len(lt)):
        
        page = get_xml(lt[j])
        #print thepage
        print j, lt[j]

        root = ET.fromstring(page)
        #print j, root.tag, root.text

        dirs = 'entity/clientDetailsDTO/'
        fields = ['macAddress', 'associationTime', 'apName', 'throughput', 'rssi']

        for i in range(len(fields)):
            for item in root.findall(dirs + fields[i]):
                if item.text is '':
                    item.text = 0

                if i == 0:
                    lt_clientmac.append(item.text)
                elif i == 1:
                    lt_assotime.append(item.text)
                elif i == 2:
                    lt_apname.append(item.text)
                elif i == 3:
                    lt_throughput.append(item.text)
                elif i == 4:
                    lt_rssi.append(item.text)
                    
    print [lt_clientmac, lt_assotime, lt_apname, lt_throughput, lt_rssi]
    return [lt_clientmac, lt_assotime, lt_apname, lt_throughput, lt_rssi]
    

def get_csv(lt):
    
    if len(lt[0]) == len(lt[1]) == len(lt[2]) == len(lt[3]) == len(lt[4]):
        
        df = pd.DataFrame({'clientMacAdd':lt[0], 'associationTime':lt[1], 'AP_Name':lt[2], 'throughput':lt[3], 'rssi':lt[4]})

        df.to_csv(r".\test" + "\\" + str(k) + "test.csv",index=False,sep=',')
        
        #print df.head(5)
    
    else:
        print "Read false!"
    
    #return df
        
if __name__ == '__main__':
    
    #theurl = "https://192.168.16.203/webacs/api/v2/data/Clients/"
    theurl = 'https://192.168.16.203/webacs/api/v1/data/ClientDetails?.sort=-associationTime&status="ASSOCIATED"'
    
    #print get_xml(theurl)
    #read_data(url_list)    
    #get_csv(read_data(url_list))
    
    k = 0

    while(k <= 999):
        
        print k
        k = k+1
        
        url_list = read_xml(get_xml(theurl), "entityId", "url")
        print len(url_list)
        
        get_csv(read_data(url_list))
