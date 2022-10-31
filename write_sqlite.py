import sqlite3
import os, sys
import numpy
from pathlib import Path
from tqdm import tqdm
from PIL import Image


# read single label file to get label info
def read_label(label_path):
	with open (label_path, 'r') as f:
		labeldata = f.read()
	return labeldata

# read dataset to and its compare label
def find_dataset_path(dataset_path):
	datalist = []
	for imagename in os.listdir(dataset_path):
		if imagename.endswith(('jpg', 'jpeg', 'bmp', 'png', 'tif')):
			labelname = imagename.replace(os.path.splitext(imagename)[1], '.label')
			datalist.append([imagename ,labelname])
	return datalist

def img_to_bytes(img_path):
	if img_path.endswith(('bmp', 'png', 'tif')):
		new_img_path = img_path.replace(os.path.splitext(img_path)[1], '.jpg')
		im = Image.open(img_path)
		im.save(new_img_path)
		with open(new_img_path, 'rb') as f:
			img_bytes = f.read()
		os.remove(new_img_path)
	else:
		with open(img_path, 'rb') as f:
			img_bytes = f.read()
	return img_bytes

class SQLiteWriter(object):
	def __init__(self, db_path):
		self.conn = sqlite3.connect(db_path)
		self.cursor = self.conn.cursor()

	def execute(self, sql, value=None):
		if value:
			self.cursor.execute(sql,value)
		else:
			self.cursor.execute(sql)

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.cursor.close()
		self.conn.commit()
		self.conn.close()

if __name__ == '__main__':
	dataset_dir = Path('datasets/DLOCR/')
	save_db_dir = dataset_dir / 'sqlite'
	save_db_path = str(save_db_dir / 'DLOCR.db')
	
	if (os.path.exists(save_db_path)): os.remove(save_db_path)

	datalist = find_dataset_path(dataset_dir)

	with SQLiteWriter(save_db_path) as db_writer:
		table_name = 'DLOCR'
		create_table_sql = f'create table {table_name} (img_name TEXT, img_data BLOB, label_data TEXT)'
		db_writer.execute(create_table_sql)
		insert_sql = f'insert into {table_name} (img_name, img_data, label_data) values(?, ?, ?)'

		for data_info in tqdm(datalist):
			img_path, label = data_info[0], data_info[1] 

			img_full_path = str(dataset_dir / img_path)
			img_data = img_to_bytes(img_full_path)

			label_full_path = str(dataset_dir / label)
			label_data = read_label(label_full_path)

			db_writer.execute(insert_sql, (os.path.splitext(img_path)[0], img_data, label_data))
