import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import os

path = "D:\workspace\Visualization\original_data\wireless_session_20171019_000046_189.csv"

file_list = []

for root, dirs, files in os.walk(path):
	for filename in files:
		file_list.append(filename)
print len(file_list), file_list

d1 = pd.read_csv(path + "\\" + file_list[0], skiprows=7)

for filename in files[1: ]:
	d2 = pd.read_csv(path + "\\" + filename, skiprows=7)
	d = pd.concat([d1,d2], ignore_index=True)
	d1 = d
	print 1
#print d.info()
d = d.sort(columns='Client MAC Address', ascending=True)
d.to_csv(r"D:\workspace\Visualization\csv_data\20171019.csv", index=False)