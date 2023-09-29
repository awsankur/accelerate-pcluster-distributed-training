import glob
import os
import pandas as pd

data_path = '/home/ubuntu/amgen/sample-amgen-data'

files = glob.glob(data_path+"/*")

num_files = len(files)

file_index_map_df = pd.DataFrame(columns = ['file_num','num_sequences','start_line_num','end_line_num'])
start_line_num = 0
for i in range(num_files):
	print(i)
	file_name = files[i]
	df = pd.read_parquet(file_name, engine='pyarrow')

	file_index_map_df.loc[i-1,'file_num'] = i
	file_index_map_df.loc[i-1,'num_sequences'] = df.shape[0]
	file_index_map_df.loc[i-1,'start_line_num'] = start_line_num
	end_line_num = start_line_num + df.shape[0] - 1
	file_index_map_df.loc[i-1,'end_line_num'] = end_line_num
	start_line_num = start_line_num + df.shape[0]

file_index_map_df.to_csv('./file_index_map_df.csv',index=False)

