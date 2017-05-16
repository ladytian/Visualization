# Visualization

This is my lab project whch is used to achieve the visualization of The campus wireless access logs.

I am responsible for the data processing.

Now, fighting!

First:

	1.The folder "data" is the original data in which everyday's log consists of several parts.

	2.The folder "Teachers_roaming_day_0307_0414" is the data in which everyday's log has been processed to a complete file.

	3.The folder "complete data" is the data which I can pass to Yiyi Chang.

	4.merge.py: Generate files in folder "Teachers_roaming_day_0307_0414" automatically.

Second(Execution sequence):

	selection 1:

	merge.py: Synthesize several .csv to a file.
		  Sorting. This is the most important step. Otherwise, the "data.py" can't success.

	data.py: Generate target file.


	selection 2:

	merge.py: Synthesize several .csv to a file.
		  Sorting. This is the most important step.
			  
	data1.py: Drop redundant columns and rename.
		  Convert "sessionDuration" in "a.csv" to seconds.
		  Deal with the values containing ",".
		  Generate intermediate file "data1.csv" for later use.

	data2.py: Drop null value(mainly for "AP Name")
		  Generate "building" and "room"
		  Generate intermediate file "data2.csv" for later use.

	data3.py: Calculation "breakingTime" using "data2.csv".
		  Set the column order as ['clientMacAdd','associationTime','sessionDuration','breakingTime','building','room','avgThroughput','byteSent','byteReceived','RSSI','vendor','vlanID','protocol']
			 
	data4.py: Adjustment format and generate target file.

	Must follow the order above.
