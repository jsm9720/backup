# 만든이 : 정성모
# 입력 : raw193.csv
# 출력 : Original data, Relative_data
# block_bio_queue, block_getrq, nvme_sq를 상대시간으로 변경

import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras import models, layers, utils

def main():
	data = pd.read_csv("/home/mo/Project/BIO/raw_cassandra/raw193.csv")
	data = data.copy()
	data.pop('Size of IO')
	data.pop('streamid')

#	data.to_csv("Original_data.csv", mode='w',index=False)
	
	# Convert absolute time to relative time
	data['block_rq_complete']= data['block_rq_complete'] - data['nvme_sq']
	data['nvme_sq']= data['nvme_sq'] - data['block_getrq']
	data['block_getrq']= data['block_getrq'] - data['block_bio_queue']
	bio_queue_preprocessing(data)

#	data.to_csv("Relative_data.csv", mode='w')

# bio_queue의 해당 row의 값은 해당 row값에서 첫번째 row 값에서 뺀 값, 첫번째 row 값은 0
def bio_queue_preprocessing(x):

	data = np.array(x['block_bio_queue'])
	temp = np.zeros(len(data))
	for i in range(len(data)):
		temp[i] = data[i] - data[0]
	temp[0] = 0.
	x['block_bio_queue'] = temp

	return x

main()
