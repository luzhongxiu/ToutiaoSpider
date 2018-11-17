import requests
from hashlib import md5
from urllib.parse import urlencode
import json
from multiprocessing.pool import Pool
def get_page(offset):
	params={
	'offset': offset,
	'format': 'json',
	'keyword': '桂纶镁',
	'autoload': 'true',
	'count': '20',
	'cur_tab': '1',
	'from': 'search_tab'
	}
	base_url = 'http://www.toutiao.com/search_content/?'
	url= base_url + urlencode(params)
	try:
		resp = requests.get(url)
		if resp.status_code == 200:
			return resp.json()
	except Exception as e:
		return None
def get_images(json):
	if json.get('data'):
		data = json.get('data')
		for item in data:
			if item.get('cell_type') is not None:
				continue
			title = item.get('title'),
			images = item.get('image_list')
			for image in images:
				yield{
					'image':'https:'+image.get('url'),
					'title':title
				}
def save_image(item):
	image_path = 'img'+os.path.sep+item.get('title')
	if not os.path.exists(image_path):
		os.makedirs(image_path)
	try:
		resp = requests.get(item.get('image'))
		if resp.status_code == 200:
			file_path = img_path + os.path.sep +'{file_name}.{file.suffix}'.format(file_name=md5(resp.content).hexdigest(),file_suffix='jpg')
			if not os.path.exists(file_path):
				with open(file_path,'wb') as f:
					f.write(resp.content)
				print('Downloaded image path is %s' %file_path)
	except requests.ConnectionError:
		print("failed")
def main(offset):
	json=get_page(offset)
	for item in get_images(json):
		print(item)
		save_image(item)
if __name__ == '__main__':
	pool = Pool()
	groups =([x*20 for x in range(0,7)])
	pool.map(main,groups)
	pool.close()
	pool.join()
