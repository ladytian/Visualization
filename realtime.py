#coding:utf-8
import urllib2
import base64
import ssl
from xml.etree import ElementTree as ET
import pandas as pd
from datetime import datetime
import time
import random
import argparse
import traceback
import MySQLdb

#to get the XML files when given a url and return the string of the files content.
def get_xml(url):

    req=urllib2.Request(url)

    username = 'prog'
    password = 'Jsj60216926'
    base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
    authheader =  "Basic %s" % base64string
    req.add_header("Authorization", authheader)
    context = ssl._create_unverified_context()

    try:
        handle = urllib2.urlopen(req, context=context, timeout=60)
        thepage = handle.read() 
        return thepage
    except:
        with open('debug.txt','a+') as errorInfo:
            traceback.print_exc(file=errorInfo)
        print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return "error"

# to get a specific property content in a XML file when given the text，label path and attribute name and return a list.
def read_xml(text, tag, attribute):
    
    lt_1 = []
    root = ET.fromstring(text)
    
    for item in root.findall(tag):
        lt_1.append(item.get(attribute))

    return lt_1

# to get the count's value
def get_count(text):
    root = ET.fromstring(text)
    c = int(root.get('count'))
    return c

# to parse the file when given a list of urls to get the desired data field and return a tuple of several lists.
def read_data(lt):
    
    dirs = 'entity/clientDetailsDTO/'
    fields = ['macAddress', 'associationTime', 'updateTime', 'apName', 'status']
   
    for j in range(len(lt)): 
        try:
            page = get_xml(lt[j])
            if page == "error":
                continue

            root = ET.fromstring(page)

            for i in range(len(fields)):
                for item in root.findall(dirs + fields[i]):
                    if i == 0:
                        lt_clientmac.append(item.text)
                    elif i == 1:
                        lt_assotime.append(item.text)
                    elif i == 2:
                        lt_updatetime.append(item.text)
                    elif i == 3:
                        lt_apname.append(item.text)
                    elif i == 4:
                        lt_status.append(item.text)

            if not(len(lt_clientmac) == len(lt_assotime) == len(lt_updatetime) == len(lt_apname) == len(lt_status)):
                m = min(len(lt_clientmac), len(lt_assotime), len(lt_updatetime), len(lt_apname), len(lt_status))

                while(len(lt_clientmac) > m):
                    lt_clientmac.pop()
                while(len(lt_assotime) > m):
                    lt_assotime.pop()
                while(len(lt_updatetime) > m):
                    lt_updatetime.pop()
                while(len(lt_apname) > m):
                    lt_apname.pop()
                while(len(lt_status) > m):
                    lt_status.pop()
            #raise Exception("Test error!", j)
            
        except Exception:
            with open('debug.txt','a+') as errorInfo:
                traceback.print_exc(file=errorInfo)
            print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print "Warning: Read false! An error occurred in the url " + lt[j]

    last_id = read_xml(page, 'entity/clientDetailsDTO', 'id')[0]

    return [lt_clientmac, lt_assotime, lt_updatetime, lt_apname, lt_status], last_id

# to store the data in the CSV file according to the field given the tuple of data lists.
def get_csv(lt):

    if len(lt[0]) == len(lt[1]) == len(lt[2]) == len(lt[3]) == len(lt[4]):
        
        df = pd.DataFrame({'clientMacAdd':lt[0], 'associationTime':lt[1], 'updateTime':lt[2], 'AP_Name':lt[3], 'status':lt[4]}) # for v2
        
        df.to_csv(r"./csv_realtime" + "/" + str(datetime.now().strftime('%Y%m%d%H%M%S')) + ".csv",index=False,sep=',', mode='w')

    else:
        print "Warning: Lists have different length!"
    
def db_create(table_name):
    #to open the connection
    db = MySQLdb.connect(host='59.67.152.230', user='root', passwd='zh911zh911_+!', db='wifi', port=3306)

    # to get the cursor with the method cursor()
    cursor = db.cursor()

    # to set up a table
    sql = "CREATE TABLE IF NOT EXISTS wifi_%s" % table_name + "( \
    id int not null auto_increment primary key, \
    clientMacAdd CHAR(25) NOT NULL, \
    associationTime CHAR(20), \
    updateTime CHAR(20), \
    AP_Name CHAR(70), \
    status CHAR(25) \
    )"

    try:
        cursor.execute(sql)
        db.commit()
    except:
        # rollback in case there is any error
        db.rollback()

    # to close the cursor and connection
    cursor.close()
    db.close()

# store into mysql
def db_insert(lt, table_name):

    #to open the connection
    db = MySQLdb.connect(host='59.67.152.230', user='root', passwd='zh911zh911_+!', db='wifi', port=3306)

    # to get the cursor with the method cursor()
    cursor = db.cursor()

    for i in range(len(lt[0])):

        sql = """INSERT IGNORE INTO wifi_%s""" % table_name + """(clientMacAdd, associationTime, updateTime, AP_Name, status)VALUES ('%s', '%s', '%s', '%s', '%s')""" % (lt[0][i], lt[1][i], lt[2][i], lt[3][i], lt[4][i])

        try:
            cursor.execute(sql)
            #cursor.execute(sql2)
            if i % 10 == 0:
                db.commit()
        except:
            # rollback in case there is any error
            db.rollback()

    db.commit()

    # to close the cursor
    cursor.close()
    db.close()

def main():
    
    try:
        n_k = 0 if args.n_k == None else args.n_k

        theurl = 'https://192.168.16.203/webacs/api/v2/data/ClientDetails/'

        table_name2 = ""
        k = 0

        while(True): 

            print "k=%d" % k
            print datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            s = 0
            p = get_xml(theurl)

            if p == "error":
                continue

            count = get_count(p)
            print count, s

            data_list = []
            read_last_id = ""
            param = '?id=gt(0)'
            
            global lt_clientmac
            lt_clientmac = []
            global lt_assotime
            lt_assotime = []
            global lt_updatetime
            lt_updatetime = []
            global lt_apname
            lt_apname = []
            global lt_status
            lt_status = []

            while(s < count):
                
                p = get_xml(theurl + param)

                if p == "error":
                    continue

                url_list = read_xml(p, "entityId", "url")
                count = get_count(p)
                s = s + len(url_list)
                print count, s
                # len(url_list) = 100
                
                data_list, read_last_id = read_data(url_list)

                param = '?id=gt(' + read_last_id + ')' 
                table_name1 = datetime.now().strftime('%Y%m%d')
                
                if not(table_name1 == table_name2):
                    db_create(table_name1)
                    db_insert(data_list, table_name1)
                    table_name2 = table_name1
                else:
                    db_insert(data_list, table_name1)

                time.sleep(random.randint(10, 20))

                lt_clientmac = []
                lt_assotime = []
                lt_updatetime = []
                lt_apname = []
                lt_status = []
                                       
            k = k+1
            if k == n_k:
                break
            if k % 2 == 0:
                time.sleep(random.randint(300, 500))
            else:
                time.sleep(random.randint(60, 180))

    except Exception:
        with open('debug.txt','a+') as errorInfo:
            traceback.print_exc(file=errorInfo)
        print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print "Warning: An error occurred in the k=" + str(k)
    else:
        print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print "Congratulations! Success!"

if __name__ == '__main__':
    
    global args
    lt_clientmac = []
    lt_assotime = []
    lt_updatetime = []
    lt_apname = []
    lt_status = []
    
    argsparser =  argparse.ArgumentParser()
    argsparser.add_argument("-n_k",type=int,default=0)
    args = argsparser.parse_args()

    main()
