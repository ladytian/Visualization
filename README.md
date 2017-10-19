# Visualization

This is my lab project whch is used to achieve the visualization of The campus wireless access logs.

I am responsible for the data processing.

Now, fighting!

First:

	1.The folder "original_data" is the original data in which everyday's log consists of several parts.

	2.The folder "csv_data" is the data in which everyday's log has been processed to a complete file.

	3.The folder "json_data" is the data which I can pass to Yiyi Chang.

	4.merge.py: Generate files in folder "csv_data" automatically from files in folder "original_data".

	5.data.py: Generate .json files in folder "json_data" automatically from files in folder "csv_data".

Second(Execution sequence):

	merge.py: Synthesize several .csv to a file.
			  Sorting. This is the most important step. Otherwise, the "data.py" can't success.

	data.py: Generate target .json files.

	Must follow the order above.
