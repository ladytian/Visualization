import numpy as np
import pandas as pd
import os
'''
print os.listdir("D:\workspace\Visualization\data\wireless_session_20170414_000112_964.csv")
'''
files = ['wireless_session_20170414_000120_926.csv', 'wireless_session_20170414_000128_274.csv', 'wireless_session_20170414_000134_801.csv', 'wireless_session_20170414_000141_530.csv', 'wireless_session_20170414_000148_362.csv', 'wireless_session_20170414_000155_469.csv', 'wireless_session_20170414_000203_044.csv', 'wireless_session_20170414_000208_318.csv']
path = "D:\workspace\Visualization\data\wireless_session_20170414_000112_964.csv"
d1 = pd.read_csv(path + "\\" + "wireless_session_20170414_000112_964.csv", skiprows=7)

for filename in files:
	d2 = pd.read_csv(path + "\\" + filename, skiprows=7)
	d = pd.concat([d1,d2], ignore_index=True)
	d1 = d
	#print 1
#print d.info()
d = d.sort(columns='Client MAC Address', ascending=True)
d.to_csv(r"D:\workspace\Visualization\Teachers_roaming\20170414.csv", index=False)
