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
	
Realtime:

	realtime_id_v1.py: to get the realtime data according to "id" from the path "https://192.168.16.203/webacs/api/v1/data/ClientDetails/", then the data will be written into the .csv.

	realtime_id_v2.py: to get the realtime data according to "id" from the path "https://192.168.16.203/webacs/api/v2/data/ClientDetails/", then the data will be written into the .csv.

	realtime_id_v2_db.py: to get the realtime data according to "id" from the path "https://192.168.16.203/webacs/api/v2/data/ClientDetails/", then the data will be saved into the MySQL.


	realtime_sort_filter.py: to get the data after filtered by 'ASSOCIATED' and sorted by '+associationTime'. 100 pieces/every time.

	realtime_id.py: to get the data according to the id so we can get all data for one day.

	realtime_to_json.py: csv to json.

	5csv_realtime: to save the real-time data by .csv.

	5json_realtime: to save the real-time data by .json.
