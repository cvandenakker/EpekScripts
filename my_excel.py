#The following class is an effort to compile some of my most common tasks at work into a comprehensive class.
#It is called 'my_excel' because it combines the functionality of many of the excel operations I use with
#specialized needs at my current job. It is a bit like a very simple PANDAS tailored to my work.
#It includes an algorithm 'map_cols' to detect characteristics and relevance of data when column names or keywords
#are missing.

class myexcel:

	import csv
	import os
	import re
	from dateutil.parser import parse

	def __init__(self, interactive=True, keyword='csv', encoding='utf-8', os=os, csv=csv):
		self.interactive=interactive
		if interactive:
			keyword = input('Enter filename keyword or enter for csv file_ ')
			if len(keyword) < 1:
				keyword='csv'
		else:
			keyword=keyword
		keyword=keyword.lower()
		for file in os.listdir(os.getcwd()):
			if keyword in file.lower():
				print("\nFile used: {}".format(file))
				self.output_name = "_" + file.replace(".csv", "__Output.csv")
				with open(file, encoding=encoding, newline='') as csvfile:
					data = csv.reader(csvfile, delimiter=',', quotechar='"')
					self.data = list(data)
					self.save = self.data.copy()
					self.headers = [item.strip().lower() for item in self.data[0]]
					self.data = self.data[1:]
					self.make_mappers()
				break

	def __len__(self):
		self.length = len(self.data)
		return self.length


	def make_mappers(self):
		self.map_dict_hdr = {header: i for i, header in enumerate(self.headers)}
		self.map_dict_idx = {i: header for i, header in enumerate(self.headers)}
		self.make_main_dict()


	def make_main_dict(self):
		main_list = ['first', 'last', 'address', 'city', 'state', 'zip', 'postal']
		main_dict=dict()
		for main in main_list:
			for i, header in enumerate(self.headers):
				if main in header.lower():
					main_dict[main] = i
					break
		for main in main_list:
			if main not in main_dict:
				main_dict[main] = None
		self.main_dict=main_dict


	def get_headers(self, format=False):
		if format:
			return "\n" + "\n".join([". ".join([str(i), header]) for i, header in enumerate(self.headers)]) + "\n"
		return self.headers


	def shorten(self, howmuch=100):
		self.data = self.data[:howmuch]
		self.length = len(self.data)


	def restore(self):
		self.data = self.save
		self.headers = self.data[0]
		self.data = self.data[1:]
		self.make_mappers()


	def keep_cols(self, inds=[]):
		if self.interactive:
			print(self.get_headers(True))
			choice = input("Input headers to keep, using ',' and '-' for range_ ")
			choice = choice.split(",")
			inds=[]
			for sub in choice:
				if "-" in sub:
					sub = sub.split("-")
					inds.extend(list(range(int(sub[0]), int(sub[1])+1)))
				else:
					inds.append(int(sub))
		else:
			inds=inds
		
		self.headers=[self.headers[i] for i in inds]
		new_data=list()
		for line in self.data:
			new_data.append([line[i] for i in inds])
		self.data=new_data
		self.make_mappers()


	def dedupe(self, column_inds=[]):
		if self.interactive:
			print(self.get_headers(True))
			choice = input("Input header numbers separated by commas with underscore + priority column, or Enter for all_ ")
			if len(choice) > 0:
				if "_" in choice:
					priority_index=int(choice[choice.find("_")+1:])
					choice=choice[:choice.find("_")]
				else:
					priority_index=None
				column_inds = [int(i) for i in [subi.strip() for subi in choice.split(",")]]
			else:
				column_inds = [ind for ind in self.map_dict_idx]

			print("\nRemoving duplicates by {} ... \n".format("\n".join([self.map_dict_idx[i] for i in column_inds])))
			if priority_index != None:
				print("Priotizing by {} ... \n".format(self.map_dict_idx[priority_index]))
		else:
			column_inds=column_inds

		new_data=list()
		sup_dict=dict()

		for line in self.data:
			if priority_index != None:
				if len(line[priority_index]) > 0:
					priority=1
				else:
					priority=0
			else:
				priority=None

			key = tuple([line[i].strip().lower() for i in column_inds])
			try:
				sup_dict[key].append([priority]+line)
			except:
				sup_dict[key]=list()
				sup_dict[key].append([priority]+line)

		for item in sup_dict:
			retlist=sorted(sup_dict[item], reverse=True)[0][1:]
			new_data.append(retlist)
		self.data=new_data
		if self.interactive:
			print('New doc length: ' + str(len(self)))


	def preview(self, howmuch=5):
		howmuch+=1
		print("\n"+"\n".join(["{}:  ".format(header) + ", ".join([line[self.map_dict_hdr[header]] for line in self.data[1:howmuch]]) for header in self.headers])+"\n")


	def make_output(self, xver=False, encoding='utf-8', no_blanks=False, csv=csv, os=os):
		if xver:
			id_terms=['EDID', 'ID', 'Customers_GlobalCustomerID', 'GlobalCustomerID']
			email_headers = set(id_terms + ["Email " + str(i) for i in range(1,9)])
			email_inds = [i for i, header in enumerate(self.headers) if header.strip() in email_headers]
			retrieved_headers = [self.headers[i] for i in email_inds]
			edid=False
			output_name = self.output_name.replace(".csv", "_toVerify.csv")
			for id_term in id_terms:
				if id_term in retrieved_headers:
					edid=True
					write_headers=["ColNum","ID", "FirstName", "LastName", "Email"]
					break
			else:
				print("_ID COLUMN NOT FOUND_")
				write_headers=["ColNum", "FirstName", "LastName", "Email"]

		else:
			output_name=self.output_name
			write_headers=self.headers

		keep_dir = os.getcwd()
		try:
			os.chdir("..")
			os.chdir(os.getcwd() + "/" + "_MyExcelOutput")
		except:
			os.chdir(keep_dir)

		no_email=set(["abc", "123", "n","cd", "info", "wng", "email", "none", "na", "no", "dnh", "noemail", "doesnothave",  "declined", "decline", "n/a", "refused", "noname", "nothing"])

		with open(output_name, 'w', encoding=encoding, newline='') as csvfile:
			output_writer=csv.writer(csvfile, delimiter=',', quotechar='"')
			output_writer.writerow(write_headers)
			email_sup_set=set()
			for line in self.data:
				if xver:
					try:
						first = line[self.main_dict['first']] 
						last = line[self.main_dict['last']]
					except:
						first = ''
						last = ''
					col_num=0
					if edid:
						edid = line[email_inds[0]]
						sub_list = [line[i] for i in email_inds[1:]]
					else:
						sub_list = [line[i] for i in email_inds]
					for email in sub_list:
						if edid:
							output_writer.writerow([str(col_num), edid, first, last, email])
						else:
							output_writer.writerow([str(col_num), first, last, email])
						continue

						if len(email) > 0 and email not in email_sup_set and "@" in email and "." in email:
							email = email.strip().lower()
							email_parts = email.split('@')
							name = email_parts[0]
							domain = email_parts[1]
							if name in no_email or domain[:domain.rfind(".")] in no_email:
								continue
							col_num+=1
							if edid:
								output_writer.writerow([str(col_num), edid, first, last, email])
							else:
								output_writer.writerow([str(col_num), first, last, email])
							email_sup_set.add(email)
						else:
							break
				elif no_blanks:
					if len("".join([entry.strip() for entry in line])) < 1:
						continue
					output_writer.writerow(line)
				else:
					output_writer.writerow(line)
		csvfile.close()
		os.chdir(keep_dir)


	def to_list(self):
		return [self.headers] + self.data


	def to_datetime(self, col_ind=0, dateparser=parse):
		if self.interactive:
			print(self.get_headers(True))
			col_ind = int(input("Select column by number_ "))
		else:
			col_ind=col_ind
		new=list()
		for line in self.data:
			entry = line[col_ind]
			try:
				entry = dateparser(entry, yearfirst=True)
			except:
				entry=entry
			newline=line
			newline[col_ind] = entry
			new.append(newline)
		self.data=new


	def get_cols(self, col_ind=0, dateparser=parse):
		if self.interactive:
			print(self.get_headers(True))
			col_ind = int(input("Select column by number_ "))
		else:
			col_ind=col_ind
		col_all=list()
		col_set=set()
		for line in self.data:
			entry = line[col_ind].strip()
			if len(entry) < 1:
				continue
			col_all.append(entry)
			col_set.add(entry.lower())

		col_length = len(col_all)
		col_all = sorted(col_all)

		if col_length > 0: 
			col_all_display = col_all[::100]
			print("\n{}:\n\n{}".format(self.map_dict_idx[col_ind], "\n".join(col_all_display)))

		print("\nNumber of values: {}".format(col_length))
		print("Number of unique values: {}\n".format(len(col_set)))
		return col_all, col_set


	def map_cols(self, re=re):
		target_headers = ["first" ,"last", "address", "city", "state", "zip", "email", \
		"date", "year", "make", "model", "type", "cost","ronumber"]
		year_set = set(['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008',\
		 '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'])
		first_names={'phillip', 'gilberto', 'jamel', 'vance', 'kendrick', 'raymond', 'alva', 'jonathon', 'bud', 'darren', 'mike', 'bernard', 'nathaniel', 'salvador', 'dustin', 'jeffery', 'toney', 'vaughn', 'maria', 'herbert', 'dino', 'rafael', 'renaldo', 'everette', 'terrance', 'joshua', 'dante', 'carter', 'jamaal', 'mitch', 'britt', 'elbert', 'rodolfo', 'freddy', 'julius', 'rolando', 'grady', 'valentine', 'bert', 'floyd', 'patricia', 'sanford', 'thad', 'deon', 'laverne', 'sonny', 'jonah', 'wally', 'jared', 'sherman', 'barney', 'kory', 'wayne', 'ruben', 'peter', 'teodoro', 'kieth', 'lanny', 'marion', 'newton', 'elias', 'haywood', 'august', 'mariano', 'gerry', 'rupert', 'sal', 'damion', 'hayden', 'fritz', 'monte', 'andres', 'daron', 'dennis', 'will', 'andre', 'rey', 'eduardo', 'jeramy', 'oscar', 'shelby', 'ulysses', 'erwin', 'scottie', 'walton', 'winfred', 'antony', 'blaine', 'stanton', 'freddie', 'enoch', 'houston', 'timmy', 'wesley', 'bryant', 'cortez', 'delmar', 'jerald', 'nicky', 'sydney', 'walter', 'zachariah', 'tad', 'arturo', 'shirley', 'dane', 'royal', 'howard', 'lyman', 'geraldo', 'monty', 'jc', 'lewis', 'vicente', 'keven', 'allen', 'hiram', 'bruno', 'donn', 'mitchell', 'cornelius', 'burt', 'abe', 'chuck', 'samuel', 'chadwick', 'jessie', 'darrell', 'carlton', 'cleveland', 'nigel', 'rich', 'don', 'buster', 'clement', 'franklyn', 'reinaldo', 'joe', 'wilmer', 'oliver', 'nickolas', 'ian', 'lauren', 'devin', 'mathew', 'roderick', 'cleo', 'fabian', 'richard', 'deshawn', 'darron', 'augustus', 'deandre', 'darell', 'kirby', 'lionel', 'dwayne', 'stephan', 'roman', 'romeo', 'valentin', 'jean', 'terrence', 'norbert', 'miquel', 'curtis', 'dick', 'junior', 'garland', 'franklin', 'noble', 'broderick', 'rodger', 'moses', 'kim', 'ike', 'bradley', 'antonia', 'wilson', 'elden', 'frank', 'lane', 'markus', 'morgan', 'weldon', 'carl', 'timothy', 'granville', 'emmanuel', 'kenny', 'otis', 'aron', 'federico', 'gustavo', 'irwin', 'elvin', 'jackie', 'irving', 'antone', 'emmitt', 'ricardo', 'troy', 'erin', 'loren', 'diego', 'rickie', 'amado', 'cecil', 'max', 'robt', 'brice', 'carroll', 'billy', 'marlin', 'quinn', 'calvin', 'johnny', 'forest', 'booker', 'tommy', 'edmundo', 'erich', 'dan', 'kenneth', 'john', 'wilfredo', 'nestor', 'zachary', 'mack', 'ali', 'carson', 'roscoe', 'asa', 'stacy', 'jon', 'foster', 'len', 'owen', 'whitney', 'dario', 'glen', 'maurice', 'tim', 'miles', 'paul', 'felix', 'edmund', 'isidro', 'boyce', 'claudio', 'avery', 'spencer', 'bernie', 'jeremy', 'jasper', 'kelley', 'isaac', 'jayson', 'eldridge', 'chauncey', 'joey', 'andreas', 'lou', 'loyd', 'wallace', 'jarod', 'norris', 'heath', 'elisha', 'neville', 'brady', 'kirk', 'zack', 'erasmo', 'emerson', 'reginald', 'ahmad', 'jim', 'parker', 'ellsworth', 'kurt', 'virgilio', 'ronny', 'mitchel', 'josiah', 'devon', 'agustin', 'maxwell', 'sidney', 'harris', 'denis', 'jeff', 'rosario', 'keneth', 'dalton', 'lester', 'carmine', 'trey', 'kraig', 'guillermo', 'lupe', 'pierre', 'brendon', 'korey', 'kurtis', 'ralph', 'rodrick', 'alex', 'rudy', 'darrel', 'sergio', 'angel', 'lenny', 'arnold', 'charles', 'jody', 'damon', 'winston', 'chase', 'omer', 'cordell', 'leigh', 'filiberto', 'sam', 'domenic', 'trent', 'bart', 'jamison', 'hong', 'edmond', 'jerrell', 'chung', 'preston', 'solomon', 'travis', 'jamey', 'ronald', 'leonard', 'mauricio', 'renato', 'waylon', 'adrian', 'douglas', 'rhett', 'dusty', 'lyndon', 'florencio', 'thomas', 'clair', 'doyle', 'kris', 'kristopher', 'darius', 'jed', 'donny', 'dexter', 'gabriel', 'micheal', 'scotty', 'abram', 'freeman', 'fernando', 'hilton', 'bryon', 'marcellus', 'sid', 'odell', 'octavio', 'darrin', 'jerold', 'neal', 'shaun', 'chi', 'adan', 'ned', 'nicholas', 'shon', 'dorsey', 'leo', 'jonas', 'douglass', 'ezequiel', 'jame', 'benedict', 'lucien', 'cesar', 'elwood', 'wes', 'mervin', 'johnathon', 'rudolf', 'kevin', 'boyd', 'derrick', 'jose', 'lamont', 'burton', 'jules', 'lindsay', 'noah', 'raphael', 'ronnie', 'emile', 'curt', 'frankie', 'michel', 'teddy', 'dong', 'shannon', 'titus', 'tyrell', 'sylvester', 'von', 'randolph', 'willie', 'james', 'daren', 'long', 'daryl', 'ted', 'francisco', 'eldon', 'sang', 'hunter', 'gerard', 'dwight', 'gail', 'isaiah', 'quintin', 'charlie', 'myron', 'rob', 'tuan', 'wilbert', 'kareem', 'phil', 'benny', 'steven', 'hai', 'bennett', 'tyson', 'carol', 'eddie', 'stevie', 'theodore', 'louis', 'milan', 'johnson', 'bennie', 'trinidad', 'frederic', 'vern', 'jermaine', 'earl', 'russ', 'hank', 'humberto', 'olin', 'rodrigo', 'leonardo', 'brant', 'philip', 'art', 'ellis', 'florentino', 'clifton', 'claude', 'columbus', 'marvin', 'leroy', 'jerrold', 'antione', 'kelly', 'gordon', 'roger', 'earle', 'keith', 'emery', 'luis', 'ismael', 'dean', 'jack', 'al', 'sean', 'alvaro', 'hoyt', 'mohamed', 'joseph', 'herschel', 'dwain', 'garret', 'jaime', 'clyde', 'ashley', 'malik', 'man', 'derek', 'graham', 'randell', 'reid', 'robby', 'albert', 'cedrick', 'luigi', 'arron', 'major', 'nelson', 'ramon', 'royce', 'chet', 'toby', 'wyatt', 'ahmed', 'issac', 'shawn', 'david', 'woodrow', 'donald', 'faustino', 'williams', 'jesse', 'rogelio', 'jamie', 'malcom', 'anton', 'sterling', 'leopoldo', 'maynard', 'anderson', 'gus', 'lenard', 'val', 'cody', 'hubert', 'rodney', 'daniel', 'buford', 'moshe', 'adalberto', 'aubrey', 'murray', 'merle', 'king', 'alexander', 'jacinto', 'tory', 'coleman', 'enrique', 'genaro', 'hipolito', 'aaron', 'jere', 'donte', 'charley', 'ethan', 'hyman', 'jerrod', 'napoleon', 'eugenio', 'desmond', 'thanh', 'del', 'terrell', 'mary', 'nicolas', 'marcel', 'lacy', 'waldo', 'clint', 'danial', 'jordan', 'berry', 'kristofer', 'harlan', 'manuel', 'harvey', 'saul', 'prince', 'erik', 'tracey', 'rayford', 'casey', 'damien', 'garrett', 'chance', 'edgar', 'melvin', 'henry', 'morton', 'archie', 'dominique', 'lemuel', 'geoffrey', 'jorge', 'micah', 'ron', 'willard', 'matt', 'emory', 'gerardo', 'cory', 'gregorio', 'jimmie', 'craig', 'virgil', 'jospeh', 'rosendo', 'johnie', 'reynaldo', 'caleb', 'leandro', 'ezekiel', 'jacques', 'christoper', 'edgardo', 'ira', 'alphonso', 'orville', 'gregory', 'blake', 'clifford', 'connie', 'nick', 'oswaldo', 'jan', 'dillon', 'gregg', 'dave', 'mario', 'sammie', 'mac', 'cyril', 'bob', 'tyree', 'benito', 'colby', 'lincoln', 'reyes', 'eliseo', 'numbers', 'ezra', 'orval', 'jarrett', 'son', 'simon', 'mohammed', 'jackson', 'dudley', 'lee', 'francis', 'irvin', 'lucio', 'tomas', 'warner', 'dominick', 'marshall', 'johnnie', 'thurman', 'danny', 'chester', 'adolfo', 'chris', 'fidel', 'harrison', 'alejandro', 'olen', 'ramiro', 'german', 'margarito', 'garth', 'marco', 'bryan', 'isaias', 'rick', 'harry', 'elijah', 'eloy', 'weston', 'cornell', 'ben', 'angelo', 'alfonzo', 'isreal', 'dale', 'lorenzo', 'abraham', 'damian', 'arlen', 'monroe', 'randal', 'leslie', 'guy', 'cristobal', 'leland', 'wilbur', 'joaquin', 'hobert', 'marlon', 'alvin', 'orlando', 'odis', 'raymon', 'linwood', 'bill', 'cedric', 'christopher', 'marty', 'morris', 'cary', 'kermit', 'carlo', 'reed', 'refugio', 'ward', 'vito', 'cole', 'aurelio', 'dannie', 'galen', 'gino', 'alonso', 'hal', 'bruce', 'marcelino', 'duane', 'myles', 'rod', 'adolph', 'rex', 'allan', 'armando', 'darwin', 'bertram', 'lavern', 'palmer', 'jesus', 'buck', 'darrick', 'elvis', 'josh', 'ollie', 'ricky', 'tracy', 'greg', 'wilburn', 'delmer', 'trevor', 'jamal', 'ken', 'jordon', 'edward', 'lesley', 'sandy', 'kerry', 'willis', 'vernon', 'rufus', 'scot', 'dewitt', 'lon', 'brock', 'jonathan', 'colton', 'giovanni', 'israel', 'carey', 'perry', 'raymundo', 'antonio', 'edison', 'pat', 'brett', 'luciano', 'neil', 'sammy', 'lawerence', 'ernesto', 'chong', 'rubin', 'dominic', 'leif', 'evan', 'santo', 'tom', 'yong', 'demetrius', 'burl', 'gerald', 'billie', 'shane', 'dylan', 'normand', 'antwan', 'lucius', 'colin', 'terence', 'andy', 'homer', 'norman', 'stacey', 'nathanial', 'dana', 'levi', 'cristopher', 'stuart', 'millard', 'ervin', 'lamar', 'norberto', 'vincent', 'ariel', 'boris', 'dirk', 'martin', 'mikel', 'blair', 'randall', 'miguel', 'michale', 'horace', 'shayne', 'eddy', 'tobias', 'marc', 'marcus', 'steve', 'wade', 'shelton', 'van', 'julian', 'anibal', 'warren', 'carmelo', 'bobbie', 'rocco', 'sebastian', 'william', 'collin', 'josue', 'rory', 'carlos', 'elliott', 'heriberto', 'jarvis', 'alton', 'logan', 'lynn', 'lucas', 'jacob', 'oren', 'rolland', 'ross', 'arnulfo', 'rolf', 'michael', 'byron', 'corey', 'lindsey', 'sung', 'forrest', 'wilber', 'joesph', 'hassan', 'chas', 'todd', 'fredrick', 'errol', 'kyle', 'porfirio', 'everett', 'milford', 'ignacio', 'dallas', 'lance', 'rudolph', 'ryan', 'tyron', 'delbert', 'francesco', 'frances', 'bo', 'brian', 'grover', 'mickey', 'reuben', 'ty', 'johnathan', 'beau', 'dorian', 'jason', 'bernardo', 'claud', 'hershel', 'eli', 'otto', 'huey', 'alexis', 'roland', 'gayle', 'gene', 'fredric', 'xavier', 'roy', 'gaylord', 'hugo', 'jefferson', 'robert', 'pedro', 'gil', 'harland', 'clayton', 'eric', 'armand', 'scott', 'tyler', 'leonel', 'dion', 'alonzo', 'austin', 'jimmy', 'fermin', 'luke', 'carmen', 'larry', 'jake', 'pablo', 'taylor', 'cletus', 'andrew', 'elmo', 'marquis', 'malcolm', 'adam', 'basil', 'darin', 'elroy', 'laurence', 'eugene', 'riley', 'seth', 'santiago', 'tod', 'robbie', 'denver', 'carrol', 'salvatore', 'zachery', 'wiley', 'alan', 'noe', 'bryce', 'karl', 'pasquale', 'patrick', 'raul', 'seymour', 'rusty', 'cliff', 'clinton', 'elton', 'joan', 'garfield', 'andrea', 'rene', 'courtney', 'quinton', 'wm', 'hung', 'giuseppe', 'leon', 'stefan', 'fletcher', 'lonnie', 'minh', 'santos', 'merlin', 'davis', 'emil', 'ivan', 'justin', 'herb', 'ferdinand', 'cruz', 'modesto', 'raleigh', 'merrill', 'landon', 'stanford', 'tanner', 'barton', 'isiah', 'jerry', 'lyle', 'mauro', 'vince', 'winford', 'abdul', 'alfredo', 'jeremiah', 'joel', 'sol', 'theron', 'efrain', 'tommie', 'russell', 'werner', 'lynwood', 'tony', 'kelvin', 'reggie', 'donnie', 'gilbert', 'mohammad', 'silas', 'stewart', 'brenton', 'victor', 'mose', 'rickey', 'rico', 'brent', 'edwin', 'michal', 'derick', 'louie', 'richie', 'quentin', 'chang', 'thaddeus', 'jerome', 'clemente', 'arthur', 'marcos', 'barrett', 'manual', 'kendall', 'benton', 'emmett', 'chad', 'gale', 'pete', 'felipe', 'roosevelt', 'noel', 'duncan', 'drew', 'stephen', 'garry', 'javier', 'maximo', 'gary', 'mel', 'trenton', 'domingo', 'willian', 'jude', 'young', 'jewel', 'ambrose', 'lawrence', 'otha', 'alec', 'roberto', 'kasey', 'amos', 'ernie', 'demarcus', 'edwardo', 'paris', 'moises', 'nathanael', 'randy', 'gaston', 'hector', 'mckinley', 'fred', 'emilio', 'omar', 'osvaldo', 'stan', 'dewey', 'jarrod', 'ed', 'zane', 'darnell', 'gonzalo', 'antoine', 'kip', 'tristan', 'bret', 'ernest', 'branden', 'abel', 'doug', 'rashad', 'juan', 'conrad', 'jeffry', 'fausto', 'bradford', 'graig', 'keenan', 'nolan', 'shad', 'denny', 'hilario', 'clarence', 'harold', 'jeffrey', 'jeromy', 'rigoberto', 'clark', 'terry', 'danilo', 'hosea', 'horacio', 'truman', 'jae', 'dee', 'julio', 'ray', 'wendell', 'marcelo', 'walker', 'bradly', 'lazaro', 'donovan', 'wilfred', 'felton', 'brendan', 'jamar', 'donnell', 'frederick', 'augustine', 'brad', 'efren', 'grant', 'kenton', 'alberto', 'eusebio', 'kennith', 'alphonse', 'coy', 'earnest', 'brooks', 'wilford', 'jewell', 'barry', 'alfred', 'hollis', 'hugh', 'josef', 'willy', 'sheldon', 'anthony', 'ivory', 'guadalupe', 'les', 'robin', 'herman', 'jess', 'bobby', 'alden', 'porter', 'rocky', 'deangelo', 'mason', 'erick', 'arden', 'buddy', 'lonny', 'clay', 'jay', 'arnoldo', 'elliot', 'gavin', 'vincenzo', 'esteban', 'christian', 'theo', 'benjamin', 'rueben', 'percy', 'quincy', 'arlie', 'brandon', 'judson', 'emanuel', 'hans', 'jefferey', 'dewayne', 'elmer', 'nathan', 'russel', 'cyrus', 'mark', 'matthew', 'zackary', 'brain', 'cameron', 'stanley', 'lloyd', 'alfonso', 'george', 'lowell', 'aldo', 'milton', 'harley', 'wilton', 'luther', 'milo', 'sherwood', 'darryl', 'jarred', 'samual', 'tyrone', 'lino', 'kent', 'glenn'}
		last_names={'page', 'vance', 'kennedy', 'henson', 'frazier', 'wolf', 'raymond', 'boyer', 'knox', 'bernard', 'rogers', 'villegas', 'dejesus', 'donaldson', 'berg', 'vaughn', 'portillo', 'dodson', 'richmond', 'rhodes', 'carter', 'french', 'diaz', 'spence', 'gonzales', 'conner', 'floyd', 'shields', 'nielsen', 'hardin', 'sanford', 'cook', 'hood', 'bravo', 'watkins', 'liu', 'graves', 'sherman', 'melton', 'shaw', 'petersen', 'mckinney', 'reese', 'mahoney', 'newton', 'white', 'hernandez', 'hayden', 'lawson', 'farrell', 'dennis', 'huber', 'garner', 'butler', 'camacho', 'walton', 'mcclure', 'lowery', 'evans', 'ortega', 'burke', 'meza', 'kerr', 'hebert', 'stanton', 'garrison', 'lam', 'shepard', 'moyer', 'leach', 'sampson', 'houston', 'dickerson', 'cantrell', 'rocha', 'valdez', 'bryant', 'cortez', 'bernal', 'mayer', 'walter', 'norton', 'dyer', 'sharp', 'howard', 'watts', 'lewis', 'west', 'robinson', 'allen', 'wilkerson', 'mccarthy', 'mclaughlin', 'mitchell', 'mcguire', 'barajas', 'crane', 'welch', 'escobar', 'pittman', 'allison', 'hinton', 'rich', 'pollard', 'shaffer', 'malone', 'abbott', 'savage', 'weaver', 'oliver', 'sandoval', 'hickman', 'wise', 'macias', 'medrano', 'wiggins', 'richard', 'jennings', 'rubio', 'delarosa', 'kirby', 'barker', 'clements', 'weber', 'nunez', 'foley', 'roman', 'faulkner', 'church', 'krueger', 'simpson', 'blevins', 'olson', 'fowler', 'salinas', 'hart', 'matthews', 'curtis', 'thompson', 'rodgers', 'cardenas', 'noble', 'franklin', 'blackburn', 'proctor', 'daniels', 'avalos', 'tate', 'ortiz', 'livingston', 'moses', 'kim', 'howell', 'kramer', 'wilson', 'bradley', 'buckley', 'frank', 'lane', 'enriquez', 'morgan', 'rice', 'keller', 'villalobos', 'truong', 'glass', 'burch', 'gill', 'hudson', 'mosley', 'fernandez', 'bowman', 'knight', 'rivera', 'harrington', 'gardner', 'banks', 'guzman', 'ayers', 'carroll', 'quinn', 'landry', 'zhang', 'holmes', 'higgins', 'booker', 'mckee', 'knapp', 'mack', 'ali', 'carson', 'ramos', 'garcia', 'mills', 'foster', 'owen', 'moran', 'whitney', 'hampton', 'moore', 'hunt', 'spencer', 'miles', 'paul', 'lozano', 'flores', 'pineda', 'hogan', 'bartlett', 'felix', 'fuller', 'avery', 'vu', 'gross', 'ramirez', 'melendez', 'lugo', 'mcpherson', 'kelley', 'stafford', 'combs', 'wallace', 'norris', 'branch', 'zimmerman', 'heath', 'armstrong', 'ball', 'brady', 'underwood', 'kirk', 'lowe', 'stark', 'williamson', 'parker', 'vazquez', 'franco', 'strickland', 'pratt', 'nicholson', 'fitzpatrick', 'ventura', 'hoffman', 'maxwell', 'harris', 'boone', 'bates', 'rosario', 'woodard', 'barrera', 'swanson', 'avila', 'dalton', 'stein', 'lester', 'salazar', 'jaramillo', 'pearson', 'small', 'murphy', 'wagner', 'haynes', 'cochran', 'chen', 'curry', 'mckenzie', 'richards', 'singh', 'munoz', 'obrien', 'rangel', 'bass', 'gibbs', 'arnold', 'cherry', 'charles', 'chase', 'rush', 'fitzgerald', 'choi', 'preston', 'solomon', 'winters', 'parrish', 'dunlap', 'chung', 'travis', 'jacobs', 'cunningham', 'vaughan', 'grimes', 'velez', 'sellers', 'leonard', 'duarte', 'roberts', 'sheppard', 'pham', 'hoover', 'barr', 'douglas', 'stevens', 'schmitt', 'oneill', 'pitts', 'thomas', 'doyle', 'duffy', 'hill', 'schultz', 'mccormick', 'booth', 'hodges', 'pennington', 'montgomery', 'hale', 'galvan', 'freeman', 'zavala', 'cline', 'serrano', 'mcintyre', 'sutton', 'bowen', 'robbins', 'corona', 'strong', 'villa', 'neal', 'sierra', 'york', 'griffin', 'bautista', 'dorsey', 'sexton', 'atkinson', 'wells', 'gaines', 'meyer', 'burgess', 'wall', 'castaneda', 'esparza', 'tucker', 'parsons', 'boyd', 'person', 'stevenson', 'burton', 'perez', 'hartman', 'payne', 'rosales', 'gibson', 'goodwin', 'yoder', 'wong', 'hughes', 'vasquez', 'james', 'randolph', 'long', 'carpenter', 'caldwell', 'soto', 'mendez', 'hunter', 'peralta', 'park', 'oneal', 'parra', 'carlson', 'mcintosh', 'solis', 'spears', 'bennett', 'navarro', 'mendoza', 'johnson', 'mata', 'quintana', 'gutierrez', 'johns', 'webb', 'tran', 'ellis', 'fry', 'schwartz', 'duran', 'deleon', 'kelly', 'gordon', 'juarez', 'bell', 'stone', 'keith', 'stephens', 'rios', 'dean', 'alfaro', 'middleton', 'yang', 'kaur', 'joseph', 'harrell', 'galindo', 'ashley', 'graham', 'reid', 'estes', 'mccullough', 'nelson', 'pugh', 'golden', 'poole', 'wyatt', 'ahmed', 'david', 'walters', 'dougherty', 'haley', 'arroyo', 'williams', 'cox', 'salgado', 'huang', 'marks', 'valenzuela', 'lu', 'ballard', 'bowers', 'schneider', 'murillo', 'mora', 'magana', 'friedman', 'anderson', 'maynard', 'li', 'estrada', 'nava', 'trevino', 'sanchez', 'hamilton', 'daniel', 'briggs', 'contreras', 'murray', 'nguyen', 'davidson', 'humphrey', 'king', 'alexander', 'coleman', 'burnett', 'padilla', 'torres', 'dawson', 'boyle', 'griffith', 'parks', 'hanna', 'larson', 'hall', 'trujillo', 'mcfarland', 'terrell', 'love', 'kemp', 'rasmussen', 'dunn', 'jordan', 'xiong', 'berry', 'snow', 'walls', 'pace', 'harvey', 'ellison', 'prince', 'clarke', 'ruiz', 'lin', 'wolfe', 'morales', 'casey', 'garrett', 'giles', 'waters', 'yu', 'hester', 'romero', 'morton', 'henry', 'zamora', 'barnes', 'klein', 'adams', 'baker', 'beltran', 'yates', 'lucero', 'lara', 'cortes', 'callahan', 'calderon', 'kline', 'larsen', 'delacruz', 'benitez', 'eaton', 'craig', 'robles', 'costa', 'ibarra', 'orozco', 'farmer', 'ingram', 'crosby', 'herring', 'gregory', 'blake', 'chambers', 'vang', 'leal', 'garza', 'kane', 'robertson', 'bullock', 'dillon', 'bender', 'medina', 'peters', 'villanueva', 'adkins', 'frye', 'baldwin', 'huynh', 'lyons', 'day', 'collins', 'bailey', 'johnston', 'mann', 'hobbs', 'goodman', 'reyes', 'olsen', 'simon', 'myers', 'jackson', 'steele', 'cuevas', 'lee', 'francis', 'warner', 'ho', 'dudley', 'marshall', 'nash', 'whitehead', 'harrison', 'castillo', 'moss', 'bryan', 'arellano', 'finley', 'sparks', 'velazquez', 'browning', 'wood', 'acevedo', 'leblanc', 'cantu', 'reilly', 'campbell', 'miranda', 'hubbard', 'decker', 'jimenez', 'miller', 'huff', 'cobb', 'horne', 'glover', 'monroe', 'moon', 'mclean', 'house', 'mcdonald', 'stokes', 'mathis', 'becker', 'reyna', 'holt', 'rivers', 'wu', 'conway', 'morris', 'howe', 'reed', 'mcdaniel', 'roach', 'fuentes', 'marsh', 'ward', 'patterson', 'carrillo', 'farley', 'cole', 'shannon', 'bruce', 'vega', 'mercado', 'wilkins', 'hancock', 'newman', 'hines', 'palmer', 'russo', 'gomez', 'fischer', 'rowe', 'black', 'buck', 'maddox', 'webster', 'horn', 'willis', 'mueller', 'patel', 'holland', 'stout', 'little', 'montoya', 'hansen', 'brock', 'hurst', 'hendricks', 'alvarez', 'maldonado', 'perry', 'carey', 'beasley', 'collier', 'guerra', 'santana', 'quintero', 'harper', 'gray', 'bishop', 'beard', 'schroeder', 'vo', 'coffey', 'edwards', 'mejia', 'palacios', 'luna', 'morse', 'fleming', 'watson', 'richardson', 'hurley', 'mckay', 'good', 'wright', 'jensen', 'norman', 'manning', 'valentine', 'vincent', 'singleton', 'stuart', 'may', 'gonzalez', 'silva', 'christensen', 'bradshaw', 'lopez', 'copeland', 'reynolds', 'hopkins', 'bauer', 'martin', 'levy', 'novak', 'ponce', 'blair', 'gillespie', 'ramsey', 'randall', 'weeks', 'rivas', 'wade', 'shelton', 'cordova', 'warren', 'lang', 'cannon', 'mccarty', 'aguilar', 'owens', 'cross', 'elliott', 'bean', 'jarvis', 'ross', 'logan', 'skinner', 'lucas', 'rosas', 'davila', 'moody', 'espinosa', 'lynn', 'gates', 'atkins', 'fox', 'michael', 'stephenson', 'lindsey', 'weiss', 'holloway', 'phan', 'hardy', 'martinez', 'dominguez', 'todd', 'cummings', 'sawyer', 'everett', 'hayes', 'hicks', 'wilkinson', 'ryan', 'mccann', 'cooper', 'schaefer', 'daugherty', 'sims', 'peterson', 'ochoa', 'beil', 'rose', 'roberson', 'whitaker', 'moreno', 'mullen', 'mcdowell', 'berger', 'brewer', 'bush', 'meyers', 'nixon', 'roy', 'lambert', 'durham', 'jefferson', 'blanchard', 'blankenship', 'mcmahon', 'macdonald', 'hendrix', 'barnett', 'snyder', 'espinoza', 'sullivan', 'gentry', 'clayton', 'ware', 'scott', 'aguirre', 'byrd', 'tyler', 'pope', 'bond', 'le', 'austin', 'acosta', 'taylor', 'crawford', 'summers', 'sloan', 'herrera', 'velasquez', 'powell', 'pierce', 'sanders', 'green', 'frost', 'odom', 'cervantes', 'shepherd', 'sosa', 'odonnell', 'schmidt', 'riley', 'santiago', 'andersen', 'hutchinson', 'wiley', 'tang', 'potter', 'salas', 'patrick', 'carr', 'khan', 'bonilla', 'blackwell', 'chapman', 'jenkins', 'davenport', 'mays', 'jones', 'drake', 'sweeney', 'mccoy', 'tapia', 'huffman', 'powers', 'marin', 'morrison', 'hammond', 'leon', 'mcbride', 'fletcher', 'short', 'santos', 'woods', 'davis', 'trejo', 'ford', 'cruz', 'hawkins', 'reeves', 'barber', 'townsend', 'hess', 'tanner', 'andrews', 'barton', 'koch', 'lamb', 'figueroa', 'cabrera', 'russell', 'woodward', 'patton', 'molina', 'brown', 'stewart', 'price', 'gilbert', 'merritt', 'jacobson', 'montes', 'greene', 'barron', 'gilmore', 'harding', 'chang', 'buchanan', 'thornton', 'barrett', 'shah', 'best', 'benton', 'gallagher', 'marquez', 'lim', 'burns', 'duncan', 'oconnell', 'dickson', 'duke', 'pruitt', 'andrade', 'osborne', 'cisneros', 'oconnor', 'lynch', 'young', 'beck', 'turner', 'lawrence', 'benson', 'colon', 'morrow', 'mayo', 'suarez', 'mathews', 'villarreal', 'brennan', 'washington', 'hanson', 'cain', 'ayala', 'mullins', 'peck', 'hensley', 'chan', 'guevara', 'wang', 'flynn', 'campos', 'esquivel', 'baxter', 'conrad', 'chandler', 'mccall', 'bradford', 'nolan', 'madden', 'waller', 'conley', 'gallegos', 'clark', 'terry', 'bentley', 'saunders', 'mcclain', 'hull', 'pacheco', 'mcgee', 'meadows', 'hail', 'ray', 'cohen', 'huerta', 'walker', 'english', 'pena', 'correa', 'donovan', 'frederick', 'dixon', 'smith', 'walsh', 'rowland', 'nichols', 'valencia', 'grant', 'alvarado', 'brandt', 'cano', 'brooks', 'barry', 'rojas', 'hodge', 'rollins', 'ferguson', 'horton', 'anthony', 'arias', 'compton', 'zuniga', 'porter', 'perkins', 'herman', 'henderson', 'wheeler', 'mason', 'flowers', 'fields', 'clay', 'christian', 'benjamin', 'case', 'guerrero', 'wilcox', 'fisher', 'potts', 'simmons', 'roth', 'hahn', 'harmon', 'castro', 'cameron', 'phelps', 'stanley', 'mcmillan', 'lloyd', 'george', 'calhoun', 'mcconnell', 'greer', 'phillips', 'rodriguez', 'orr', 'gould', 'bridges', 'chavez', 'delgado', 'vargas', 'massey', 'kent', 'erickson', 'glenn'}
		auto_makes={'isuzu', 'acura', 'audi', 'am general', 'dodge', 'land rover', 'cadillac', 'aston martin', 'saturn', 'suzuki', 'nissan', 'porsche', 'subaru', 'kia', 'saab', 'fiat', 'chrysler', 'gmc', 'bmw', 'buick', 'plymouth', 'mini', 'scion', 'volkswagen', 'ram', 'lincoln', 'merkur', 'geo', 'toyota', 'mazda', 'eagle', 'volvo', 'datsun', 'daewoo', 'bentley', 'mercury', 'infiniti', 'jaguar', 'hummer', 'jeep', 'mercedes-benz', 'hyundai', 'lexus', 'pontiac', 'mitsubishi', 'auto make', 'chevrolet', 'oldsmobile', 'ford', 'ferrari', 'tesla', 'honda'}
		auto_models={'dynasty', 'z8', 'mustang svt cobra', 'is 250', '850', 'fifth avenue', 'discovery', 'silverado 1500', 'amanti', 'commander', 'nova', 'passport', 'trailblazer ext', 'taurus x', 'scorpio', 'taurus', 'tucson', 'express passenger', 'm-class', 'm30', 'express', 'mkt', 'probe', 'durango', 'prius plug-in hybrid', 'silverado 3500hd cc', 'a8 l', 'cx-9', 'r8', 'aztek', 'charger', 'caprice', 'cobalt', 'h1', 'sonata', 'avalanche', 'capri', 'xc60', 'gl-class', 'fusion energi', 'ascender', 'x3', 'hhr', 'sonoma', 'toronado', 'cube', 'legend', 'aries america', 'patriot', 'e-series cargo', 'storm', '6 series', 'santa fe sport', 'range rover evoque', 'ls 430', 'element', 'omega', 'cutlass supreme', 'colorado', 'quest', 'sierra 2500hd classic', 'rx-8', 'continental gtc v8', 'borrego', 'daytona', 'stratus', 'ram 150', 'aries k', 'black diamond avalanche', 'aerio', 'rondo', 'clk', 'villager', 'x5 m', 'tl', 'panamera', 'qx80', 's-10', 'g8', 'gti', 'impreza', 'lr4', 'volt', 'optima hybrid', '940', 'escalade esv', 'cruze', 'q7', 'elantra gt', 'tahoe', 'g5', 'maxima', 'mountaineer', 'qx4', 'le mans', 'silverado 2500hd', 'tribute', 'forester', 'mkz', 'roadmaster', 'aerostar', 'prius v', 'c4500 pickup', 'mpv', 'blazer', 'pilot', 's5', 'ilx', 'm56', 'sidekick', 'accent', 'spectra', 'excel', 'forenza', 'silverado 2500', 'sundance', 'eurovan', 'mazdaspeed3', 'loyale', '350z', 'outlander', 'trans sport', 'c/k 1500 series', 's80', 'sunfire', 'tempo', 'gs 300', 'tsx', 'vue', 'relay', 'is 350', 'verano', 'integra', 'cayenne', 'neon srt-4', 'silverado', 'ct 200h', 'mdx', 'traverse', 'grand vitara', 'genesis coupe', 'envoy xl', 'cooper coupe', 'e-250', 'r32', 'alero', 'lumina', 'santa fe', 'crossfire', 'sequoia', 'x6', '5 series', 'wrangler unlimited', 'ridgeline', 's-series', 'tercel', 'suburban', 'e-series chassis', 'cayman', 'mr2 spyder', 'rav4', 'savana cargo', 'sorento', '560-class', 'm37', 'aviator', 'rx 300', 'golf r', 'sentra', 'tundra', 'm5', 'entourage', 'q40', 'soul', 'vitara', 'outlander sport', 'f-250 super duty', 'gt-r', 'elantra', 'g20', 'boxster', 'rx 400h', 'a5', 'astra', 'fx45', 'h3t', 'altima hybrid', 'freelander', 'corsica', 'cts-v', 'amigo', 'crown victoria', 'm45', 'rainier', 'riviera', 'escalade hybrid', 'expedition', 'accord', 'metro', 'cutlass calais', 'camry solara', 'es 350', 'malibu hybrid', 'hardtop', 'endeavor', 'a8', 'mini ram van', 'impala', 'f-350 super duty', 'ls', 'tt', 'b-series truck', 'xj-series', 'magnum', 'pacifica', 'c/k 10 series', 'cls', 'cooper roadster', 'f-450 super duty', 'eldorado', 'ramcharger', 'sierra 1500 classic', 'is f', 'new beetle', 'trooper', 'r-class', 'raider', 'accord crosstour', 'hardbody', 'i35', 'sierra 3500hd cc', '4 series', 'stanza', 'uplander', 'camry hybrid', 'cts', 'fleetwood', 'aveo', 'nitro', 'z3', 'slk', 'brougham', '380-class', '8 series', 'malibu limited', 'sierra', '3 series', 'chevy van', 'mini e', '600', 'lss', 'monte carlo', 'samurai', 'versa', 'c-max hybrid', 'veracruz', 'cl-class', 'mariner', 'f-350', 's60', 'tracker', '370z', 'ats', 'challenger', 'sl-class', 'beetle', 'prizm', 'ram wagon', 'venture', 'xb', 'eighty-eight royale', '9-7x', 'z4', 'a7', 'altima', 'xf', 'celebrity', 'land cruiser', 'b-series pickup', 'sierra 1500hd', 's-15 jimmy', 'equus', 'hs 250h', 'eclipse spyder', 'grand am', '300m', 'celica', 'x5', 'enclave', 'f-150', 'srx', 'c/k', 'is 350c', 'navigator', 'xjl', 'milan', 'civic crx', 'db9', 'oasis', 'protege5', 'acclaim', 'cx-7', 'town car', 'camaro', 'mkx', '200 convertible', 'wrx', 'roadster', 'm', 'escort', 'shelby gt500', 'xlr', 'ram pickup 3500', 'rx 350', 'pickup', 'tiburon', 'murano', 'sierra 3500', 'v70', 'tracer', 'fiesta', 'diamante', 'prowler', '7 series', '300-class', 'c/k 20 series', 'milan hybrid', 'trailblazer', 'mks', 'journey', 'protege', 'ram cargo', 's7', 'sonic', 'xc', 'c-max energi', 'g35', 'savana passenger', '4runner', 'focus', 'ram pickup 2500', 'rl', 'sc 400', 'breeze', 'xk', 'edge', 'is 250c', 'c/k 2500 series', 's2000', 'h3', 'lhs', 'freestar', 'ram 50 pickup', '500', 's6', 'ssr', 'sx4 crossover', 'astro cargo', 'regal', 'mx-5 miata', 'q45', 'park avenue', 'sierra 2500', 'rx 330', 'qx56', 'touareg', 'avenger', 'ram pickup 1500', 'rio5', 'terrain', 'cruze limited', 'gle', 'lancer', 'acadia', 'g37 convertible', 'cl', 'marauder', 'tsx sport wagon', 'malibu', 'ram 100', 'caballero', '360 spider', 'xg350', 'silverado 1500 ss', 'montero sport', 'silverado 2500hd classic', '240sx', 'forte', 'galant', 'colt', 'envoy xuv', 'genesis', 'm6', 'shadow', 'intrigue', 'grand marquis', 'lumina minivan', 'lesabre', 's-10 blazer', 'five hundred', 'prius c', 'imperial', 'malibu classic', 'allante', '6000', 'flex', 'jetta', 'xd', 'rodeo', 'g37', 'sierra 2500hd', '760', 'solstice', 'gs 430', 'rogue select', 'safari', 'seville', 'golf', 'matrix', 'dts', 'hummer', '5000', 'e-series wagon', 'sprinter', 'xa', 'g6', 'dbs', 'e-350', 'routan', 'grand cherokee', 'v8 vantage', 'a3', 'insight', 'contour', '9-2x', 'silverado 3500 classic', 'thunderbird', 'rlx', 'yukon', 'savana', 'escape hybrid', 'zdx', 'continental', 'delta eighty-eight royale', 'mazda2', 'gx 460', 'tc', 'ls 460', 'cressida', 'windstar cargo', 'verona', 'previa', 'xk-series', 'super duty', 'mirage', 'es 300', 'impala limited', 'venza', 'spirit', 'gs 400', 'new yorker', 'glk', 'legacy', 'cc', 'sonata hybrid', 'qx60', '911', 'x1', 'eos', '190-class', 'compass', 'es 300h', 'dart', 'silverado 1500hd', 'a6', 'sx4', 'omni', 'laser', 'navigator l', 'beretta', '240', 'countryman', 'rs 7', 'elantra coupe', 'eclipse', 'sephia', 'ion red line', 'armada', 'sierra 3500 classic', 'fairmont', 'explorer sport', 'forte koup', 'xj', 'murano crosscabriolet', 'cutlass ciera', 'sierra c3', 'allroad quattro', 'tacoma', 'ram', 'cadenza', 'sls amg', 'tlx', 'x-type', 'cabrio', 'eighty-eight', 'sky', 'town and country', 'cooper hardtop', 'catera', 'truck', 'axiom', 'discovery series ii', 'fx35', 'sc 430', 'c-class', 'sportvan', 'grand voyager', 'crosstour', 'vision', 'liberty', 'es 330', 'van', 'civic del sol', 'a4', 'fusion', 'lx 470', 'ciera', 'silverado 1500 hybrid', 'xc90', 'xg300', 'ram pickup 1500 srt-10', 'c/k 3500 series', 'q50 hybrid', '740', 'mkz hybrid', 'esteem', 'xjr', 'vibe', 'silverado 1500 classic', 'cabriolet', 'reliant k', 'gto', 'juke', '260-class', 'cooper', 'lancer evolution', 'tiguan', 'concorde', 'fx37', 'sebring', 'xkr', 'ltd crown victoria', 'pathfinder', 'supra', 'aura', 'gli', 'l-series', 'expedition el', 'cr-v', 'highlander', 'range rover', 's-class', 'mark lt', 'ram van', 'sunbird', 'corolla', 'echo', 'bronco', 'sienna', 'e-class', 'astro van', '300', 'tribeca', 'passat', 'fusion hybrid', 'spark', 'xl7', 'c30', 'gs 350', 'jimmy', 'envoy', 'cx-5', 'rabbit', 'c3500 pickup', 'marquis', '200', 'sc 300', 'le baron', 'classic', 'mark vii', 'city express cargo', 'sable', 'cavalier', 'intrepid', 'explorer', '400-class', 'explorer sport trac', 'rio', 'mazdaspeed protege', 'e-150', '626', '1 series', 'lanos', 'elantra touring', 'fit', 'lancer sportback', 'talon', 'grand prix', 'h2', 'jx35', 'millenia', 'xl-7', 'lacrosse', 'sierra 1500', 'nv passenger', 'terraza', 'veloster turbo', 'sts-v', 'avalon', 'excursion', 'bravada', 'gx 470', 'encore', 'xts', 'avalon hybrid', 'freestyle', 'canyon', '200sx', 'rdx', 'is 300', 'outback', 'f250', 'forte5', 'deville', 'voyager', 'viper', 'yukon xl', 'ex35', 'dakota', 'yaris', 'touareg 2', 'veloster', 'v40', 'ranger', 'stealth', 'wrangler', 'trooper ii', 'slx', 'montana', 'g-class', 'c70', 'torrent', 'express cargo', 'fj cruiser', 'qx70', 'outlook', 'silverado 3500', 's70', 'prius', 's-type', 'g3', 'rsx', 'versa note', 'gls', 'cooper countryman', '420-class', 'cherokee', 'xterra', 'bonneville', 'm35', 'cougar', 'leaf', 's40', 'sts', 'q70', 'v50', 'escape', 'cirrus', 'odyssey', 'civic', 'highlander hybrid', 'q5', 'mustang', 'sierra 3500hd', 'commercial vans', 'q50', 'sedona', 'escalade', 'firebird', 'h2 sut', 'range rover evoque coupe', 'vehicross', 'ls 400', 'grand caravan', 'g37 coupe', 'xv crosstrek', 'brz', 'silhouette', 'rx 450h', 'cla', 'm3', 'equinox', 'starion', 'range rover sport', 'aspen', 'nv cargo', 'silverado 3500hd', 'econoline', 'sportage', 'optima', 'escalade ext', 'montego', 'mark viii', 'century', 'cooper clubman', 'corvette', 'rogue', 'neon', 'astro', 'camry', 'mazda6', 'mazda5', 'reno', 'lx 570', 'pt cruiser', 's4', 'premier', 'xc70', 'frontier', 'titan', 'l300', 'rendezvous', 'caliber', 'transit connect', 'impulse', 'mx-6', 'montero', 'tahoe limited/z71', 'prelude', 'skylark', 'focus svt', 'ion', 'lucerne', 'rodeo sport', 'convertible', 'cooper convertible', 'nubira', '900', 'aurora', 'windstar', 'i30', 'g37 sedan', 'malibu maxx', 'mazda3', 'caravan', 'azera', 'g25 sedan'}
		states={'nh', 'tn', 'wi', 'nc', 'nv', 'il', 'wv', 'de', 'co', 'ky', 'ca', 'az', 'mi', 'ct', 'wy', 'ia', 'id', 'ma', 'mn', 'nm', 'md', 'fl', 'ny', 'nd', 'va', 'ak', 'ok', 'sc', 'pa', 'or', 'al', 'oh', 'vt', 'sd', 'ks', 'hi', 'tx', 'in', 'ut', 'wa', 'mo', 'ga', 'ri', 'ne', 'la', 'nj', 'ms', 'ar', 'me', 'mt'}
		types={'new','used','n','u'}
		headers = self.get_headers()
		headers_inds = [i for i in range(len(headers))]
		data_dict=dict()
		local_mapper=dict()

		for line in self.data:
			for col_ind in headers_inds:
				data_set = data_dict.get(col_ind, set())
				entry = line[col_ind].strip()
				if len(entry) < 1:
					continue
				data_set.add(entry.lower())
				data_dict[col_ind]=data_set

		for entry in target_headers:
			for key in self.map_dict_hdr:
				if entry in key:
					local_mapper[entry]=self.map_dict_hdr[key]
					break
		if len(local_mapper) == len(headers):
			return local_mapper
		else:
			unknown_headers_inds = [self.map_dict_hdr[item] for item in headers if item not in local_mapper]
			unknown_dict={i:list() for i in unknown_headers_inds}
			for i in unknown_headers_inds:
				
				try:
					#here, we need to analyze the data and compare against the missing cols
					#goign to do this stuff behind the scenes, displays conclusions, if not correct, gives user options to manually assign
					data_to_analyze=data_dict[i]

					address_count=0
					first_name_count=0
					last_name_count=0
					auto_make_count=0
					auto_model_count=0
					state_count=0
					city_count=0
					type_count=0
					cost_count=0
					email_count=0
					year_count=0
					zip_count=0
					date_count=0

					for entry in data_to_analyze:

						entry = re.sub(r'[^A-Za-z0-9./@-]','', entry)
						add_check = re.sub(r'[^A-Za-z0-9]','', entry)
						if entry.isalpha():
							if entry in states:
								state_count+=7
							if entry in first_names:
								first_name_count+=7
							elif entry in last_names:
								last_name_count+=7
							elif entry in auto_makes:
								auto_make_count+=20
							elif entry in auto_models:
								auto_model_count+=20
							elif entry in types:
								type_count+=7
							else:
								city_count+=1
						elif add_check.isalnum():
							address_count+=1
						try:
							flt_test = float(entry)
							cost_count+=1
						except:
							pass
						if '@' in entry:
							email_count+=1
						if entry.isdigit():
							if entry in year_set or len(entry) <= 3:
								year_count+=1
							else:
								zip_count+=1
						if '/' in entry:
							date_count+=1

					unknown_dict[i] = {address_count: 'address',
									first_name_count: 'first',
									last_name_count: 'last',
									auto_make_count: 'make',
									auto_model_count: 'model',
									cost_count: 'cost',
									email_count: 'email',
									year_count: 'year',
									zip_count: 'zip',
									date_count: 'date',
									city_count: 'city',
									state_count: 'state',
									type_count: 'type'}

				except:
					print('no data for {}'.format(self.map_dict_idx[i]))
					continue

			fetched_cols=set()

			for entry in unknown_dict:
				analyze_lst=sorted([(count, header) for count, header in unknown_dict[entry].items()], reverse=True)
				print(analyze_lst)
				detected_column=analyze_lst[0][1]
				local_mapper[detected_column] = entry

			missing_headers = (set(target_headers).difference(local_mapper))
			for header in missing_headers:
				local_mapper[header]=None
		if len(missing_headers) > 0:
			print('No data found for {}'.format(', '.join(missing_headers)))
		return local_mapper

	
