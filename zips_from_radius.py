import sqlite3
import sys
import os

		
conn = sqlite3.connect("zip_distances.sqlite")

cur = conn.cursor()


while True :

	try :

		check = dict()

		_input = input('Enter zip followed by a space and the desired radius _ ').strip()

		try :

			lst = _input.split(" ")

		except :

			continue

		zip_ = lst[0].strip()
		miles = int(lst[1].strip()) 

		save_zip = zip_

		radius = 5

		w_zip = "'" + zip_ + "'"


		cur.execute("select * from " + w_zip) 

	except :

		continue

		
	return_lst = list()
	return_lst.append(save_zip)

	for line in cur :
		if line[1] <= miles :
			#return_lst.append(unicodedata.normalize('NFKD', line[0]).encode('ascii','ignore'))
			return_lst.append(line[0])
			

	print("\n")

	print(','.join(return_lst))

	print("\n")

sys.exit()


