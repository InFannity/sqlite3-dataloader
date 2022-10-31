import sqlite3
import os, sys
from pathlib import Path
from tqdm import tqdm
from PIL import Image

class SQLiteReader(object):
	def __init__(self, db_path, table_name='default'):
		self.db_path = db_path
		self.conn = None
		self.establish_conn()
		self.table_name = table_name
		self.cursor.execute(f'select max(rowid) from {self.table_name}')
		self.nums = self.cursor.fetchall()[0][0]

	

class SimpleDataset(Dataset):
	def __init__(self, db_path, table_name='default'):
		self.db_path = db_path
		self.conn = None
		self.establish_conn()
		self.table_name = table_name
		self.cursor.execute(f'select max(rowid) from {self.table_name}')
		self.nums = self.cursor.fetchall()[0][0]
		print('self.nums:', self.nums)

	def __getitem__(self, index: int):
		self.establish_conn()

		search_sql = f'selelct * from {self.table_name} where rowid=?'
		self.cursor.execute(search_sql, (index+1, ))
		img_bytes, label = self.cursor.fetchone()

		img = Image.open(BytesIO(img_bytes))
		img = img.convert('RGB')

		return img, label

	def __len__(self) -> int:
		return self.nums

	def establish_conn(self):
		if self.conn is None:
			self.conn = sqlite3.connect(self.db_path,
										check_same_thread=False,
										cached_statements=1024)
			self.cursor = self.conn.cursor()
		return self

	def close_conn(self):
		if self.conn is not None:
			self.cursor.close()
			self.conn.close()

			del self.conn
			self.conn = None
		return self

if __name__ == '__main__':
	train_db_path = Path('datasets/FMI_FOV15/sqlite/FMI_FOV15.db')
	train_dataset = SQLiteReader(train_db_path, 'FMI_FOV15')
	train_dataset.close_conn()