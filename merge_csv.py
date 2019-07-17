#The following is a simple script to combine data files that I frequently use. It removes duplicate entries by
#creating a tuple for each entry consisting of a customizable subset of columns, adding this to a set and skipping
#any entries whose key is already in the set. This is a technique I developed for removing duplicates and currently
#implement in many of my scripts. It enables the removal of duplicates in a fraction of the time Excel requires.
#This technique also lends itself to added specificity in removing duplicates, such as sorting or columns by which
#to prioritize entries. In more involved applications, I use dictionaries with a key value and a list of entries,
#which I can later sort in order to extract the desired entry.


import csv
import os
import re


def main():

	raw_list=list()
	for file in os.listdir(os.getcwd()):
		file_key = file.lower()
		if 'csv' not in file_key or 'raw' not in file_key:
			continue
		raw_list.append(file)

	edid_sup_set=set()
	headers_set=set()
	data_master=list()
	dupe_count=0

	if len(raw_list) < 2:
		print("There must be at least two files and 'RAW' must be in their name_")
		return None
	for raw_file in raw_list:
		with open(raw_file, encoding='latin', newline='') as read_file:
			raw_reader = csv.reader(read_file, delimiter=',', quotechar='"')
			for line in raw_reader:
				headers=line
				write_headers=headers
				headers_set.add(tuple(headers))
				break
			read_file.close()

	if len(headers_set) != 1:
		print('headers mismatch, cannot combine files_')
		for headers_list in headers_set:
			print(', '.join(headers_list))
		return None

	print('...')

	for raw_file in raw_list:
		with open(raw_file, encoding='latin', newline='') as read_file:
			raw_reader = csv.reader(read_file, delimiter=',', quotechar='"')
			for line in raw_reader:
				break
			for line in raw_reader:
				data_master.append(line)
			read_file.close()

	file_base = raw_list[0]
	file_base = re.sub(r'_\d{4,}.+', '', file_base)
	output_name = file_base + '_Combined_RAW.csv'
	with open(output_name, 'w', encoding='latin', newline='') as output_file:
		output_writer = csv.writer(output_file, delimiter=',', quotechar='"')
		output_writer.writerow(write_headers)
		for line in data_master:
			edid = line[0]
			if edid in edid_sup_set:
				dupe_count+=1
				continue
			edid_sup_set.add(edid)
			output_writer.writerow(line)
			
		output_file.close()
	print('{} duplicates skipped out of {} total records with {} output records_'.format(dupe_count, len(data_master), len(edid_sup_set)))

main()



