# Visualization

This is my lab project whch is used to achieve the visualization of The campus wireless access logs.

I am responsible for the data processing.

Now, fighting!

First(The introduction of the file and floders):

	1. "0compus_wireless": The data downloaded from the email.

	2. "1original_data" is the original data in which everyday's log consists of several parts.

	3. "2csv_data_18" is the data in which everyday's log has been processed to a complete file. The data is from 20130307 to 20170414. Each file represents a whole day's data. And each file has 18 columns.

	4. "2csv_data_19": The data from 20171017 to 20171019. Each file represents a whole day's data. And each file has 19 columns.

	5. "json_data": The data doesn't include "count".

	6. "4json_data": The data includes "count".

	7. merge.py: Generate files in folder "csv_data" automatically from files in folder "original_data".

	8. data.py: Generate .json files in folder "json_data" automatically from files in folder "csv_data".

Second(Execution sequence):

	merge.py: Synthesize several .csv to a file.
			  Sorting. This is the most important step. Otherwise, the "data.py" can't success.

	data.py: Generate target .json files.

	Must follow the order above.
