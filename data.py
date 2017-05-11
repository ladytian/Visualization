#Import
import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import seaborn as sns
sns.set_style('whitegrid')

test_df = pd.read_csv(r"D:\workspace\Visualization\Teachers_roaming_day_0307_0414\20170406.csv")
#print test_df.head(10)
#test_df.info()
#print test_df.describe()

test_df = test_df.drop(['Client Username','Client IP Address','Device Name','SSID','Profile','Mobility Status','AP IP Address','Client Type'], axis=1)
#test_df.info()
#test_df['AP Name'] = test_df['AP Name'].fillna('outdoor')
test_df = test_df.dropna(axis=0, how="any")

test_df['building'] = test_df['AP Name'].str.split('-')
test_df['floor'] = test_df['AP Name'].str.split('-')
test_df['building'] = test_df['building'].str[0]
test_df['floor'] = test_df['floor'].str[1]
test_df = test_df.drop(['AP Name'], axis=1)

association_time = test_df['Association Time']
test_df.drop(['Association Time'], axis=1, inplace=True)
test_df.insert(0, 'association_time', association_time)

test_df['association_time'] = pd.to_datetime(test_df['association_time'])
#.astype(str)

test_df.rename(columns={'association_time':'associationTime','Client MAC Address':'clientMacAdd','Vendor':'vendor','floor':'room','VLAN ID':'vlanID','Protocol':'protocol','Session Duration':'sessionDuration','Avg. Session Throughput (Kbps)':'avgThroughput','Bytes Sent':'byteSent','Bytes Received':'byteReceived'}, inplace=True)
#print test_df.head(10)

#print test_df.head(15)
#test_df.info()
#df = test_df[0:5]
#print df
#test_df.to_csv("test1.csv")

json = test_df.to_json(r"D:\workspace\Visualization\complete\test1.json", orient="records")