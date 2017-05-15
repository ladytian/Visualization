import pandas as pd
from pandas import Series,DataFrame
from pandas.tseries.offsets import *
import numpy as np
import string


test_df = pd.read_csv(r"D:\workspace\Visualization\complete data\ing\out1.csv", error_bad_lines=False)
#print test_df.head()
#test_df.info()
#print test_df.describe()

test_df = test_df.drop(['Unnamed: 0'], axis=1)
test_df = test_df.dropna(axis=0, how="any")
#test_df['AP Name'] = test_df['AP Name'].fillna('outdoor')

test_df['building'] = test_df['AP_Name'].str.split('-')
test_df['room'] = test_df['AP_Name'].str.split('-')
test_df['building'] = test_df['building'].str[0]
test_df['room'] = test_df['room'].str[1]
test_df = test_df.drop(['AP_Name'], axis=1)

#association_time = test_df['Association Time']
#test_df.drop(['Association Time'], axis=1, inplace=True)
#test_df.insert(0, 'association_time', association_time)
#test_df['Association Time'] = pd.to_datetime((test_df['Association Time']))

#test_df.rename(columns={'association_time':'associationTime','Client MAC Address':'clientMacAdd','floor':'room','VLAN ID':'vlanID','Protocol':'protocol','Session Duration':'sessionDuration','Avg. Session Throughput (Kbps)':'avgThroughput','Bytes Sent':'byteSent','Bytes Received':'byteReceived'}, inplace=True)


#print test_df.head(10)
#print test_df.index()
#test_df.info()
test_df.to_csv("out2.csv", index=False)

#json = test_df.to_json(r"D:\workspace\Visualization\complete data\test1.json", orient="records")