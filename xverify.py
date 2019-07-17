#The following script is used to determine valid or invalid emails after running them through a verification service.
#It uses an original source file containing multiple columns of emails. It detects this file,
#extracting the first column to run through the service. It then detects a returned file with verification information
#on this column, analyzes the output to determine validity, saving out valid emails. Entries with invalid
#emails are included in the second file to input along with the second column of emails and so on and so forth.
#The script integrates the production of the input files, as well as the analysis of the output files for
#a continuous process until all columns are analyzed and the number of valid emails is maximized.
#It then outputs a file with all retrieved valid emails.
#While every email could be uploaded to the verification service, this script enables a convenient way
#to minimize the number of emails passed through the verification service in order to minimize costs to the company.

import sys
import csv
import os

def main():

	good_data=list()
	bad_data=list()
	main_file_found=False
	verified_ids=set()
	provided_ids=set()
	main_provided_dict=dict()

	for file in os.listdir(os.getcwd()):
		if 'csv' not in file:
			continue
		if '2019' not in file:
			main_file=file
			main_file_found=True
			print('Main file used: {}'.format(file))
			break
	if not main_file_found:
		print('Main file not found! ')
		return None

	with open(main_file, encoding='latin', newline='') as main_data_file:
		reader = csv.reader(main_data_file, delimiter=',', quotechar='"')
		for line in reader:
			main_headers=line
			break
		main_data=[line for line in reader]
		main_data_file.close()

	col_found=False
	id_found=False
	email_found=False

	for i in range(len(main_headers)):
		if main_headers[i].lower() in {'score', 'source', 'column', 'colnum', 'col_num'}:
			main_source_i=i
			col_found=True
		if main_headers[i].lower() in {'id', 'edid', 'global_id', 'globalid'}:
			main_id_i=i
			id_found=True
		if main_headers[i].lower() in {'email', 'email_1'}:
			main_e_i=i
			email_found=True

	if not col_found or not id_found or not email_found:
		print('Review header names for column source, id and email! ')
		return None

	print('main source index: {}, main id index: {}, main email index: {}'.format(main_source_i, main_id_i, main_e_i))
	#counts=dict()

	for line in main_data:
		col_source = int(line[main_source_i]) #getting which column it comes from
		#counts[col_source] = counts.get(col_source, 0)+1
		customer_id = line[main_id_i].strip() #getting the id
		sub_source_dict = main_provided_dict.get(col_source, dict()) #getting thedict for the col source otherwise blank dict
		sub_source_dict[customer_id] = line #in this dict, I am making a NEW entry for the customer's id and the email for that column
		main_provided_dict[col_source] = sub_source_dict

	#print(counts)

	cols = sorted([item for item in main_provided_dict])

	first=True

	for col_count in cols:

		count=0
		ver_file_name = main_file.replace('.csv', '_TO_VERIFY') + '_{}.csv'.format(col_count)
		with open(ver_file_name, 'w', encoding='latin', newline='') as sub_xver_file:
			writer = csv.writer(sub_xver_file)
			writer.writerow(main_headers)
			col_dict = main_provided_dict[col_count]
			for _id in col_dict:
				if _id in verified_ids:
					continue
				line = col_dict[_id]
				count+=1
				writer.writerow(line)
			sub_xver_file.close()

		xver_file_found=False
		done=False

		while not xver_file_found:
			for file in os.listdir(os.getcwd()):
				if '2019' in file:
					xver_file=file
					print('Xverify file used: {}'.format(file))
					xver_file_found=True
					break
			if not xver_file_found:
				print('Emails to verify: {}'.format(count))
				choice = input('Input xverify output file {} and enter to continue or w to write current data_ '.format(col_count))
				if choice == 'w':
					done=True
					break

		os.remove(ver_file_name)

		if done:
			break

		with open(xver_file, encoding='latin', newline='') as xver_input_data:
			reader = csv.reader(xver_input_data, delimiter=',', quotechar='"')
			for line in reader:
				xver_headers=line
				break
			xver_data=[line for line in reader]
			xver_input_data.close()
			os.remove(xver_file)

		if first:
			col_found=False
			id_found=False

			for i in range(len(xver_headers)):
				if xver_headers[i].lower() in {'source', 'column', 'colnum', 'col_num', 'score'}:
					source_i=i
					col_found=True
				if xver_headers[i].lower() in {'id', 'edid', 'global_id', 'globalid'}:
					id_i=i
					id_found=True
				if xver_headers[i].lower() == 'email':
					e_i=i
				if xver_headers[i] == 'Status':
					i_1=i
				if xver_headers[i] == 'Catch All Domain':
					i_2=i
			first=False
			if not col_found or not id_found:
				print('Review header names for column source and id!')
				return None

		bad_ids=set()

		for line in xver_data:
			_id = line[id_i].strip()
			if (str(line[i_1].strip().lower()) == 'valid' and str(line[i_2].strip().lower()) == "false"):
				good_data.append(line)
				verified_ids.add(_id)
			else:
				bad_ids.add(_id)
				bad_data.append(line)

	with open(main_file.replace('.csv', '_HYGIENED.csv'), 'w', encoding='latin', newline='') as output_file:   
		output_writer = csv.writer(output_file)
		output_writer.writerow(xver_headers)
		for item in good_data:
			output_writer.writerow(item)
		output_file.close()

	with open(main_file.replace('.csv', '_BAD.csv'), 'w', encoding='latin', newline='') as output_file:   
		output_writer = csv.writer(output_file)
		output_writer.writerow(xver_headers)
		for item in bad_data:
			output_writer.writerow(item)
		output_file.close()


main()


