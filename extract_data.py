import csv
import os

# go through each file, use global customer ID. This becomes the key in the master dictionary.
def main():

	master_dict=dict()
	all_headers=list()
	master_email=dict()
	score_dict_keys={'dealership': 5, 'address_only': 4, 'name_address': 3, 'phone': 2, 'email': 1}
	output_score_keys={5: 'DLR', 4: 'ADD', 3: 'NM_ADD', 2: 'PHN', 1: 'EML'}
	email_score_dict_keys={'dealership': 1, 'address_only': 5, 'name_address': 4, 'phone': 3, 'email': 2}
	output_score_keys_email={1: 'DLR', 5: 'ADD', 4: 'NM_ADD', 3: 'PHN', 2: 'EML'}
	score_dict={}
	email_score_dict={}

	for file in os.listdir(os.getcwd()):
		if 'csv' not in file or 'output' in file.lower():
			continue
		for key in score_dict_keys:
			if key in file.lower():
				score_dict[file]=score_dict_keys[key]
				email_score_dict[file]=email_score_dict_keys[key]

	for item in sorted(score_dict.items(), key = lambda x: x[1]):
		print(item)
	if len(score_dict_keys) != len(score_dict):
		print("** File key mismatch **")
	choice = input('Continue? y/n ')
	if choice == 'n':
		return None

	for file in os.listdir(os.getcwd()):
		dealership=False
		headers_to_add=list()
		source=file
		if 'csv' not in file or 'output' in file.lower():
			continue
		if 'dealership' in file:
			dealership=True
		with open(file, encoding='latin') as datafile:
			reader = csv.reader(datafile, delimiter=',', quotechar='"')
			for line in reader:
				headers = [entry.strip() + "_DEALER" if dealership else entry.strip() for entry in line]
				for header in headers:
					if header not in all_headers:
						headers_to_add.append(header)
				#print(headers_to_add, len(headers_to_add), len(set(headers_to_add)))
				all_headers.extend(headers_to_add)
				break
			for line in reader:
				global_id = line[0].strip()
				temp_dict = {headers[i]:line[i] for i in range(1, len(headers))}
				all_dict = master_dict.get(global_id, dict())
				for header in temp_dict:
					local_list = all_dict.get(header, list())
					val = temp_dict[header].strip()
					if len(val) < 1:
						continue
					if "@" in val:
						if "." in val:
							cust_email_list = master_email.get(global_id, list())
							cust_email_list.append((email_score_dict[source], val))
							master_email[global_id] = cust_email_list
					local_list.append((score_dict[source], val))
					all_dict[header] = local_list
				master_dict[global_id] = all_dict

	dealer_headers=list()
	epek_headers=list()

	for header in all_headers:
		if header.endswith('_DEALER'):
			dealer_headers.append(header)
		else:
			epek_headers.append(header)

	write_headers = epek_headers + dealer_headers
	write_headers_inds_dict = {write_headers[i]:i for i in range(len(write_headers))}

	with open('Merged_Master_Output.csv', 'w', encoding='latin', newline='') as output_file:
		output_writer = csv.writer(output_file, delimiter=',', quotechar='"' )
		output_writer.writerow(["Global_ID", "Address_Source"] + write_headers)
		for global_id in master_dict:
			address_found=False
			retrieved_source='DLR'
			entry = master_dict[global_id] #entry is a dictionary consisting of the header name and a list of tuples - source rank, value
			writedict=dict()
			for header in entry:
				#print(entry[header])
				both = sorted(entry[header])[0]
				#print(both)
				if not address_found:
					if header == 'Address':
						retrieved_source = both[0]
						address_found=True
				#print(retrieved_source)
				writedict[header] = both[1] #REMOVE COMMENT
				#writedict[header] = ";".join([str(both[0]), both[1]]) #THIS IS FOR TESTING, COMMENT OUT!!!!!!!
				#print(both[1])
				#print("\n")
			towrite = ['' for _ in range(len(write_headers))]
			for header in write_headers:
				try:
					towrite[write_headers_inds_dict[header]] = writedict[header]
				except:
					continue

			output_writer.writerow([global_id, output_score_keys[retrieved_source]] + towrite)

		output_file.close()

	no_email=set(["abc", "123", "n","cd", "info", "wng", "email", "none", "na", "no", "dnh", "noemail", "doesnothave",  "declined", "decline", "n/a", "refused", "noname", "nothing"])
	email_sup_set=set()

	with open('Merged_Email_Output.csv', 'w', encoding='latin', newline='') as output_file:
		output_writer = csv.writer(output_file, delimiter=',', quotechar='"')
		output_writer.writerow(['Global_ID', 'Score', 'File_Origin', 'Email'])
		for global_id in master_email:
			count=0
			email_tups = sorted(master_email[global_id])
			for email_tup in email_tups:
				score = email_tup[0]
				email = email_tup[1]
				email = email.lower()
				if email in email_sup_set:
					continue
				email_sup_set.add(email)
				email_parts = email.split('@')
				name = email_parts[0]
				domain = email_parts[1]
				if name in no_email or domain[:domain.rfind(".")] in no_email:
					continue
				count+=1
				output_writer.writerow([global_id, str(count), output_score_keys_email[score], email])
		output_file.close()


main()
				


