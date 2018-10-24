import os
import csv
import sys

print("\nProcessing data... \n")

cur_dir = os.getcwd()
file_lst_ = os.listdir(cur_dir)

file_lst = list()

for name in file_lst_ :
	if "vlookup" not in name and "Store" not in name :
		file_lst.append(name)


first = [item for item in csv.reader(open(file_lst[0], 'rU'))]
second = [item for item in csv.reader(open(file_lst[1], 'rU'))]


first_dic = dict()

second_dic = dict()

count = 0

for header in first[0]:
	first_dic[count] = header
	count += 1
	
count = 0

for header in second[0]:
	second_dic[count] = header
	count += 1
	
print("\nFile_1 - " + file_lst[0] + " :\n")
for header in first_dic :
	print(str(header) + ". " + first_dic[header])
	
print("\nFile_2 - " + file_lst[1] + " :\n")
	
for header in second_dic :
	print(str(header) + ". " + second_dic[header])
	
while True :
	choice = input("\nEnter principal file - 1 or 2_ ")
	try :
		if choice == "1" :
			principal = first
			principal_name = file_lst[0].replace(".csv", "_VLOOKUP.csv")
			secondary = second
		else :
			principal = second 
			principal_name = file_lst[1].replace(".csv", "_VLOOKUP.csv")
			secondary = first
		break
	except :
		continue
		
print("\nPrincipal chosen: " + str(choice) + "\n")


choices = input("Choose origin column(s) by number separated by commas_ ")

choices = choices.replace(" ","").split(",")

origins = [int(choice) for choice in choices]
	
choices = input("Choose compare column(s) by number separated by commas_ ")

choices = choices.replace(" ","").split(",")

compares = [int(choice) for choice in choices]

choices = input("Choose column(s) to append from secondary file_ ")

choices = choices.replace(" ","").split(",")

returns = [int(choice) for choice in choices]

add_headers = list()

for i in returns :
	add_headers.append("VL_" + secondary[0][i])

add_headers = "," + ",".join(add_headers)


#output_ = raw_input("Enter output filename w/o csv_ ")

#output_ = output_.replace(" ","_")

#output_ = output_ + "_VLOOKUP.csv"

all_match_name = principal_name.replace("VLOOKUP", "VLOOKUP_MATCHES_ONLY")

output = open(principal_name, "w")

all_matches = open(all_match_name, "w")

output.write(",".join(principal[0]) + add_headers + "\n")

all_matches.write(",".join(principal[0]) + add_headers + "\n")



princ_dic = dict()

default = ["#N/A" for idx in range(len(returns))]

for entry in secondary[1:] : 

	key = list()
	for i in compares :
		key.append(entry[i].strip().lower())
	key = tuple(key)
	second_dic[key] = entry 
	
for entry in principal[1:] :

	key = list()
	for i in origins :
		key.append(entry[i].strip().lower())
	key = tuple(key)
	try :
		get = second_dic[key]
		to_write = [get[i] for i in returns]
		all_matches.write(",".join(entry) + "," + ",".join(to_write) + "\n")
	except :
		to_write = default  
	output.write(",".join(entry) + "," + ",".join(to_write) + "\n")
	
print("\nVlookup complete.\n")
	
	 































