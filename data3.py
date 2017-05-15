import pandas as pd
from pandas import Series, DataFrame
from pandas.tseries.offsets import *
import numpy as np
import string

test_df2 = pd.read_csv(r"D:\workspace\Visualization\complete data\ing\out2.csv", error_bad_lines=False)


test_df2['associationTime'] = pd.to_datetime(test_df2["associationTime"])
test_df2['breakingTime'] = test_df2['associationTime']
#test_df2['breakingTime'] = pd.to_datetime(test_df2["breakingTime"])
sd = 0
for i in range(len(test_df2.index)):
	sd = int(test_df2['sessionDuration'].ix[i])
	test_df2['breakingTime'].ix[i] = test_df2['breakingTime'].ix[i] + DateOffset(seconds=sd)

columns = ['clientMacAdd','associationTime','sessionDuration','breakingTime','building','room','avgThroughput','byteSent','byteReceived','RSSI','vlanID','protocol']

test_df2.to_csv("D:\workspace\Visualization\complete data\out3.csv",index=False,columns=columns)

#print test_df2.head(10)
#test_df2.info()