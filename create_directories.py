import os 

base_directory = os.getcwd()

def folder_make (dealer) :


	client = dealer.strip().replace(" ", "_")
				
	file_path = os.getcwd()

	#directory = os.path.dirname(file_path) + "/" + client 

	directory = file_path + "/" + client 


	os.mkdir(directory) 
	#os.chdir(directory)


	labels = ["A", "B", "C", "D", "E"]

	label_dict = {"A" : "F", "B" : "G", "C" : "H", "D" : "I", "E" : "J"}



	lst = ["CR", "DS", "DE", "MC"]


	for item in lst :

		os.mkdir(directory + "/" + client + "_" + item) 
	
	
	now = directory + "/" + client + "_DE"

	os.chdir(now)


	for label in labels :

	
		os.mkdir(client + label)
	
	
	
	now = directory + "/" + client + "_CR"

	os.chdir(now)

	ret_now = now

	for label in labels :
	
		
		if label == 'E' :
		
			mobile = True
			
		else :
		
			mobile = False
		
		
		now = ret_now
	
		os.chdir(now)

		abb = label_dict[label]
	
		os.mkdir(client + label)
	
		now += "/" + client + label
	
		os.chdir(now)
	
		os.mkdir(client + "_" + abb + "EM")
		os.mkdir(client + "_" + abb + "SV")

		#now = os.getcwd()
	
		now += "/" + client + "_" + abb + "EM"
		os.chdir(now)

		#os.mkdir(now + "/" + client + "_ENP1")
		#os.mkdir(now + "/" + client + "MAS")

		#now = os.getcwd()
	
		os.mkdir(now + "/" + client + "_" + abb + "MAS")
	
		now += "/" + client + "_" + abb + "_E1"
	

		os.mkdir(now)
	
		os.chdir(now) ###
	
		now = os.getcwd()
	
		now += "/" + client + "_" + abb + "_E1"
	
		os.mkdir(now)
	
	
		os.chdir(now)

		lst = ["_FS", "_PS", "_SS"]


		for item in lst :
			os.mkdir(now + "/" + client + item + "_" + abb + "_E1")
	
		now = now.split("/")
		now = "/".join(now[:-3]) + "/" + client + "_" + abb + "SV"
		os.chdir(now)

		os.mkdir(now + "/" + client + "_" + abb + "SVMAS")

		if not mobile :

			for num in [1, 2, 3, 4, 5, 6] :

				os.mkdir(now + "/" + client + "_" + abb + "SV_P" + str(num))

		else :

			os.mkdir(now + "/" + client + "_" + abb + "SV_P" + '1')

		now += "/" + client + "_" + abb + "SVMAS"
		os.chdir(now)

		lst = ["Aw", "Dy", "Pl", "Sh", "Sl"]

		for item in lst :
			os.mkdir(now + "/" + item) 
	
		if not mobile :

			lst = ["Aw", "DS", "GN", "PL", "SC"]

			for num in [1, 2, 3, 4, 5, 6] :

				now = now.split("/")
				now = "/".join(now[:-1])
				name = "SV_P" + str(num) + "_"
				now += "/" + client + "_" + abb + name[:-1] 
				os.chdir(now)

				for item in lst :

					os.mkdir(now + "/" + client + "_" + abb + name + item)
					
				#if mobile :
				#	to_write = 'Offers'
				#else :
				#	to_write = 'Reviews'

				to_write = 'Rs'
		
				os.mkdir(now + "/" + "! " + client + "_" + abb + name + to_write)
			
		else :

			now = now.split("/")
			now = "/".join(now[:-1])
			name = "SV_P" + '1' + "_"
			now += "/" + client + "_" + abb + name[:-1] 
			os.chdir(now)

			lst = ["_Os", "_Aw", "_DS"]

			new = ['M1', 'M2', 'M3']

			for newthing in new :

				temp = now + "/" + client + "_" + abb + name + newthing

				os.mkdir(temp)
				os.chdir(temp)

				for item in lst :

					if item == '_Os' :

						os.mkdir(temp + "/" + "!" + client + "_" + abb + name + newthing + item)

					else :

						os.mkdir(temp + "/" + client + "_" + abb + name + newthing + item)

			os.chdir(now)
	


	now = directory + "/" + client + "_DS"

	dealer = client
	#os.chdir(now) 

	#os.mkdir(now + "/" + client + "_Brand_NEW_Working_DataMAS")

	#now += "/" + client + "_Brand_NEW_Working_DataMAS"

	os.chdir(now) 

	c_list = ['_J_C1','_J_C2','_J_C3']

	sub_lists = [('EM', ['_Rw', '_Ad', '_Hd', '_Fl']), ('_DT', ['_Rs', '_Ad', '_Hd', '_FP']), ('_AP', ['_Rw', '_Md', '_Fl', '_Fc']), ('_RM', [])]

	os.mkdir("!!!!!! Mc")

	os.chdir(os.getcwd() + "/" + "!!!!!! Mc")


	for item in c_list :
	
		name = dealer + item
		os.mkdir(os.getcwd() + "/" + name)
		os.chdir(os.getcwd() + "/" + name)

		for thing in sub_lists :
		
			main = thing[0]
			subs = thing[1]

			temp_name = name + main
			os.mkdir(temp_name)
			os.chdir(os.getcwd() + "/" + temp_name)
		
			if main == "_RM" :
		
				file = open(temp_name + "_AP.csv", 'w')
				file.write("FirstName,LastName,Phone")
				file.close()
		
			else :
		
				for sub in subs :
					os.mkdir(temp_name + sub)
			
			os.chdir("/".join(os.getcwd().split("/")[:-1]))
			
		os.chdir("/".join(os.getcwd().split("/")[:-1]))
	
	os.chdir("/".join(os.getcwd().split("/")[:-2]))

	lst = ["! Ds", "!! Sa", "!!! Ss", "Hs", "!!!! PP", "!!!!! Sa", "De"] 

	for item in lst :
		os.mkdir(now + "/" + item)
	
	now += "/" + "!! Sa"

	os.chdir(now)

	lst = ["M1", "M2", "Sd"]

	for item in lst :
		os.mkdir(now + "/" + item)
	
	now += "/" + "M1"

	os.chdir(now)

	os.mkdir(now + "/" + "SL")
	os.mkdir(now + "/" + "SV")

	now = now.split("/")
	now = "/".join(now[:-1])

	now += "/" + "M2" 

	os.mkdir(now + "/" + "SL")
	os.mkdir(now + "/" + "SV")

	now = now.split("/")
	now = "/".join(now[:-2])

	now += "/" +  "!!! Ss" 

	os.chdir(now)

	lst = ["Ms", "Mk", "M2k"] 

	for item in lst :
		os.mkdir(now + "/" + item)
	
	now = now.split("/")
	now = "/".join(now[:-1])

	now += "/" +  "!!!! PP" 

	os.chdir(now)

	for item in ["Is", "Rs"] :
		os.mkdir(item) 

	now = now.split("/")
	now = "/".join(now[:-1])
	now += "/" + "!!!!! Sa" 
	os.chdir(now)

	for item in ["Hl", "Ms", "Sn"] :
		os.mkdir(now + "/" + item)
	
	now += "/" + "Hl"
	os.chdir(now) 

	for item in ["HM", "HL", "HV"] : 
		os.mkdir(now + "/" + item)
	
	now = now.split("/")
	now = "/".join(now[:-2])
	now += "/" + "De" 

input1 = input("Enter Client Name_ ")

if input1 == 'file' :
	file = open('clients.txt') 
	for line in file :
		folder_make(line)
		os.chdir(base_directory)
		
else :
	folder_make(input1)
