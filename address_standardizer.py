import csv
import os
import usaddress
import re
import sys


def convert(filename) :


	def low(up) :

		return up.group().lower()


	def pravopisanie(bad) :

		if re.search(r'\b(?:s|e|n|w|sw|se|nw|ne)\b', bad) != None :

			return bad.upper()

		bad = bad.title()

		bad = re.sub(r'[0-9]+(?:Rd|Th|St|Nd)', low, bad)

		return bad.replace('Po Box', 'PO Box')
			 


	states = set(["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])


	dict_1 = {('aly', 'alley', 'ally', 'allee'): 'ALY', ('annex', 'anx', 'annx', 'anex'): 'ANX', ('arc', 'arcade'): 'ARC', ('avnue', 'aven', 'avn', 'avenu', 'ave', 'av', 'avenue'): 'AVE', ('bayoo', 'bayou'): 'BYU', ('beach', 'bch'): 'BCH', ('bend', 'bnd'): 'BND', ('bluf', 'blf', 'bluff'): 'BLF', ('bluffs',): 'BLFS', ('bot', 'bottm', 'btm', 'bottom'): 'BTM', ('blvd', 'boulevard', 'boul', 'boulv'): 'BLVD', ('brnch', 'br', 'branch'): 'BR', ('bridge', 'brdge', 'brg'): 'BRG', ('brk', 'brook'): 'BRK', ('brooks',): 'BRKS', ('burg',): 'BG', ('burgs',): 'BGS', ('bypass', 'byp', 'bypas', 'byps', 'bypa'): 'BYP', ('cmp', 'camp', 'cp'): 'CP', ('canyon', 'cnyn', 'canyn'): 'CYN', ('cpe', 'cape'): 'CPE', ('cswy', 'causeway', 'causwa'): 'CSWY', ('cent', 'centre', 'cntr', 'ctr', 'cnter', 'center', 'centr', 'cen'): 'CTR', ('centers',): 'CTRS', ('circ', 'crcl', 'cir', 'crcle', 'circle', 'circl'): 'CIR', ('circles',): 'CIRS', ('clf', 'cliff'): 'CLF', ('cliffs', 'clfs'): 'CLFS', ('club', 'clb'): 'CLB', ('common',): 'CMN', ('commons',): 'CMNS', ('corner', 'cor'): 'COR', ('corners', 'cors'): 'CORS', ('course', 'crse'): 'CRSE', ('ct', 'court'): 'CT', ('cts', 'courts'): 'CTS', ('cv', 'cove'): 'CV', ('coves',): 'CVS', ('crk', 'creek'): 'CRK', ('crsent', 'crsnt', 'crescent', 'cres'): 'CRES', ('crest',): 'CRST', ('xing', 'crossing', 'crssng'): 'XING', ('crossroad',): 'XRD', ('crossroads',): 'XRDS', ('curve',): 'CURV', ('dl', 'dale'): 'DL', ('dm', 'dam'): 'DM', ('dv', 'dvd', 'div', 'divide'): 'DV', ('drive', 'drv', 'dr', 'driv'): 'DR', ('drives',): 'DRS', ('est', 'estate'): 'EST', ('ests', 'estates'): 'ESTS', ('expy', 'exp', 'expw', 'expr', 'express', 'expressway'): 'EXPY', ('extension', 'ext', 'extn', 'extnsn'): 'EXT', ('exts', 'extensions'): 'EXTS', ('fall',): 'FALL', ('fls', 'falls'): 'FLS', ('ferry', 'frry', 'fry'): 'FRY', ('field', 'fld'): 'FLD', ('fields', 'flds'): 'FLDS', ('flat', 'flt'): 'FLT', ('flats', 'flts'): 'FLTS', ('ford', 'frd'): 'FRD', ('fords',): 'FRDS', ('forest', 'frst', 'forests'): 'FRST', ('frg', 'forge', 'forg'): 'FRG', ('forges',): 'FRGS', ('frk', 'fork'): 'FRK', ('frks', 'forks'): 'FRKS', ('frt', 'ft', 'fort'): 'FT', ('frwy', 'fwy', 'freeway', 'frway', 'freewy'): 'FWY', ('grden', 'gardn', 'grdn', 'garden'): 'GDN', ('gardens', 'grdns', 'gdns'): 'GDNS', ('gateway', 'gatway', 'gatewy', 'gtway', 'gtwy'): 'GTWY', ('glen', 'gln'): 'GLN', ('glens',): 'GLNS', ('green', 'grn'): 'GRN', ('greens',): 'GRNS', ('grov', 'grove', 'grv'): 'GRV', ('groves',): 'GRVS', ('hbr', 'harbr', 'harbor', 'harb', 'hrbor'): 'HBR', ('harbors',): 'HBRS', ('hvn', 'haven'): 'HVN', ('heights', 'ht', 'hts'): 'HTS', ('highwy', 'hway', 'hiwy', 'hwy', 'highway', 'hiway'): 'HWY', ('hill', 'hl'): 'HL', ('hls', 'hills'): 'HLS', ('hollow', 'holw', 'holws', 'hllw', 'hollows'): 'HOLWS', ('inlet', 'inlt'): 'INLT', ('island', 'is', 'islnd'): 'IS', ('iss', 'islnds', 'islands'): 'ISS', ('isle', 'isles'): 'ISLE', ('junction', 'jctn', 'juncton', 'jct', 'jction', 'junctn'): 'JCT', ('junctions', 'jctns', 'jcts'): 'JCTS', ('key', 'ky'): 'KY', ('kys', 'keys'): 'KYS', ('knoll', 'knl', 'knol'): 'KNL', ('knls', 'knolls'): 'KNLS', ('lake', 'lk'): 'LK', ('lks', 'lakes'): 'LKS', ('land',): 'LAND', ('lndg', 'landing', 'lndng'): 'LNDG', ('lane', 'ln'): 'LN', ('light', 'lgt'): 'LGT', ('lights',): 'LGTS', ('lf', 'loaf'): 'LF', ('lock', 'lck'): 'LCK', ('locks', 'lcks'): 'LCKS', ('lodg', 'lodge', 'ldg', 'ldge'): 'LDG', ('loop', 'loops'): 'LOOP', ('mall',): 'MALL', ('mnr', 'manor'): 'MNR', ('mnrs', 'manors'): 'MNRS', ('meadow',): 'MDW', ('mdw', 'mdws', 'medows', 'meadows'): 'MDWS', ('mews',): 'MEWS', ('mill',): 'ML', ('mills',): 'MLS', ('mission', 'mssn', 'missn'): 'MSN', ('motorway',): 'MTWY', ('mount', 'mnt', 'mt'): 'MT', ('mtn', 'mntain', 'mtin', 'mntn', 'mountin', 'mountain'): 'MTN', ('mountains', 'mntns'): 'MTNS', ('nck', 'neck'): 'NCK', ('orchard', 'orch', 'orchrd'): 'ORCH', ('ovl', 'oval'): 'OVAL', ('overpass',): 'OPAS', ('prk', 'park'): 'PARK', ('parks',): 'PARK', ('pkway', 'pkwy', 'parkway', 'pky', 'parkwy'): 'PKWY', ('parkways', 'pkwys'): 'PKWY', ('pass',): 'PASS', ('passage',): 'PSGE', ('path', 'paths'): 'PATH', ('pike', 'pikes'): 'PIKE', ('pine',): 'PNE', ('pines', 'pnes'): 'PNES', ('pl', 'place'): 'PL', ('plain', 'pln'): 'PLN', ('plains', 'plns'): 'PLNS', ('plz', 'plza', 'plaza'): 'PLZ', ('point', 'pt'): 'PT', ('points', 'pts'): 'PTS', ('prt', 'port'): 'PRT', ('ports', 'prts'): 'PRTS', ('prr', 'prairie', 'pr'): 'PR', ('rad', 'radiel', 'radial', 'radl'): 'RADL', ('ramp',): 'RAMP', ('rnch', 'rnchs', 'ranches', 'ranch'): 'RNCH', ('rpd', 'rapid'): 'RPD', ('rapids', 'rpds'): 'RPDS', ('rst', 'rest'): 'RST', ('rdg', 'ridge', 'rdge'): 'RDG', ('rdgs', 'ridges'): 'RDGS', ('rvr', 'riv', 'rivr', 'river'): 'RIV', ('road', 'rd'): 'RD', ('roads', 'rds'): 'RDS', ('route',): 'RTE', ('row',): 'ROW', ('rue',): 'RUE', ('run',): 'RUN', ('shoal', 'shl'): 'SHL', ('shoals', 'shls'): 'SHLS', ('shoar', 'shore', 'shr'): 'SHR', ('shores', 'shrs', 'shoars'): 'SHRS', ('skyway',): 'SKWY', ('sprng', 'spg', 'spring', 'spng'): 'SPG', ('spngs', 'spgs', 'sprngs', 'springs'): 'SPGS', ('spur',): 'SPUR', ('spurs',): 'SPUR', ('sq', 'squ', 'sqre', 'sqr', 'square'): 'SQ', ('squares', 'sqrs'): 'SQS', ('station', 'statn', 'stn', 'sta'): 'STA', ('strvn', 'strvnue', 'straven', 'strav', 'stravenue', 'stra', 'stravn'): 'STRA', ('streme', 'strm', 'stream'): 'STRM', ('strt', 'street', 'str', 'st'): 'ST', ('streets',): 'STS', ('smt', 'summit', 'sumitt', 'sumit'): 'SMT', ('terr', 'terrace', 'ter'): 'TER', ('throughway',): 'TRWY', ('trce', 'trace', 'traces'): 'TRCE', ('trak', 'trk', 'trks', 'tracks', 'track'): 'TRAK', ('trafficway',): 'TRFY', ('trail', 'trl', 'trails', 'trls'): 'TRL', ('trailer', 'trlr', 'trlrs'): 'TRLR', ('tunl', 'tunnl', 'tunnel', 'tunnels', 'tunls', 'tunel'): 'TUNL', ('trnpk', 'turnpike', 'turnpk'): 'TPKE', ('underpass',): 'UPAS', ('un', 'union'): 'UN', ('unions',): 'UNS', ('vally', 'vly', 'vlly', 'valley'): 'VLY', ('vlys', 'valleys'): 'VLYS', ('via', 'viaduct', 'vdct', 'viadct'): 'VIA', ('view', 'vw'): 'VW', ('vws', 'views'): 'VWS', ('villiage', 'villg', 'village', 'villag', 'vlg', 'vill'): 'VLG', ('villages', 'vlgs'): 'VLGS', ('ville', 'vl'): 'VL', ('vis', 'vsta', 'vista', 'vist', 'vst'): 'VIS', ('walk',): 'WALK', ('walks',): 'WALK', ('wall',): 'WALL', ('way', 'wy'): 'WAY', ('ways',): 'WAYS', ('well',): 'WL'}
	dict_2 = {('header1',): 'header3', ('apartment',): 'APT', ('basement',): 'BSMT', ('building',): 'BLDG', ('department',): 'DEPT', ('floor',): 'FL', ('front',): 'FRNT', ('hanger',): 'HNGR', ('key',): 'KEY', ('lobby',): 'LBBY', ('lot',): 'LOT', ('lower',): 'LOWR', ('office',): 'OFC', ('penthouse',): 'PH', ('pier',): 'PIER', ('rear',): 'REAR', ('room',): 'RM', ('side',): 'SIDE', ('slip',): 'SLIP', ('space',): 'SPC', ('stop',): 'STOP', ('suite',): 'STE', ('trailer',): 'TRLR', ('unit',): 'UNIT'}
	
	# These are not official abbreviations from USPS, but appear in Google searches... they were added to dict1_vals manually : 'vista', 'knolls', 'knoll','crossing', 'field', 'hollow'

	dict1_vals = {'vista', 'knolls', 'knoll','crossing', 'field', 'pr', 'ctrs', 'grns', 'brks', 'fry', 'clfs', 'exts', 'frd', 'hwy', 'pass', 'land', 'blvd', 'clf', 'vis', 'cv', 'shr', 'rte', 'trl', 'uns', 'row', 'expy', 'spg', 'spur', 'hl', 'cp', 'fall', 'jcts', 'pnes', 'frgs', 'blfs', 'gln', 'gtwy', 'xrd', 'cmn', 'mdws', 'wl', 'cres', 'ft', 'blf', 'trce', 'pike', 'crk','creek', 'ave', 'rue', 'jct', 'dl', 'cts', 'trlr', 'byp', 'sta', 'aly', 'gdns', 'rdg', 'nck', 'radl', 'skwy', 'rd', 'mnrs', 'trwy', 'ramp', 'mdw', 'mtn', 'oval', 'vlgs', 'kys', 'fwy', 'sqs', 'hts', 'lcks', 'lf', 'brk', 'vly', 'pts', 'lck', 'btm', 'ct', 'trak', 'knls', 'xing', 'path', 'smt', 'orch', 'vw', 'is', 'shls', 'glns', 'frg', 'rnch', 'br', 'mtwy', 'shrs', 'ter', 'tpke', 'flds', 'xrds', 'knl', 'gdn', 'dm', 'clb', 'upas', 'vlg', 'rpds', 'ctr', 'prts', 'lgt', 'frst', 'bgs', 'shl', 'dv', 'sts', 'bg', 'wall', 'cor', 'arc', 'cirs', 'curv', 'crst', 'inlt', 'crse', 'mall', 'hvn', 'pne', 'tunl', 'lndg', 'ldg', 'pln', 'vl', 'ests', 'grvs', 'hls', 'cswy', 'lk', 'trfy', 'anx', 'psge', 'stra', 'hbr', 'byu', 'mtns', 'fld', 'rdgs', 'bch', 'ml', 'est', 'mews', 'spgs', 'park', 'rds', 'pl', 'plns', 'flts', 'fls', 'riv', 'ln', 'lks', 'vlys', 'strm', 'rpd', 'cpe', 'cors', 'dr', 'hbrs', 'prt', 'cir', 'frks', 'flt', 'cyn', 'loop', 'isle', 'vws', 'via', 'brg', 'cmns', 'st', 'drs', 'pt', 'un', 'lgts', 'grn', 'sq', 'iss', 'walk', 'mt', 'msn', 'rst', 'pkwy', 'opas', 'frds', 'ky', 'ways', 'bnd', 'holw', 'ext', 'mnr', 'frk', 'run', 'grv', 'cvs', 'way', 'plz', 'mls'}
	dict2_vals = {'ph', 'trlr', 'lbby', 'ste', 'spc', 'fl', 'lot', 'rear', 'header3', 'ofc', 'side', 'rm', 'slip', 'bsmt', 'apt', 'pier', 'unit', 'hngr', 'lowr', 'key', 'bldg', 'stop', 'frnt', 'dept'}

	#remove_re = r"\s(?:|ste|lot|apt|unit|bldg)\s[ #0-9a-z/-]+$" # this one is consistent but doesn't remove just numbers or just # number

	#remove_re = r"\s(?:|ste|lot|apt|unit|bldg|#)\s[ #0-9a-z/-]+$"

	remove_re = r"\s(?:ste|lot|apt|unit|bldg|trlr|#)(?:[0-9#]+$|\s.*$|$)"

	#remove_re = r"\s#[\s0-9a-z]+$|\s(?:|ste|lot|apt|unit|bldg)\s[#0-9a-z/-]+$"

	#remove_re = r"\s(?:|ste|lot|apt|unit|bldg)\s[#0-9a-z/-]+$|\s(?:|ste|lot|apt|unit|bldg)\s#[\s0-9a-z]+$"

	# 5010 LOISE ST APT 3

	numbers = {'sixth ' : '6th ', 'seventh ' : '7th ', 'eighth ' : '8th ', 'ninth ' : '9th ', 'tenth ' : '10th ', 'first ' : '1st ', 'second ' : '2nd ', 'third ' : '3rd ', 'fourth ' : '4th ', 'fifth' : '5th ', r'^(one\s)|\sone\s|\sone$' : '1 ', r'^(two\s)|\stwo\s|\stwo$' : '2 ', r'^(three\s)|\sthree\s|\sthree$' : '3 ', r'^(four\s)|\sfour\s|\sfour$' : '4 ', r'^(five\s)|\sfive\s|\sfive$' : '5 '}

	print('!! FILE USED: ' + filename)

	output = open(filename.replace(".csv", "_STANDARDIZED.csv"), 'w')

	data = csv.reader(open(filename, encoding ='latin-1'))

	directions = {r"\bnorth\b" : "n", r"\bsouth\b" : "s", r"\beast\b" : "e", r"\bwest\b" : "w"}

	for line in data :

		headers = line

		break


	try :

		for ind, header in enumerate(headers) :

			if 'address' in header.lower() :

				index = ind

				break

	except :

		print('! Address header not found !')
		sys.exit()


	output.write(",".join(headers) + "\n")


	for line in data :

		if len(line) < 1 :

			output.write('--,--\n')

			continue


		orig_ad = line[index]

		#orig_ad = orig_ad.replace(".", "")

		#print(orig_ad)

		orig_ad = orig_ad.replace(" - ","-").rstrip()

		address = re.sub(r"[^a-zA-Z0-9\s#-']", "", orig_ad.lower())


		if len(address.split(" ")) > 3 :

			for direction in directions :

				address = re.sub(direction, directions[direction], address)


		for number in numbers :

			address = re.sub(number, numbers[number], address)


		try :

			parsed = usaddress.tag(address)

			dic = parsed[0]

			#print(dic)

			flag1 = False
			flag2 = False

			if 'StreetNamePostType' in dic :

				snp = dic['StreetNamePostType']
				
				if snp not in dict1_vals :

					for item in dict_1 :

						if snp in item :

							snp_append = dict_1[item]

							flag1 = True


				if not flag1 :

					snp_append = snp
			
				dic['StreetNamePostType'] = snp_append


			if 'OccupancyType' in dic :


				ot = dic['OccupancyType']


				if ot not in dict2_vals :

					for item in dict_2 :

						if ot in item :

							ot_append = dict_2[item]

							flag2 = True

				if not flag2 :

					ot_append = ot

				dic['OccupancyType'] = ot_append

			if flag1 or flag2 :

				suf = ",**********"

			else :

				suf = ""

			#print(dic)

			write_address = " ".join([pravopisanie(dic[item]) for item in dic])

			if remove :

				write_address = re.sub(remove_re, "", write_address, flags = re.IGNORECASE)

			line[index] = write_address

			to_write = ",".join([item.upper() if item in states else pravopisanie(item.replace(",","")) for item in line]) + '\n'# + suf + "\n"


			#to_write += "," + write_address + suf + "\n" 


			output.write(to_write)
			#output.write(orig_ad + "," + " ".join([dic[item].upper() if dic[item] in directions else dic[item].title() for item in dic]).replace('County Rd', 'County Road') + suf + "\n")

			#print(dic)

		except :

			line[index] = pravopisanie(orig_ad)

			#suf = "," + pravopisanie(orig_ad) + ",!!ERROR!!\n"

			to_write = ",".join([item.upper() if item.upper() in states else pravopisanie(item.replace(",","")) for item in line]) + '\n'# + suf


			output.write(to_write)

			print('Address could not be parsed: ' + address)



#convert()


choice = input('\nRemove apartment and unit numbers? y/n_ ')

if choice == 'n' :

	remove = False

else :

	remove = True

for item in os.listdir(os.getcwd()) :

	if 'csv' in item and 'standardized' not in item :

		convert(item)





