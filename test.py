import requests
import pandas as pd
import random
import json
import time
from datetime import datetime
from bs4 import BeautifulSoup

def format_json(js_code):
	block = js_code.replace('\n', '')
	#find the first { and replace by *, assign its index to i1
	i1 = block.find('{')
	block =  block.replace('{', '*', 1)
	i2 = block.find('{')
	block = block[i2:]
	return block


def get_info(lurl):
	ca = []
	dt = []
	uc = []
	gc = []
	result = pd.DataFrame([])
	for url in lurl:
		r = requests.get(url)
		dom = r.content.decode('utf-8')
		soup = BeautifulSoup(dom, 'html.parser')
		#format the string
		block = soup.find_all('script')[-1]
		block = block.decode_contents()
		block = format_json(block)
		block = block.split('},')
		temp0 = json.loads(block[0] + '}}')
		temp1 = json.loads(block[2] +'}')
		ca.append(temp0['created_at'])
		dt.append(temp0['disp_title'])
		uc.append(temp1['user_clicks'])
		gc.append(temp1['global_clicks'])
		#jiggle
		a = random.uniform(0,0.5)
		time.sleep(a)
	dt = [x.replace('"', '') for x in dt]
	result['bitly'] = [x[:-1].replace('.', '[.]') for x in lurl]
	result['disp_title'] = [x.replace('http', 'hxxp') for x in dt]
	result['create_at'] = [datetime.utcfromtimestamp(int(x)).\
	strftime('%Y-%m-%d %H:%M:%S') for x in ca]
	result['user_clicks'] = uc
	result['global_clicks'] = gc
	return result


if __name__ == '__main__':
	#option1: pass in a list
	lurl = ['https://bitly.com/1ckcXew+', \
	'https://bit.ly/1bdCiX8+', 'https://bit.ly/1GygJ1Y+']
	#option2: pass in a csv file
	#cleaning included
	# df = pd.read_csv('bitlyurl.csv')
	# data = df.copy()
	# data.index = data.index + 1
	# data.loc[0] = dadta.columns[0]
	# data = data.sort_columns[0]
	# data = data.sort_index()
	# data.columns = ['bitlyurl']
	#lurl = [x + '+' for x in data['bitlyurl']]
	#lurl is a list of url
	result = get_info(lurl)
	result.to_csv('result.csv',index = False)