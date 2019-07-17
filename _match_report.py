#The following script is an script I wrote to integrate nearly all aspects of a task I commonly encounter at work.
#It's principle purpose is address matching.
#It includes a series of components I have developed:
# - a data type analysis algorithm to determine what data a column contains when the column name is missing
# - an address standardizer using USPS norms to efficiently compare non-standardized addresses against other both
#standardized and non-standardized address lists
# - a function that matches column names of an arbitrary order to a separate list of column names also in an
#arbitrary order and reorders the columns in the first document to correspond to the second set
# - determines whether or not date information is present and if present, converts to datetime and sorts
# - determines if there are duplicate entries and, if so, outputs the potential duplicates to the terminal for user review
# - consistent and predictable functioning given a wide variety of input files and formats
# - easy manipulation and cuztomization of core functions in order to satisfy the evolving needs of the commpany


import csv
import sys
import re
import os
import usaddress
from datetime import date

dict_1 = {('aly', 'alley', 'ally', 'allee'): 'aly', ('annex', 'anx', 'annx', 'anex'): 'anx', ('arc', 'arcade'): 'arc', ('avnue', 'aven', 'avn', 'avenu', 'ave', 'av', 'avenue'): 'ave', ('bayoo', 'bayou'): 'byu', ('beach', 'bch'): 'bch', ('bend', 'bnd'): 'bnd', ('bluf', 'blf', 'bluff'): 'blf', ('bluffs',): 'blfs', ('bot', 'bottm', 'btm', 'bottom'): 'btm', ('blvd', 'boulevard', 'boul', 'boulv'): 'blvd', ('brnch', 'br', 'branch'): 'br', ('bridge', 'brdge', 'brg'): 'brg', ('brk', 'brook'): 'brk', ('brooks',): 'brks', ('burg',): 'bg', ('burgs',): 'bgs', ('bypass', 'byp', 'bypas', 'byps', 'bypa'): 'byp', ('cmp', 'camp', 'cp'): 'cp', ('canyon', 'cnyn', 'canyn'): 'cyn', ('cpe', 'cape'): 'cpe', ('cswy', 'causeway', 'causwa'): 'cswy', ('cent', 'centre', 'cntr', 'ctr', 'cnter', 'center', 'centr', 'cen'): 'ctr', ('centers',): 'ctrs', ('circ', 'crcl', 'cir', 'crcle', 'circle', 'circl'): 'cir', ('circles',): 'cirs', ('clf', 'cliff'): 'clf', ('cliffs', 'clfs'): 'clfs', ('club', 'clb'): 'clb', ('common',): 'cmn', ('commons',): 'cmns', ('corner', 'cor'): 'cor', ('corners', 'cors'): 'cors', ('course', 'crse'): 'crse', ('ct', 'court'): 'ct', ('cts', 'courts'): 'cts', ('cv', 'cove'): 'cv', ('coves',): 'cvs', ('crk', 'creek'): 'crk', ('crsent', 'crsnt', 'crescent', 'cres'): 'cres', ('crest',): 'crst', ('xing', 'crossing', 'crssng'): 'xing', ('crossroad',): 'xrd', ('crossroads',): 'xrds', ('curve',): 'curv', ('dl', 'dale'): 'dl', ('dm', 'dam'): 'dm', ('dv', 'dvd', 'div', 'divide'): 'dv', ('drive', 'drv', 'dr', 'driv'): 'dr', ('drives',): 'drs', ('est', 'estate'): 'est', ('ests', 'estates'): 'ests', ('expy', 'exp', 'expw', 'expr', 'express', 'expressway'): 'expy', ('extension', 'ext', 'extn', 'extnsn'): 'ext', ('exts', 'extensions'): 'exts', ('fall',): 'fall', ('fls', 'falls'): 'fls', ('ferry', 'frry', 'fry'): 'fry', ('field', 'fld'): 'fld', ('fields', 'flds'): 'flds', ('flat', 'flt'): 'flt', ('flats', 'flts'): 'flts', ('ford', 'frd'): 'frd', ('fords',): 'frds', ('forest', 'frst', 'forests'): 'frst', ('frg', 'forge', 'forg'): 'frg', ('forges',): 'frgs', ('frk', 'fork'): 'frk', ('frks', 'forks'): 'frks', ('frt', 'ft', 'fort'): 'ft', ('frwy', 'fwy', 'freeway', 'frway', 'freewy'): 'fwy', ('grden', 'gardn', 'grdn', 'garden'): 'gdn', ('gardens', 'grdns', 'gdns'): 'gdns', ('gateway', 'gatway', 'gatewy', 'gtway', 'gtwy'): 'gtwy', ('glen', 'gln'): 'gln', ('glens',): 'glns', ('green', 'grn'): 'grn', ('greens',): 'grns', ('grov', 'grove', 'grv'): 'grv', ('groves',): 'grvs', ('hbr', 'harbr', 'harbor', 'harb', 'hrbor'): 'hbr', ('harbors',): 'hbrs', ('hvn', 'haven'): 'hvn', ('heights', 'ht', 'hts'): 'hts', ('highwy', 'hway', 'hiwy', 'hwy', 'highway', 'hiway'): 'hwy', ('hill', 'hl'): 'hl', ('hls', 'hills'): 'hls', ('hollow', 'holw', 'holws', 'hllw', 'hollows'): 'holws', ('inlet', 'inlt'): 'inlt', ('island', 'is', 'islnd'): 'is', ('iss', 'islnds', 'islands'): 'iss', ('isle', 'isles'): 'isle', ('junction', 'jctn', 'juncton', 'jct', 'jction', 'junctn'): 'jct', ('junctions', 'jctns', 'jcts'): 'jcts', ('key', 'ky'): 'ky', ('kys', 'keys'): 'kys', ('knoll', 'knl', 'knol'): 'knl', ('knls', 'knolls'): 'knls', ('lake', 'lk'): 'lk', ('lks', 'lakes'): 'lks', ('land',): 'land', ('lndg', 'landing', 'lndng'): 'lndg', ('lane', 'ln'): 'ln', ('light', 'lgt'): 'lgt', ('lights',): 'lgts', ('lf', 'loaf'): 'lf', ('lock', 'lck'): 'lck', ('locks', 'lcks'): 'lcks', ('lodg', 'lodge', 'ldg', 'ldge'): 'ldg', ('loop', 'loops'): 'loop', ('mall',): 'mall', ('mnr', 'manor'): 'mnr', ('mnrs', 'manors'): 'mnrs', ('meadow',): 'mdw', ('mdw', 'mdws', 'medows', 'meadows'): 'mdws', ('mews',): 'mews', ('mill',): 'ml', ('mills',): 'mls', ('mission', 'mssn', 'missn'): 'msn', ('motorway',): 'mtwy', ('mount', 'mnt', 'mt'): 'mt', ('mtn', 'mntain', 'mtin', 'mntn', 'mountin', 'mountain'): 'mtn', ('mountains', 'mntns'): 'mtns', ('nck', 'neck'): 'nck', ('orchard', 'orch', 'orchrd'): 'orch', ('ovl', 'oval'): 'oval', ('overpass',): 'opas', ('prk', 'park'): 'park', ('parks',): 'park', ('pkway', 'pkwy', 'parkway', 'pky', 'parkwy'): 'pkwy', ('parkways', 'pkwys'): 'pkwy', ('pass',): 'pass', ('passage',): 'psge', ('path', 'paths'): 'path', ('pike', 'pikes'): 'pike', ('pine',): 'pne', ('pines', 'pnes'): 'pnes', ('pl', 'place'): 'pl', ('plain', 'pln'): 'pln', ('plains', 'plns'): 'plns', ('plz', 'plza', 'plaza'): 'plz', ('point', 'pt'): 'pt', ('points', 'pts'): 'pts', ('prt', 'port'): 'prt', ('ports', 'prts'): 'prts', ('prr', 'prairie', 'pr'): 'pr', ('rad', 'radiel', 'radial', 'radl'): 'radl', ('ramp',): 'ramp', ('rnch', 'rnchs', 'ranches', 'ranch'): 'rnch', ('rpd', 'rapid'): 'rpd', ('rapids', 'rpds'): 'rpds', ('rst', 'rest'): 'rst', ('rdg', 'ridge', 'rdge'): 'rdg', ('rdgs', 'ridges'): 'rdgs', ('rvr', 'riv', 'rivr', 'river'): 'riv', ('road', 'rd'): 'rd', ('roads', 'rds'): 'rds', ('route',): 'rte', ('row',): 'row', ('rue',): 'rue', ('run',): 'run', ('shoal', 'shl'): 'shl', ('shoals', 'shls'): 'shls', ('shoar', 'shore', 'shr'): 'shr', ('shores', 'shrs', 'shoars'): 'shrs', ('skyway',): 'skwy', ('sprng', 'spg', 'spring', 'spng'): 'spg', ('spngs', 'spgs', 'sprngs', 'springs'): 'spgs', ('spur',): 'spur', ('spurs',): 'spur', ('sq', 'squ', 'sqre', 'sqr', 'square'): 'sq', ('squares', 'sqrs'): 'sqs', ('station', 'statn', 'stn', 'sta'): 'sta', ('strvn', 'strvnue', 'straven', 'strav', 'stravenue', 'stra', 'stravn'): 'stra', ('streme', 'strm', 'stream'): 'strm', ('strt', 'street', 'str', 'st'): 'st', ('streets',): 'sts', ('smt', 'summit', 'sumitt', 'sumit'): 'smt', ('terr', 'terrace', 'ter'): 'ter', ('throughway',): 'trwy', ('trce', 'trace', 'traces'): 'trce', ('trak', 'trk', 'trks', 'tracks', 'track'): 'trak', ('trafficway',): 'trfy', ('trail', 'trl', 'trails', 'trls'): 'trl', ('trailer', 'trlr', 'trlrs'): 'trlr', ('tunl', 'tunnl', 'tunnel', 'tunnels', 'tunls', 'tunel'): 'tunl', ('trnpk', 'turnpike', 'turnpk'): 'tpke', ('underpass',): 'upas', ('un', 'union'): 'un', ('unions',): 'uns', ('vally', 'vly', 'vlly', 'valley'): 'vly', ('vlys', 'valleys'): 'vlys', ('via', 'viaduct', 'vdct', 'viadct'): 'via', ('view', 'vw'): 'vw', ('vws', 'views'): 'vws', ('villiage', 'villg', 'village', 'villag', 'vlg', 'vill'): 'vlg', ('villages', 'vlgs'): 'vlgs', ('ville', 'vl'): 'vl', ('vis', 'vsta', 'vista', 'vist', 'vst'): 'vis', ('walk',): 'walk', ('walks',): 'walk', ('wall',): 'wall', ('way', 'wy'): 'way', ('ways',): 'ways', ('well',): 'wl'}
dict_2 = {('header1',): 'header3', ('apartment',): 'apt', ('basement',): 'bsmt', ('building',): 'bldg', ('department',): 'dept', ('floor',): 'fl', ('front',): 'frnt', ('hanger',): 'hngr', ('key',): 'key', ('lobby',): 'lbby', ('lot',): 'lot', ('lower',): 'lowr', ('office',): 'ofc', ('penthouse',): 'ph', ('pier',): 'pier', ('rear',): 'rear', ('room',): 'rm', ('side',): 'side', ('slip',): 'slip', ('space',): 'spc', ('stop',): 'stop', ('suite',): 'ste', ('trailer',): 'trlr', ('unit',): 'unit'}
dict1_vals = {'vista', 'knolls', 'knoll','crossing', 'field', 'pr', 'ctrs', 'grns', 'brks', 'fry', 'clfs', 'exts', 'frd', 'hwy', 'pass', 'land', 'blvd', 'clf', 'vis', 'cv', 'shr', 'rte', 'trl', 'uns', 'row', 'expy', 'spg', 'spur', 'hl', 'cp', 'fall', 'jcts', 'pnes', 'frgs', 'blfs', 'gln', 'gtwy', 'xrd', 'cmn', 'mdws', 'wl', 'cres', 'ft', 'blf', 'trce', 'pike', 'crk','creek', 'ave', 'rue', 'jct', 'dl', 'cts', 'trlr', 'byp', 'sta', 'aly', 'gdns', 'rdg', 'nck', 'radl', 'skwy', 'rd', 'mnrs', 'trwy', 'ramp', 'mdw', 'mtn', 'oval', 'vlgs', 'kys', 'fwy', 'sqs', 'hts', 'lcks', 'lf', 'brk', 'vly', 'pts', 'lck', 'btm', 'ct', 'trak', 'knls', 'xing', 'path', 'smt', 'orch', 'vw', 'is', 'shls', 'glns', 'frg', 'rnch', 'br', 'mtwy', 'shrs', 'ter', 'tpke', 'flds', 'xrds', 'knl', 'gdn', 'dm', 'clb', 'upas', 'vlg', 'rpds', 'ctr', 'prts', 'lgt', 'frst', 'bgs', 'shl', 'dv', 'sts', 'bg', 'wall', 'cor', 'arc', 'cirs', 'curv', 'crst', 'inlt', 'crse', 'mall', 'hvn', 'pne', 'tunl', 'lndg', 'ldg', 'pln', 'vl', 'ests', 'grvs', 'hls', 'cswy', 'lk', 'trfy', 'anx', 'psge', 'stra', 'hbr', 'byu', 'mtns', 'fld', 'rdgs', 'bch', 'ml', 'est', 'mews', 'spgs', 'park', 'rds', 'pl', 'plns', 'flts', 'fls', 'riv', 'ln', 'lks', 'vlys', 'strm', 'rpd', 'cpe', 'cors', 'dr', 'hbrs', 'prt', 'cir', 'frks', 'flt', 'cyn', 'loop', 'isle', 'vws', 'via', 'brg', 'cmns', 'st', 'drs', 'pt', 'un', 'lgts', 'grn', 'sq', 'iss', 'walk', 'mt', 'msn', 'rst', 'pkwy', 'opas', 'frds', 'ky', 'ways', 'bnd', 'holw', 'ext', 'mnr', 'frk', 'run', 'grv', 'cvs', 'way', 'plz', 'mls'}
dict2_vals = {'ph', 'trlr', 'lbby', 'ste', 'spc', 'fl', 'lot', 'rear', 'header3', 'ofc', 'side', 'rm', 'slip', 'bsmt', 'apt', 'pier', 'unit', 'hngr', 'lowr', 'key', 'bldg', 'stop', 'frnt', 'dept'}
remove_re = r"\s(?:ste|lot|apt|unit|bldg|trlr|#)(?:[0-9#]+$|\s.*$|$)"
ave_reg = r"\s(ave)\s[a-z0-9]+$"
numbers = {'sixth ': '6th ', 'seventh ': '7th ', 'eighth ': '8th ', 'ninth ': '9th ', 'tenth ': '10th ', 'first ': '1st ', 'second ': '2nd ', 'third ': '3rd ', 'fourth ': '4th ', 'fifth': '5th ', r'^(one\s)|\sone\s|\sone$': '1 ', r'^(two\s)|\stwo\s|\stwo$': '2 ', r'^(three\s)|\sthree\s|\sthree$': '3 ', r'^(four\s)|\sfour\s|\sfour$': '4 ', r'^(five\s)|\sfive\s|\sfive$': '5 '}
directions = {'north': 'n', 'south': 's', 'east': 'e', 'west': 'w', 'northwest': 'nw', 'northeast': 'ne', 'southeast': 'se', 'southwest': 'sw'}
direction_abbrevs = {'n', 's', 'e', 'w', 'nw', 'ne', 'sw', 'se'}
keep = set(['StreetNamePreDirectional', 'AddressNumber', 'StreetName', 'StreetNamePostType'])


def map_cols(csv_data, target_headers=None, all_headers=False):

	year_set = set(['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008',\
	 '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'])
	first_names={'phillip', 'gilberto', 'jamel', 'vance', 'kendrick', 'raymond', 'alva', 'jonathon', 'bud', 'darren', 'mike', 'bernard', 'nathaniel', 'salvador', 'dustin', 'jeffery', 'toney', 'vaughn', 'maria', 'herbert', 'dino', 'rafael', 'renaldo', 'everette', 'terrance', 'joshua', 'dante', 'carter', 'jamaal', 'mitch', 'britt', 'elbert', 'rodolfo', 'freddy', 'julius', 'rolando', 'grady', 'valentine', 'bert', 'floyd', 'patricia', 'sanford', 'thad', 'deon', 'laverne', 'sonny', 'jonah', 'wally', 'jared', 'sherman', 'barney', 'kory', 'wayne', 'ruben', 'peter', 'teodoro', 'kieth', 'lanny', 'marion', 'newton', 'elias', 'haywood', 'august', 'mariano', 'gerry', 'rupert', 'sal', 'damion', 'hayden', 'fritz', 'monte', 'andres', 'daron', 'dennis', 'will', 'andre', 'rey', 'eduardo', 'jeramy', 'oscar', 'shelby', 'ulysses', 'erwin', 'scottie', 'walton', 'winfred', 'antony', 'blaine', 'stanton', 'freddie', 'enoch', 'houston', 'timmy', 'wesley', 'bryant', 'cortez', 'delmar', 'jerald', 'nicky', 'sydney', 'walter', 'zachariah', 'tad', 'arturo', 'shirley', 'dane', 'royal', 'howard', 'lyman', 'geraldo', 'monty', 'jc', 'lewis', 'vicente', 'keven', 'allen', 'hiram', 'bruno', 'donn', 'mitchell', 'cornelius', 'burt', 'abe', 'chuck', 'samuel', 'chadwick', 'jessie', 'darrell', 'carlton', 'cleveland', 'nigel', 'rich', 'don', 'buster', 'clement', 'franklyn', 'reinaldo', 'joe', 'wilmer', 'oliver', 'nickolas', 'ian', 'lauren', 'devin', 'mathew', 'roderick', 'cleo', 'fabian', 'richard', 'deshawn', 'darron', 'augustus', 'deandre', 'darell', 'kirby', 'lionel', 'dwayne', 'stephan', 'roman', 'romeo', 'valentin', 'jean', 'terrence', 'norbert', 'miquel', 'curtis', 'dick', 'junior', 'garland', 'franklin', 'noble', 'broderick', 'rodger', 'moses', 'kim', 'ike', 'bradley', 'antonia', 'wilson', 'elden', 'frank', 'lane', 'markus', 'morgan', 'weldon', 'carl', 'timothy', 'granville', 'emmanuel', 'kenny', 'otis', 'aron', 'federico', 'gustavo', 'irwin', 'elvin', 'jackie', 'irving', 'antone', 'emmitt', 'ricardo', 'troy', 'erin', 'loren', 'diego', 'rickie', 'amado', 'cecil', 'max', 'robt', 'brice', 'carroll', 'billy', 'marlin', 'quinn', 'calvin', 'johnny', 'forest', 'booker', 'tommy', 'edmundo', 'erich', 'dan', 'kenneth', 'john', 'wilfredo', 'nestor', 'zachary', 'mack', 'ali', 'carson', 'roscoe', 'asa', 'stacy', 'jon', 'foster', 'len', 'owen', 'whitney', 'dario', 'glen', 'maurice', 'tim', 'miles', 'paul', 'felix', 'edmund', 'isidro', 'boyce', 'claudio', 'avery', 'spencer', 'bernie', 'jeremy', 'jasper', 'kelley', 'isaac', 'jayson', 'eldridge', 'chauncey', 'joey', 'andreas', 'lou', 'loyd', 'wallace', 'jarod', 'norris', 'heath', 'elisha', 'neville', 'brady', 'kirk', 'zack', 'erasmo', 'emerson', 'reginald', 'ahmad', 'jim', 'parker', 'ellsworth', 'kurt', 'virgilio', 'ronny', 'mitchel', 'josiah', 'devon', 'agustin', 'maxwell', 'sidney', 'harris', 'denis', 'jeff', 'rosario', 'keneth', 'dalton', 'lester', 'carmine', 'trey', 'kraig', 'guillermo', 'lupe', 'pierre', 'brendon', 'korey', 'kurtis', 'ralph', 'rodrick', 'alex', 'rudy', 'darrel', 'sergio', 'angel', 'lenny', 'arnold', 'charles', 'jody', 'damon', 'winston', 'chase', 'omer', 'cordell', 'leigh', 'filiberto', 'sam', 'domenic', 'trent', 'bart', 'jamison', 'hong', 'edmond', 'jerrell', 'chung', 'preston', 'solomon', 'travis', 'jamey', 'ronald', 'leonard', 'mauricio', 'renato', 'waylon', 'adrian', 'douglas', 'rhett', 'dusty', 'lyndon', 'florencio', 'thomas', 'clair', 'doyle', 'kris', 'kristopher', 'darius', 'jed', 'donny', 'dexter', 'gabriel', 'micheal', 'scotty', 'abram', 'freeman', 'fernando', 'hilton', 'bryon', 'marcellus', 'sid', 'odell', 'octavio', 'darrin', 'jerold', 'neal', 'shaun', 'chi', 'adan', 'ned', 'nicholas', 'shon', 'dorsey', 'leo', 'jonas', 'douglass', 'ezequiel', 'jame', 'benedict', 'lucien', 'cesar', 'elwood', 'wes', 'mervin', 'johnathon', 'rudolf', 'kevin', 'boyd', 'derrick', 'jose', 'lamont', 'burton', 'jules', 'lindsay', 'noah', 'raphael', 'ronnie', 'emile', 'curt', 'frankie', 'michel', 'teddy', 'dong', 'shannon', 'titus', 'tyrell', 'sylvester', 'von', 'randolph', 'willie', 'james', 'daren', 'long', 'daryl', 'ted', 'francisco', 'eldon', 'sang', 'hunter', 'gerard', 'dwight', 'gail', 'isaiah', 'quintin', 'charlie', 'myron', 'rob', 'tuan', 'wilbert', 'kareem', 'phil', 'benny', 'steven', 'hai', 'bennett', 'tyson', 'carol', 'eddie', 'stevie', 'theodore', 'louis', 'milan', 'johnson', 'bennie', 'trinidad', 'frederic', 'vern', 'jermaine', 'earl', 'russ', 'hank', 'humberto', 'olin', 'rodrigo', 'leonardo', 'brant', 'philip', 'art', 'ellis', 'florentino', 'clifton', 'claude', 'columbus', 'marvin', 'leroy', 'jerrold', 'antione', 'kelly', 'gordon', 'roger', 'earle', 'keith', 'emery', 'luis', 'ismael', 'dean', 'jack', 'al', 'sean', 'alvaro', 'hoyt', 'mohamed', 'joseph', 'herschel', 'dwain', 'garret', 'jaime', 'clyde', 'ashley', 'malik', 'man', 'derek', 'graham', 'randell', 'reid', 'robby', 'albert', 'cedrick', 'luigi', 'arron', 'major', 'nelson', 'ramon', 'royce', 'chet', 'toby', 'wyatt', 'ahmed', 'issac', 'shawn', 'david', 'woodrow', 'donald', 'faustino', 'williams', 'jesse', 'rogelio', 'jamie', 'malcom', 'anton', 'sterling', 'leopoldo', 'maynard', 'anderson', 'gus', 'lenard', 'val', 'cody', 'hubert', 'rodney', 'daniel', 'buford', 'moshe', 'adalberto', 'aubrey', 'murray', 'merle', 'king', 'alexander', 'jacinto', 'tory', 'coleman', 'enrique', 'genaro', 'hipolito', 'aaron', 'jere', 'donte', 'charley', 'ethan', 'hyman', 'jerrod', 'napoleon', 'eugenio', 'desmond', 'thanh', 'del', 'terrell', 'mary', 'nicolas', 'marcel', 'lacy', 'waldo', 'clint', 'danial', 'jordan', 'berry', 'kristofer', 'harlan', 'manuel', 'harvey', 'saul', 'prince', 'erik', 'tracey', 'rayford', 'casey', 'damien', 'garrett', 'chance', 'edgar', 'melvin', 'henry', 'morton', 'archie', 'dominique', 'lemuel', 'geoffrey', 'jorge', 'micah', 'ron', 'willard', 'matt', 'emory', 'gerardo', 'cory', 'gregorio', 'jimmie', 'craig', 'virgil', 'jospeh', 'rosendo', 'johnie', 'reynaldo', 'caleb', 'leandro', 'ezekiel', 'jacques', 'christoper', 'edgardo', 'ira', 'alphonso', 'orville', 'gregory', 'blake', 'clifford', 'connie', 'nick', 'oswaldo', 'jan', 'dillon', 'gregg', 'dave', 'mario', 'sammie', 'mac', 'cyril', 'bob', 'tyree', 'benito', 'colby', 'lincoln', 'reyes', 'eliseo', 'numbers', 'ezra', 'orval', 'jarrett', 'son', 'simon', 'mohammed', 'jackson', 'dudley', 'lee', 'francis', 'irvin', 'lucio', 'tomas', 'warner', 'dominick', 'marshall', 'johnnie', 'thurman', 'danny', 'chester', 'adolfo', 'chris', 'fidel', 'harrison', 'alejandro', 'olen', 'ramiro', 'german', 'margarito', 'garth', 'marco', 'bryan', 'isaias', 'rick', 'harry', 'elijah', 'eloy', 'weston', 'cornell', 'ben', 'angelo', 'alfonzo', 'isreal', 'dale', 'lorenzo', 'abraham', 'damian', 'arlen', 'monroe', 'randal', 'leslie', 'guy', 'cristobal', 'leland', 'wilbur', 'joaquin', 'hobert', 'marlon', 'alvin', 'orlando', 'odis', 'raymon', 'linwood', 'bill', 'cedric', 'christopher', 'marty', 'morris', 'cary', 'kermit', 'carlo', 'reed', 'refugio', 'ward', 'vito', 'cole', 'aurelio', 'dannie', 'galen', 'gino', 'alonso', 'hal', 'bruce', 'marcelino', 'duane', 'myles', 'rod', 'adolph', 'rex', 'allan', 'armando', 'darwin', 'bertram', 'lavern', 'palmer', 'jesus', 'buck', 'darrick', 'elvis', 'josh', 'ollie', 'ricky', 'tracy', 'greg', 'wilburn', 'delmer', 'trevor', 'jamal', 'ken', 'jordon', 'edward', 'lesley', 'sandy', 'kerry', 'willis', 'vernon', 'rufus', 'scot', 'dewitt', 'lon', 'brock', 'jonathan', 'colton', 'giovanni', 'israel', 'carey', 'perry', 'raymundo', 'antonio', 'edison', 'pat', 'brett', 'luciano', 'neil', 'sammy', 'lawerence', 'ernesto', 'chong', 'rubin', 'dominic', 'leif', 'evan', 'santo', 'tom', 'yong', 'demetrius', 'burl', 'gerald', 'billie', 'shane', 'dylan', 'normand', 'antwan', 'lucius', 'colin', 'terence', 'andy', 'homer', 'norman', 'stacey', 'nathanial', 'dana', 'levi', 'cristopher', 'stuart', 'millard', 'ervin', 'lamar', 'norberto', 'vincent', 'ariel', 'boris', 'dirk', 'martin', 'mikel', 'blair', 'randall', 'miguel', 'michale', 'horace', 'shayne', 'eddy', 'tobias', 'marc', 'marcus', 'steve', 'wade', 'shelton', 'van', 'julian', 'anibal', 'warren', 'carmelo', 'bobbie', 'rocco', 'sebastian', 'william', 'collin', 'josue', 'rory', 'carlos', 'elliott', 'heriberto', 'jarvis', 'alton', 'logan', 'lynn', 'lucas', 'jacob', 'oren', 'rolland', 'ross', 'arnulfo', 'rolf', 'michael', 'byron', 'corey', 'lindsey', 'sung', 'forrest', 'wilber', 'joesph', 'hassan', 'chas', 'todd', 'fredrick', 'errol', 'kyle', 'porfirio', 'everett', 'milford', 'ignacio', 'dallas', 'lance', 'rudolph', 'ryan', 'tyron', 'delbert', 'francesco', 'frances', 'bo', 'brian', 'grover', 'mickey', 'reuben', 'ty', 'johnathan', 'beau', 'dorian', 'jason', 'bernardo', 'claud', 'hershel', 'eli', 'otto', 'huey', 'alexis', 'roland', 'gayle', 'gene', 'fredric', 'xavier', 'roy', 'gaylord', 'hugo', 'jefferson', 'robert', 'pedro', 'gil', 'harland', 'clayton', 'eric', 'armand', 'scott', 'tyler', 'leonel', 'dion', 'alonzo', 'austin', 'jimmy', 'fermin', 'luke', 'carmen', 'larry', 'jake', 'pablo', 'taylor', 'cletus', 'andrew', 'elmo', 'marquis', 'malcolm', 'adam', 'basil', 'darin', 'elroy', 'laurence', 'eugene', 'riley', 'seth', 'santiago', 'tod', 'robbie', 'denver', 'carrol', 'salvatore', 'zachery', 'wiley', 'alan', 'noe', 'bryce', 'karl', 'pasquale', 'patrick', 'raul', 'seymour', 'rusty', 'cliff', 'clinton', 'elton', 'joan', 'garfield', 'andrea', 'rene', 'courtney', 'quinton', 'wm', 'hung', 'giuseppe', 'leon', 'stefan', 'fletcher', 'lonnie', 'minh', 'santos', 'merlin', 'davis', 'emil', 'ivan', 'justin', 'herb', 'ferdinand', 'cruz', 'modesto', 'raleigh', 'merrill', 'landon', 'stanford', 'tanner', 'barton', 'isiah', 'jerry', 'lyle', 'mauro', 'vince', 'winford', 'abdul', 'alfredo', 'jeremiah', 'joel', 'sol', 'theron', 'efrain', 'tommie', 'russell', 'werner', 'lynwood', 'tony', 'kelvin', 'reggie', 'donnie', 'gilbert', 'mohammad', 'silas', 'stewart', 'brenton', 'victor', 'mose', 'rickey', 'rico', 'brent', 'edwin', 'michal', 'derick', 'louie', 'richie', 'quentin', 'chang', 'thaddeus', 'jerome', 'clemente', 'arthur', 'marcos', 'barrett', 'manual', 'kendall', 'benton', 'emmett', 'chad', 'gale', 'pete', 'felipe', 'roosevelt', 'noel', 'duncan', 'drew', 'stephen', 'garry', 'javier', 'maximo', 'gary', 'mel', 'trenton', 'domingo', 'willian', 'jude', 'young', 'jewel', 'ambrose', 'lawrence', 'otha', 'alec', 'roberto', 'kasey', 'amos', 'ernie', 'demarcus', 'edwardo', 'paris', 'moises', 'nathanael', 'randy', 'gaston', 'hector', 'mckinley', 'fred', 'emilio', 'omar', 'osvaldo', 'stan', 'dewey', 'jarrod', 'ed', 'zane', 'darnell', 'gonzalo', 'antoine', 'kip', 'tristan', 'bret', 'ernest', 'branden', 'abel', 'doug', 'rashad', 'juan', 'conrad', 'jeffry', 'fausto', 'bradford', 'graig', 'keenan', 'nolan', 'shad', 'denny', 'hilario', 'clarence', 'harold', 'jeffrey', 'jeromy', 'rigoberto', 'clark', 'terry', 'danilo', 'hosea', 'horacio', 'truman', 'jae', 'dee', 'julio', 'ray', 'wendell', 'marcelo', 'walker', 'bradly', 'lazaro', 'donovan', 'wilfred', 'felton', 'brendan', 'jamar', 'donnell', 'frederick', 'augustine', 'brad', 'efren', 'grant', 'kenton', 'alberto', 'eusebio', 'kennith', 'alphonse', 'coy', 'earnest', 'brooks', 'wilford', 'jewell', 'barry', 'alfred', 'hollis', 'hugh', 'josef', 'willy', 'sheldon', 'anthony', 'ivory', 'guadalupe', 'les', 'robin', 'herman', 'jess', 'bobby', 'alden', 'porter', 'rocky', 'deangelo', 'mason', 'erick', 'arden', 'buddy', 'lonny', 'clay', 'jay', 'arnoldo', 'elliot', 'gavin', 'vincenzo', 'esteban', 'christian', 'theo', 'benjamin', 'rueben', 'percy', 'quincy', 'arlie', 'brandon', 'judson', 'emanuel', 'hans', 'jefferey', 'dewayne', 'elmer', 'nathan', 'russel', 'cyrus', 'mark', 'matthew', 'zackary', 'brain', 'cameron', 'stanley', 'lloyd', 'alfonso', 'george', 'lowell', 'aldo', 'milton', 'harley', 'wilton', 'luther', 'milo', 'sherwood', 'darryl', 'jarred', 'samual', 'tyrone', 'lino', 'kent', 'glenn'}
	last_names={'page', 'vance', 'kennedy', 'henson', 'frazier', 'wolf', 'raymond', 'boyer', 'knox', 'bernard', 'rogers', 'villegas', 'dejesus', 'donaldson', 'berg', 'vaughn', 'portillo', 'dodson', 'richmond', 'rhodes', 'carter', 'french', 'diaz', 'spence', 'gonzales', 'conner', 'floyd', 'shields', 'nielsen', 'hardin', 'sanford', 'cook', 'hood', 'bravo', 'watkins', 'liu', 'graves', 'sherman', 'melton', 'shaw', 'petersen', 'mckinney', 'reese', 'mahoney', 'newton', 'white', 'hernandez', 'hayden', 'lawson', 'farrell', 'dennis', 'huber', 'garner', 'butler', 'camacho', 'walton', 'mcclure', 'lowery', 'evans', 'ortega', 'burke', 'meza', 'kerr', 'hebert', 'stanton', 'garrison', 'lam', 'shepard', 'moyer', 'leach', 'sampson', 'houston', 'dickerson', 'cantrell', 'rocha', 'valdez', 'bryant', 'cortez', 'bernal', 'mayer', 'walter', 'norton', 'dyer', 'sharp', 'howard', 'watts', 'lewis', 'west', 'robinson', 'allen', 'wilkerson', 'mccarthy', 'mclaughlin', 'mitchell', 'mcguire', 'barajas', 'crane', 'welch', 'escobar', 'pittman', 'allison', 'hinton', 'rich', 'pollard', 'shaffer', 'malone', 'abbott', 'savage', 'weaver', 'oliver', 'sandoval', 'hickman', 'wise', 'macias', 'medrano', 'wiggins', 'richard', 'jennings', 'rubio', 'delarosa', 'kirby', 'barker', 'clements', 'weber', 'nunez', 'foley', 'roman', 'faulkner', 'church', 'krueger', 'simpson', 'blevins', 'olson', 'fowler', 'salinas', 'hart', 'matthews', 'curtis', 'thompson', 'rodgers', 'cardenas', 'noble', 'franklin', 'blackburn', 'proctor', 'daniels', 'avalos', 'tate', 'ortiz', 'livingston', 'moses', 'kim', 'howell', 'kramer', 'wilson', 'bradley', 'buckley', 'frank', 'lane', 'enriquez', 'morgan', 'rice', 'keller', 'villalobos', 'truong', 'glass', 'burch', 'gill', 'hudson', 'mosley', 'fernandez', 'bowman', 'knight', 'rivera', 'harrington', 'gardner', 'banks', 'guzman', 'ayers', 'carroll', 'quinn', 'landry', 'zhang', 'holmes', 'higgins', 'booker', 'mckee', 'knapp', 'mack', 'ali', 'carson', 'ramos', 'garcia', 'mills', 'foster', 'owen', 'moran', 'whitney', 'hampton', 'moore', 'hunt', 'spencer', 'miles', 'paul', 'lozano', 'flores', 'pineda', 'hogan', 'bartlett', 'felix', 'fuller', 'avery', 'vu', 'gross', 'ramirez', 'melendez', 'lugo', 'mcpherson', 'kelley', 'stafford', 'combs', 'wallace', 'norris', 'branch', 'zimmerman', 'heath', 'armstrong', 'ball', 'brady', 'underwood', 'kirk', 'lowe', 'stark', 'williamson', 'parker', 'vazquez', 'franco', 'strickland', 'pratt', 'nicholson', 'fitzpatrick', 'ventura', 'hoffman', 'maxwell', 'harris', 'boone', 'bates', 'rosario', 'woodard', 'barrera', 'swanson', 'avila', 'dalton', 'stein', 'lester', 'salazar', 'jaramillo', 'pearson', 'small', 'murphy', 'wagner', 'haynes', 'cochran', 'chen', 'curry', 'mckenzie', 'richards', 'singh', 'munoz', 'obrien', 'rangel', 'bass', 'gibbs', 'arnold', 'cherry', 'charles', 'chase', 'rush', 'fitzgerald', 'choi', 'preston', 'solomon', 'winters', 'parrish', 'dunlap', 'chung', 'travis', 'jacobs', 'cunningham', 'vaughan', 'grimes', 'velez', 'sellers', 'leonard', 'duarte', 'roberts', 'sheppard', 'pham', 'hoover', 'barr', 'douglas', 'stevens', 'schmitt', 'oneill', 'pitts', 'thomas', 'doyle', 'duffy', 'hill', 'schultz', 'mccormick', 'booth', 'hodges', 'pennington', 'montgomery', 'hale', 'galvan', 'freeman', 'zavala', 'cline', 'serrano', 'mcintyre', 'sutton', 'bowen', 'robbins', 'corona', 'strong', 'villa', 'neal', 'sierra', 'york', 'griffin', 'bautista', 'dorsey', 'sexton', 'atkinson', 'wells', 'gaines', 'meyer', 'burgess', 'wall', 'castaneda', 'esparza', 'tucker', 'parsons', 'boyd', 'person', 'stevenson', 'burton', 'perez', 'hartman', 'payne', 'rosales', 'gibson', 'goodwin', 'yoder', 'wong', 'hughes', 'vasquez', 'james', 'randolph', 'long', 'carpenter', 'caldwell', 'soto', 'mendez', 'hunter', 'peralta', 'park', 'oneal', 'parra', 'carlson', 'mcintosh', 'solis', 'spears', 'bennett', 'navarro', 'mendoza', 'johnson', 'mata', 'quintana', 'gutierrez', 'johns', 'webb', 'tran', 'ellis', 'fry', 'schwartz', 'duran', 'deleon', 'kelly', 'gordon', 'juarez', 'bell', 'stone', 'keith', 'stephens', 'rios', 'dean', 'alfaro', 'middleton', 'yang', 'kaur', 'joseph', 'harrell', 'galindo', 'ashley', 'graham', 'reid', 'estes', 'mccullough', 'nelson', 'pugh', 'golden', 'poole', 'wyatt', 'ahmed', 'david', 'walters', 'dougherty', 'haley', 'arroyo', 'williams', 'cox', 'salgado', 'huang', 'marks', 'valenzuela', 'lu', 'ballard', 'bowers', 'schneider', 'murillo', 'mora', 'magana', 'friedman', 'anderson', 'maynard', 'li', 'estrada', 'nava', 'trevino', 'sanchez', 'hamilton', 'daniel', 'briggs', 'contreras', 'murray', 'nguyen', 'davidson', 'humphrey', 'king', 'alexander', 'coleman', 'burnett', 'padilla', 'torres', 'dawson', 'boyle', 'griffith', 'parks', 'hanna', 'larson', 'hall', 'trujillo', 'mcfarland', 'terrell', 'love', 'kemp', 'rasmussen', 'dunn', 'jordan', 'xiong', 'berry', 'snow', 'walls', 'pace', 'harvey', 'ellison', 'prince', 'clarke', 'ruiz', 'lin', 'wolfe', 'morales', 'casey', 'garrett', 'giles', 'waters', 'yu', 'hester', 'romero', 'morton', 'henry', 'zamora', 'barnes', 'klein', 'adams', 'baker', 'beltran', 'yates', 'lucero', 'lara', 'cortes', 'callahan', 'calderon', 'kline', 'larsen', 'delacruz', 'benitez', 'eaton', 'craig', 'robles', 'costa', 'ibarra', 'orozco', 'farmer', 'ingram', 'crosby', 'herring', 'gregory', 'blake', 'chambers', 'vang', 'leal', 'garza', 'kane', 'robertson', 'bullock', 'dillon', 'bender', 'medina', 'peters', 'villanueva', 'adkins', 'frye', 'baldwin', 'huynh', 'lyons', 'day', 'collins', 'bailey', 'johnston', 'mann', 'hobbs', 'goodman', 'reyes', 'olsen', 'simon', 'myers', 'jackson', 'steele', 'cuevas', 'lee', 'francis', 'warner', 'ho', 'dudley', 'marshall', 'nash', 'whitehead', 'harrison', 'castillo', 'moss', 'bryan', 'arellano', 'finley', 'sparks', 'velazquez', 'browning', 'wood', 'acevedo', 'leblanc', 'cantu', 'reilly', 'campbell', 'miranda', 'hubbard', 'decker', 'jimenez', 'miller', 'huff', 'cobb', 'horne', 'glover', 'monroe', 'moon', 'mclean', 'house', 'mcdonald', 'stokes', 'mathis', 'becker', 'reyna', 'holt', 'rivers', 'wu', 'conway', 'morris', 'howe', 'reed', 'mcdaniel', 'roach', 'fuentes', 'marsh', 'ward', 'patterson', 'carrillo', 'farley', 'cole', 'shannon', 'bruce', 'vega', 'mercado', 'wilkins', 'hancock', 'newman', 'hines', 'palmer', 'russo', 'gomez', 'fischer', 'rowe', 'black', 'buck', 'maddox', 'webster', 'horn', 'willis', 'mueller', 'patel', 'holland', 'stout', 'little', 'montoya', 'hansen', 'brock', 'hurst', 'hendricks', 'alvarez', 'maldonado', 'perry', 'carey', 'beasley', 'collier', 'guerra', 'santana', 'quintero', 'harper', 'gray', 'bishop', 'beard', 'schroeder', 'vo', 'coffey', 'edwards', 'mejia', 'palacios', 'luna', 'morse', 'fleming', 'watson', 'richardson', 'hurley', 'mckay', 'good', 'wright', 'jensen', 'norman', 'manning', 'valentine', 'vincent', 'singleton', 'stuart', 'may', 'gonzalez', 'silva', 'christensen', 'bradshaw', 'lopez', 'copeland', 'reynolds', 'hopkins', 'bauer', 'martin', 'levy', 'novak', 'ponce', 'blair', 'gillespie', 'ramsey', 'randall', 'weeks', 'rivas', 'wade', 'shelton', 'cordova', 'warren', 'lang', 'cannon', 'mccarty', 'aguilar', 'owens', 'cross', 'elliott', 'bean', 'jarvis', 'ross', 'logan', 'skinner', 'lucas', 'rosas', 'davila', 'moody', 'espinosa', 'lynn', 'gates', 'atkins', 'fox', 'michael', 'stephenson', 'lindsey', 'weiss', 'holloway', 'phan', 'hardy', 'martinez', 'dominguez', 'todd', 'cummings', 'sawyer', 'everett', 'hayes', 'hicks', 'wilkinson', 'ryan', 'mccann', 'cooper', 'schaefer', 'daugherty', 'sims', 'peterson', 'ochoa', 'beil', 'rose', 'roberson', 'whitaker', 'moreno', 'mullen', 'mcdowell', 'berger', 'brewer', 'bush', 'meyers', 'nixon', 'roy', 'lambert', 'durham', 'jefferson', 'blanchard', 'blankenship', 'mcmahon', 'macdonald', 'hendrix', 'barnett', 'snyder', 'espinoza', 'sullivan', 'gentry', 'clayton', 'ware', 'scott', 'aguirre', 'byrd', 'tyler', 'pope', 'bond', 'le', 'austin', 'acosta', 'taylor', 'crawford', 'summers', 'sloan', 'herrera', 'velasquez', 'powell', 'pierce', 'sanders', 'green', 'frost', 'odom', 'cervantes', 'shepherd', 'sosa', 'odonnell', 'schmidt', 'riley', 'santiago', 'andersen', 'hutchinson', 'wiley', 'tang', 'potter', 'salas', 'patrick', 'carr', 'khan', 'bonilla', 'blackwell', 'chapman', 'jenkins', 'davenport', 'mays', 'jones', 'drake', 'sweeney', 'mccoy', 'tapia', 'huffman', 'powers', 'marin', 'morrison', 'hammond', 'leon', 'mcbride', 'fletcher', 'short', 'santos', 'woods', 'davis', 'trejo', 'ford', 'cruz', 'hawkins', 'reeves', 'barber', 'townsend', 'hess', 'tanner', 'andrews', 'barton', 'koch', 'lamb', 'figueroa', 'cabrera', 'russell', 'woodward', 'patton', 'molina', 'brown', 'stewart', 'price', 'gilbert', 'merritt', 'jacobson', 'montes', 'greene', 'barron', 'gilmore', 'harding', 'chang', 'buchanan', 'thornton', 'barrett', 'shah', 'best', 'benton', 'gallagher', 'marquez', 'lim', 'burns', 'duncan', 'oconnell', 'dickson', 'duke', 'pruitt', 'andrade', 'osborne', 'cisneros', 'oconnor', 'lynch', 'young', 'beck', 'turner', 'lawrence', 'benson', 'colon', 'morrow', 'mayo', 'suarez', 'mathews', 'villarreal', 'brennan', 'washington', 'hanson', 'cain', 'ayala', 'mullins', 'peck', 'hensley', 'chan', 'guevara', 'wang', 'flynn', 'campos', 'esquivel', 'baxter', 'conrad', 'chandler', 'mccall', 'bradford', 'nolan', 'madden', 'waller', 'conley', 'gallegos', 'clark', 'terry', 'bentley', 'saunders', 'mcclain', 'hull', 'pacheco', 'mcgee', 'meadows', 'hail', 'ray', 'cohen', 'huerta', 'walker', 'english', 'pena', 'correa', 'donovan', 'frederick', 'dixon', 'smith', 'walsh', 'rowland', 'nichols', 'valencia', 'grant', 'alvarado', 'brandt', 'cano', 'brooks', 'barry', 'rojas', 'hodge', 'rollins', 'ferguson', 'horton', 'anthony', 'arias', 'compton', 'zuniga', 'porter', 'perkins', 'herman', 'henderson', 'wheeler', 'mason', 'flowers', 'fields', 'clay', 'christian', 'benjamin', 'case', 'guerrero', 'wilcox', 'fisher', 'potts', 'simmons', 'roth', 'hahn', 'harmon', 'castro', 'cameron', 'phelps', 'stanley', 'mcmillan', 'lloyd', 'george', 'calhoun', 'mcconnell', 'greer', 'phillips', 'rodriguez', 'orr', 'gould', 'bridges', 'chavez', 'delgado', 'vargas', 'massey', 'kent', 'erickson', 'glenn'}
	auto_makes={'isuzu', 'acura', 'audi', 'am general', 'dodge', 'land rover', 'cadillac', 'aston martin', 'saturn', 'suzuki', 'nissan', 'porsche', 'subaru', 'kia', 'saab', 'fiat', 'chrysler', 'gmc', 'bmw', 'buick', 'plymouth', 'mini', 'scion', 'volkswagen', 'ram', 'lincoln', 'merkur', 'geo', 'toyota', 'mazda', 'eagle', 'volvo', 'datsun', 'daewoo', 'bentley', 'mercury', 'infiniti', 'jaguar', 'hummer', 'jeep', 'mercedes-benz', 'hyundai', 'lexus', 'pontiac', 'mitsubishi', 'auto make', 'chevrolet', 'oldsmobile', 'ford', 'ferrari', 'tesla', 'honda'}
	auto_models={'dynasty', 'z8', 'mustang svt cobra', 'is 250', '850', 'fifth avenue', 'discovery', 'silverado 1500', 'amanti', 'commander', 'nova', 'passport', 'trailblazer ext', 'taurus x', 'scorpio', 'taurus', 'tucson', 'express passenger', 'm-class', 'm30', 'express', 'mkt', 'probe', 'durango', 'prius plug-in hybrid', 'silverado 3500hd cc', 'a8 l', 'cx-9', 'r8', 'aztek', 'charger', 'caprice', 'cobalt', 'h1', 'sonata', 'avalanche', 'capri', 'xc60', 'gl-class', 'fusion energi', 'ascender', 'x3', 'hhr', 'sonoma', 'toronado', 'cube', 'legend', 'aries america', 'patriot', 'e-series cargo', 'storm', '6 series', 'santa fe sport', 'range rover evoque', 'ls 430', 'element', 'omega', 'cutlass supreme', 'colorado', 'quest', 'sierra 2500hd classic', 'rx-8', 'continental gtc v8', 'borrego', 'daytona', 'stratus', 'ram 150', 'aries k', 'black diamond avalanche', 'aerio', 'rondo', 'clk', 'villager', 'x5 m', 'tl', 'panamera', 'qx80', 's-10', 'g8', 'gti', 'impreza', 'lr4', 'volt', 'optima hybrid', '940', 'escalade esv', 'cruze', 'q7', 'elantra gt', 'tahoe', 'g5', 'maxima', 'mountaineer', 'qx4', 'le mans', 'silverado 2500hd', 'tribute', 'forester', 'mkz', 'roadmaster', 'aerostar', 'prius v', 'c4500 pickup', 'mpv', 'blazer', 'pilot', 's5', 'ilx', 'm56', 'sidekick', 'accent', 'spectra', 'excel', 'forenza', 'silverado 2500', 'sundance', 'eurovan', 'mazdaspeed3', 'loyale', '350z', 'outlander', 'trans sport', 'c/k 1500 series', 's80', 'sunfire', 'tempo', 'gs 300', 'tsx', 'vue', 'relay', 'is 350', 'verano', 'integra', 'cayenne', 'neon srt-4', 'silverado', 'ct 200h', 'mdx', 'traverse', 'grand vitara', 'genesis coupe', 'envoy xl', 'cooper coupe', 'e-250', 'r32', 'alero', 'lumina', 'santa fe', 'crossfire', 'sequoia', 'x6', '5 series', 'wrangler unlimited', 'ridgeline', 's-series', 'tercel', 'suburban', 'e-series chassis', 'cayman', 'mr2 spyder', 'rav4', 'savana cargo', 'sorento', '560-class', 'm37', 'aviator', 'rx 300', 'golf r', 'sentra', 'tundra', 'm5', 'entourage', 'q40', 'soul', 'vitara', 'outlander sport', 'f-250 super duty', 'gt-r', 'elantra', 'g20', 'boxster', 'rx 400h', 'a5', 'astra', 'fx45', 'h3t', 'altima hybrid', 'freelander', 'corsica', 'cts-v', 'amigo', 'crown victoria', 'm45', 'rainier', 'riviera', 'escalade hybrid', 'expedition', 'accord', 'metro', 'cutlass calais', 'camry solara', 'es 350', 'malibu hybrid', 'hardtop', 'endeavor', 'a8', 'mini ram van', 'impala', 'f-350 super duty', 'ls', 'tt', 'b-series truck', 'xj-series', 'magnum', 'pacifica', 'c/k 10 series', 'cls', 'cooper roadster', 'f-450 super duty', 'eldorado', 'ramcharger', 'sierra 1500 classic', 'is f', 'new beetle', 'trooper', 'r-class', 'raider', 'accord crosstour', 'hardbody', 'i35', 'sierra 3500hd cc', '4 series', 'stanza', 'uplander', 'camry hybrid', 'cts', 'fleetwood', 'aveo', 'nitro', 'z3', 'slk', 'brougham', '380-class', '8 series', 'malibu limited', 'sierra', '3 series', 'chevy van', 'mini e', '600', 'lss', 'monte carlo', 'samurai', 'versa', 'c-max hybrid', 'veracruz', 'cl-class', 'mariner', 'f-350', 's60', 'tracker', '370z', 'ats', 'challenger', 'sl-class', 'beetle', 'prizm', 'ram wagon', 'venture', 'xb', 'eighty-eight royale', '9-7x', 'z4', 'a7', 'altima', 'xf', 'celebrity', 'land cruiser', 'b-series pickup', 'sierra 1500hd', 's-15 jimmy', 'equus', 'hs 250h', 'eclipse spyder', 'grand am', '300m', 'celica', 'x5', 'enclave', 'f-150', 'srx', 'c/k', 'is 350c', 'navigator', 'xjl', 'milan', 'civic crx', 'db9', 'oasis', 'protege5', 'acclaim', 'cx-7', 'town car', 'camaro', 'mkx', '200 convertible', 'wrx', 'roadster', 'm', 'escort', 'shelby gt500', 'xlr', 'ram pickup 3500', 'rx 350', 'pickup', 'tiburon', 'murano', 'sierra 3500', 'v70', 'tracer', 'fiesta', 'diamante', 'prowler', '7 series', '300-class', 'c/k 20 series', 'milan hybrid', 'trailblazer', 'mks', 'journey', 'protege', 'ram cargo', 's7', 'sonic', 'xc', 'c-max energi', 'g35', 'savana passenger', '4runner', 'focus', 'ram pickup 2500', 'rl', 'sc 400', 'breeze', 'xk', 'edge', 'is 250c', 'c/k 2500 series', 's2000', 'h3', 'lhs', 'freestar', 'ram 50 pickup', '500', 's6', 'ssr', 'sx4 crossover', 'astro cargo', 'regal', 'mx-5 miata', 'q45', 'park avenue', 'sierra 2500', 'rx 330', 'qx56', 'touareg', 'avenger', 'ram pickup 1500', 'rio5', 'terrain', 'cruze limited', 'gle', 'lancer', 'acadia', 'g37 convertible', 'cl', 'marauder', 'tsx sport wagon', 'malibu', 'ram 100', 'caballero', '360 spider', 'xg350', 'silverado 1500 ss', 'montero sport', 'silverado 2500hd classic', '240sx', 'forte', 'galant', 'colt', 'envoy xuv', 'genesis', 'm6', 'shadow', 'intrigue', 'grand marquis', 'lumina minivan', 'lesabre', 's-10 blazer', 'five hundred', 'prius c', 'imperial', 'malibu classic', 'allante', '6000', 'flex', 'jetta', 'xd', 'rodeo', 'g37', 'sierra 2500hd', '760', 'solstice', 'gs 430', 'rogue select', 'safari', 'seville', 'golf', 'matrix', 'dts', 'hummer', '5000', 'e-series wagon', 'sprinter', 'xa', 'g6', 'dbs', 'e-350', 'routan', 'grand cherokee', 'v8 vantage', 'a3', 'insight', 'contour', '9-2x', 'silverado 3500 classic', 'thunderbird', 'rlx', 'yukon', 'savana', 'escape hybrid', 'zdx', 'continental', 'delta eighty-eight royale', 'mazda2', 'gx 460', 'tc', 'ls 460', 'cressida', 'windstar cargo', 'verona', 'previa', 'xk-series', 'super duty', 'mirage', 'es 300', 'impala limited', 'venza', 'spirit', 'gs 400', 'new yorker', 'glk', 'legacy', 'cc', 'sonata hybrid', 'qx60', '911', 'x1', 'eos', '190-class', 'compass', 'es 300h', 'dart', 'silverado 1500hd', 'a6', 'sx4', 'omni', 'laser', 'navigator l', 'beretta', '240', 'countryman', 'rs 7', 'elantra coupe', 'eclipse', 'sephia', 'ion red line', 'armada', 'sierra 3500 classic', 'fairmont', 'explorer sport', 'forte koup', 'xj', 'murano crosscabriolet', 'cutlass ciera', 'sierra c3', 'allroad quattro', 'tacoma', 'ram', 'cadenza', 'sls amg', 'tlx', 'x-type', 'cabrio', 'eighty-eight', 'sky', 'town and country', 'cooper hardtop', 'catera', 'truck', 'axiom', 'discovery series ii', 'fx35', 'sc 430', 'c-class', 'sportvan', 'grand voyager', 'crosstour', 'vision', 'liberty', 'es 330', 'van', 'civic del sol', 'a4', 'fusion', 'lx 470', 'ciera', 'silverado 1500 hybrid', 'xc90', 'xg300', 'ram pickup 1500 srt-10', 'c/k 3500 series', 'q50 hybrid', '740', 'mkz hybrid', 'esteem', 'xjr', 'vibe', 'silverado 1500 classic', 'cabriolet', 'reliant k', 'gto', 'juke', '260-class', 'cooper', 'lancer evolution', 'tiguan', 'concorde', 'fx37', 'sebring', 'xkr', 'ltd crown victoria', 'pathfinder', 'supra', 'aura', 'gli', 'l-series', 'expedition el', 'cr-v', 'highlander', 'range rover', 's-class', 'mark lt', 'ram van', 'sunbird', 'corolla', 'echo', 'bronco', 'sienna', 'e-class', 'astro van', '300', 'tribeca', 'passat', 'fusion hybrid', 'spark', 'xl7', 'c30', 'gs 350', 'jimmy', 'envoy', 'cx-5', 'rabbit', 'c3500 pickup', 'marquis', '200', 'sc 300', 'le baron', 'classic', 'mark vii', 'city express cargo', 'sable', 'cavalier', 'intrepid', 'explorer', '400-class', 'explorer sport trac', 'rio', 'mazdaspeed protege', 'e-150', '626', '1 series', 'lanos', 'elantra touring', 'fit', 'lancer sportback', 'talon', 'grand prix', 'h2', 'jx35', 'millenia', 'xl-7', 'lacrosse', 'sierra 1500', 'nv passenger', 'terraza', 'veloster turbo', 'sts-v', 'avalon', 'excursion', 'bravada', 'gx 470', 'encore', 'xts', 'avalon hybrid', 'freestyle', 'canyon', '200sx', 'rdx', 'is 300', 'outback', 'f250', 'forte5', 'deville', 'voyager', 'viper', 'yukon xl', 'ex35', 'dakota', 'yaris', 'touareg 2', 'veloster', 'v40', 'ranger', 'stealth', 'wrangler', 'trooper ii', 'slx', 'montana', 'g-class', 'c70', 'torrent', 'express cargo', 'fj cruiser', 'qx70', 'outlook', 'silverado 3500', 's70', 'prius', 's-type', 'g3', 'rsx', 'versa note', 'gls', 'cooper countryman', '420-class', 'cherokee', 'xterra', 'bonneville', 'm35', 'cougar', 'leaf', 's40', 'sts', 'q70', 'v50', 'escape', 'cirrus', 'odyssey', 'civic', 'highlander hybrid', 'q5', 'mustang', 'sierra 3500hd', 'commercial vans', 'q50', 'sedona', 'escalade', 'firebird', 'h2 sut', 'range rover evoque coupe', 'vehicross', 'ls 400', 'grand caravan', 'g37 coupe', 'xv crosstrek', 'brz', 'silhouette', 'rx 450h', 'cla', 'm3', 'equinox', 'starion', 'range rover sport', 'aspen', 'nv cargo', 'silverado 3500hd', 'econoline', 'sportage', 'optima', 'escalade ext', 'montego', 'mark viii', 'century', 'cooper clubman', 'corvette', 'rogue', 'neon', 'astro', 'camry', 'mazda6', 'mazda5', 'reno', 'lx 570', 'pt cruiser', 's4', 'premier', 'xc70', 'frontier', 'titan', 'l300', 'rendezvous', 'caliber', 'transit connect', 'impulse', 'mx-6', 'montero', 'tahoe limited/z71', 'prelude', 'skylark', 'focus svt', 'ion', 'lucerne', 'rodeo sport', 'convertible', 'cooper convertible', 'nubira', '900', 'aurora', 'windstar', 'i30', 'g37 sedan', 'malibu maxx', 'mazda3', 'caravan', 'azera', 'g25 sedan'}
	states={'nh', 'tn', 'wi', 'nc', 'nv', 'il', 'wv', 'de', 'co', 'ky', 'ca', 'az', 'mi', 'ct', 'wy', 'ia', 'id', 'ma', 'mn', 'nm', 'md', 'fl', 'ny', 'nd', 'va', 'ak', 'ok', 'sc', 'pa', 'or', 'al', 'oh', 'vt', 'sd', 'ks', 'hi', 'tx', 'in', 'ut', 'wa', 'mo', 'ga', 'ri', 'ne', 'la', 'nj', 'ms', 'ar', 'me', 'mt'}
	types={'new','used','n','u'}
	headers = [header.strip().lower() for header in csv_data[0]]

	if all_headers:

		headers[:7] = ['first','last','address','city','state','zip','email']
		inds=list(range(len(headers)))
		return [inds, {i:headers[i] for i in inds}, headers]

	data=csv_data[1:]
	headers_inds = [i for i in range(len(headers))]
	data_dict=dict()
	local_mapper=dict()
	imported_headers=set()
	map_dict_hdr = {header: i for i, header in enumerate(headers)}
	map_dict_idx = {i: header for i, header in enumerate(headers)}

	for line in data:
		for col_ind in headers_inds:
			data_set = data_dict.get(col_ind, set())
			entry = line[col_ind].strip()
			if len(entry) < 1:
				continue
			data_set.add(entry.lower())
			data_dict[col_ind]=data_set

	for entry in target_headers:
		for key in map_dict_hdr:
			if entry in key:
				imported_headers.add(key)
				local_mapper[map_dict_hdr[key]]=entry
				break

	if len(local_mapper) == len(headers) and len(headers) == len(target_headers):

		reverse_mapper = {value:key for key,value in local_mapper.items()}
		mapper_inds = [reverse_mapper[header] for header in target_headers]
		return [mapper_inds, local_mapper, target_headers]

	else:
		unknown_headers_inds = [i[0] for i in enumerate(headers) if i[1] not in imported_headers]
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
						continue
					if '@' in entry:
						email_count+=1
						continue
					if entry.isdigit():
						if entry in year_set or len(entry) <= 3:
							year_count+=1
						elif i <= 7:
							zip_count+=1
						elif len(entry) <= 6:
							cost_count+=1
						continue
					try:
						flt_test = float(entry)
						cost_count+=1
						continue
					except:
						pass
					if '/' in entry or '-' in entry:
						date_count+=1
						continue
					if add_check.isalnum():
						address_count+=1
					

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
				print('column skipped: {}'.format(map_dict_idx[i]))
				continue

		fetched_cols=set()
		skip_cols=set(local_mapper.values())

		for entry in unknown_dict:

			value=unknown_dict[entry]
			if len(value) < 1:
				continue
			analyze_lst=sorted([(count, header) for count, header in value.items()], reverse=True)
			detected_column=analyze_lst[0][1]
			if detected_column in skip_cols:
				continue
			else:
				local_mapper[entry] = detected_column
		missing_headers = (set(target_headers).difference(set(local_mapper.values())))
		for i, header in enumerate(missing_headers):
			local_mapper['missing_{}'.format(i)]=header
	if len(missing_headers) > 0:
		print('\nNo column found for {}'.format(', '.join(missing_headers)))
		choice=input('\nContinue? y/n ')
		if choice == 'n':
			sys.exit()

	reverse_mapper = {value:key for key,value in local_mapper.items()}
	mapper_inds = [reverse_mapper[header] for header in target_headers]
	#print(reverse_mapper, mapper_inds)
	#print(local_mapper,reverse_mapper,mapper_inds)
	#sys.exit()
	return [mapper_inds, local_mapper, target_headers]


def convert(orig_ad, ret_tup = False):
	
	orig_ad = re.sub(remove_re, "", orig_ad, flags = re.IGNORECASE)
	orig_ad = orig_ad.replace(" - ","-").strip()
	address = re.sub(r"[^a-zA-Z0-9\s#-']", "", orig_ad.lower())
	if 'ave' in address:
		try:
			address = address.replace(re.search(ave_reg, address).group(1), 'avenue')
		except:
			pass
	
	for number in numbers:
		address = re.sub(number, numbers[number], address)
	
	try:
		parsed = usaddress.tag(address)
		dic = parsed[0]
		flag1 = False
		flag2 = False
		if 'StreetNamePostType' in dic:
			snp = dic['StreetNamePostType']
			
			if snp not in dict1_vals:
				for item in dict_1:
					if snp in item:
						snp_append = dict_1[item]
						flag1 = True
			if not flag1:
				snp_append = snp
		
			dic['StreetNamePostType'] = snp_append
		if 'StreetNamePreDirectional' in dic:
			try:
				key = dic['StreetNamePreDirectional']
				dic['StreetNamePreDirectional'] = directions[key]
			except:
				x = 1
		stand_address = " ".join([dic[item] for item in dic])
	except:
		stand_address = orig_ad.replace(","," ")
	return stand_address

sup = False
sup_ = False
num_reg_1 = r"^\S+\s"
my_reg_2 = r"\s+jr$|\s+sr$|\s+[Ii]{1,}$|\s+jr\s+|\s+sr\s+|\s+[Ii]{1,}\s+"
num_reg_4 = r"^\D*([0-9]+)\D"
num_reg_3 = r"^[nsewu]{1,2}\s+|\s+[nsewu]{1,2}\s+|north\s+|south\s+|east\s+|west\s+"
apt_reg = r"\s([\d]+)\D{,1}$"
cr_reg = r'^cr |^county rd ' 
direction_abbrevs = {'n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw'}


def match(orig, comp, match_val_ = 1, thresh = 0.8, ret_matcher = False, e = False, name = False, address = False, sup = False, exact = False):
	
	if not name and (len(orig) < 2 or len(comp) < 2):
		return False
	orig = orig.strip().lower()
	comp = comp.strip().lower()
	
	if not sup and (orig.startswith("box") or comp.startswith("box")):
		return False
		
	if not ret_matcher:
		if address:
			if orig == comp:
				return True
			try:
				orig1 = orig.split(" ")
				comp1 = comp.split(" ")
				if orig1[0] in direction_abbrevs and comp1[0] not in direction_abbrevs:
					orig1 = orig1[1:]
					orig = " ".join(orig1)
				elif comp1[0] in direction_abbrevs and orig1[0] not in direction_abbrevs:
					comp1 = comp1[1:]
					comp = " ".join(comp1)
				if orig == comp:
					return True
				lenorig1 = len(orig1)
				lencomp1 = len(comp1)
				if (lenorig1 - lencomp1 == 1 and orig1[-1] in dict1_vals and orig1[:-1] == comp1) or (lencomp1 - lenorig1 == 1 and comp1[-1] in dict1_vals and comp1[:-1] == orig1):
					return True
			except:
				x = 1

			if match_val_ == 1:
				return False
				
			if sup or len(sales_to_process) < 120:
				check_len = 2
			else:
				check_len = 4
			orig = re.sub(cr_reg, "county road", orig)
			comp = re.sub(cr_reg, "county road", comp)
			if (len(comp) <=4 or len(orig) <= 4) and comp[:1] == orig[:1]:
				return True
			else:
				orig_ = orig
				comp_ = comp
				if len(orig.split(" ")[-1]) < 3:
					orig_ = orig[:orig.rfind(" ")]
				if len(comp.split(" ")[-1]) < 3:
					comp_ = comp[:comp.rfind(" ")]
				orig_ = orig_.replace(" ","")
				comp_ = comp_.replace(" ","")
				if orig_[:check_len] == comp_[:check_len]:
					return True
			
			if sup or len(sales_to_process) < 60:
				if orig_[(-1 * check_len):] == comp_[(-1 * check_len):]:
					return True
				try:
					orig_ = int(orig_[0])
					comp_ = int(comp_[0])
					if orig_ == comp_:
						return True
				except: 
					x = 1
			try:
				orig_ = int("".join(orig_[:2]))
				comp_ = int("".join(comp_[:2]))
				if orig_ == comp_:
					return True
			except: 
				x = 1
			return False
	
		if name:
			if len(comp) < 1 or len(orig) < 1:
				return False
			orig = re.sub(r"[^a-z ]", "", orig)
			comp = re.sub(r"[^a-z ]", "", comp)
			orig_ = orig.split(" ")
			comp_ = comp.split(" ")
			flag = False
			if len(orig_) != len(comp_):
				flag = False
				for entry1 in orig_:
					for entry2 in comp_:
						if abs(len(entry1) - len(entry2)) <= 1 and entry1[:1] == entry2[:1]:
							orig = entry1
							comp = entry2
							flag = True
							break
			else:
				flag = True
			if flag:
				if comp[:4] in orig or comp[-4:] in orig:
					return True
			return False
		if e:
			if not (abs(len(orig) - len(comp)) < 2 and (len(orig) > 4 and len(comp) > 4)):  
				return False
			orig = re.sub(r"[^a-z0-9]", "", orig)
			comp = re.sub(r"[^a-z0-9]", "", comp)
			if orig[:int(len(orig)*(thresh))] in comp[:int(len(comp)*(thresh))] or\
			comp[:int(len(comp)*(thresh))] in orig[:int(len(orig)*(thresh))]:
				return True
			return False
			
	if len(orig) <= 2 or len(comp) <= 2:
		return False	
	ret_val = False
	orig = orig.replace('customer', "")
	comp = comp.replace('customer', "")
	if orig in comp or comp in orig:
		return 1.
	check_lst = list()
	for i in range(len(orig) - 1):
		check_lst.append(orig[i:i+2])
	count = 0
	for thing in check_lst:
		if thing in comp:
			count += 1
	matcher_1 = count / float(len(orig) - 1)
	if not ret_matcher:
		if matcher_1 >= thresh:
			ret_val = True
	
	count = 0		
	
	check_lst = list()
	for i in range(len(comp) - 1):
		check_lst.append(comp[i:i+2])
	count = 0
	for thing in check_lst:
		if thing in orig:
			count += 1
	matcher_2 = count / float(len(comp) - 1)
	if not ret_matcher:
		if matcher_2 >= thresh:
			ret_val = True
				
	if not ret_matcher:
		return ret_val
	else:
		return (matcher_1 + matcher_2) / 2
		

def detect_file (key_lst, display_word, sl=False):
	cur_dir = os.getcwd() 
	file_lst = os.listdir(cur_dir)
	for file_name in file_lst:
		if sl:
			key=file_name.lower()
			if 'suppression' not in key and 'pap' not in key and 'staff' not in key and ('.csv' in key or '.xls' in key):
				return file_name
			continue
		for keyword in key_lst: 
			if keyword in file_name.lower() and '~' not in file_name:
				return file_name
				break


def write_items (dic, file, sales = False, target_headers=[]):

	write_lst = [(sale, dic[sale]) for sale in dic]
	dupe_check = dict()
	dup=False
	dupes=set()
	
	file.writerow(target_headers)

	to_sort=list()
	sup_entries=list()

	for item in write_lst:

		temp = list(item[0])
		check_ad = temp[2]
		write_ad = final_add_dict[check_ad]
		temp[2] = write_ad
		to_write = [sub for sub in temp]
		write_tup = tuple(to_write)
		dupe_key = to_write[2][:7]
		if dupe_key in dupe_check:
			dup=True
			dupes.add(dupe_check[dupe_key])
			dupes.add(write_tup)
			dupe_check[dupe_key] = write_tup
		dupe_check[dupe_key] = write_tup

		if (item[0][0].strip().lower(), item[0][1].strip().lower()) in name_dic:
			to_write = to_write + ["EXACT MASTER SUPPRESSION NAME MATCH"]
			sup_entries.append(to_write)
		else:
			to_sort.append(to_write)
	if sales and len(dupes) > 0:
		dupes = sorted(list(dupes), key = lambda x: x[2])
		print('\n')
		print('** POTENTIAL DUPLICATES FOUND **')
		count=0
		for entry in dupes:
			if count%2 == 0:
				print('\n')
			print(entry)
			count+=1
		print('\n** POTENTIAL DUPLICATES FOUND **\n')
	medate_ind=None

	for thing in to_sort:
		for i, entry in enumerate(thing):
			test=str(entry)
			if '-' in test and len(test) == 10:
				medate_ind=i
				break

	if medate_ind != None:
		try:
			final = sorted(to_sort, key = lambda x: x[medate_ind])
		except:
			print('date sorting failed')
			final=to_sort
	else:
		final=to_sort

	for entry1 in sup_entries:
		file.writerow(entry1)
	for entry2 in final:
		file.writerow(entry2)

	file.writerow([])
	file.writerow([])

	for item in write_lst:
		to_write = [sub1 for sub1 in item[0]]
		file.writerow(to_write)
		for record in item[1]:
			file.writerow([sub for sub in record])
		file.writerow([])
		file.writerow([])


sales_merged_name = detect_file(["sale","sales", 'service', 'services'], "Sales/Services", sl=True)
staff_check = False
excel_input=False

try:
	try:
		read_file = open(sales_merged_name, encoding = 'latin', newline='')
	except:
		print("Data file not found - make sure 'sales' or 'service' in filename")
		sys.exit()
	reader = csv.reader(read_file, dialect = csv.excel_tab, delimiter = ",", quotechar='"')
	sales_merged = [[entry.strip() for entry in item] for item in reader]
except:
	from pandas import read_excel
	excel_input=True
	data = read_excel(sales_merged_name, dtype='str')
	cols = [str(header) for header in data.columns.tolist()]
	data = data.values.tolist()
	data = [cols] + data
	sales_merged=data
	#sales_merged = [[str(entry) for entry in row] for row in data]
	#print(data)
	#sys.exit()

sales_merged_name = sales_merged_name.replace('xlsx','csv')
sales_merged_data = [list(thing) for thing in set([tuple(item) for item in sales_merged[1:]])]
sales_merged_headers = sales_merged[0]
sales_merged = [sales_merged_headers]+sales_merged_data

try:
	staff_filename = detect_file(["staff"], "Staff")
	staff = set([(item[0].strip().lower(), item[1].strip().lower()) for item in list(csv.reader(open(staff_filename, encoding = 'latin'), dialect = csv.excel_tab, delimiter = ","))])
	staff_check = True
	print(str(len(staff)) + " staff entries retrieved_\n")
except:
	print("\n\n** STAFF DATA COULD NOT BE RETRIEVED ** CONTINUING WITHOUT STAFF **_ \n\n")
	staff_check = False
service = False

target_headers_dict = {
1: ["first" ,"last", "address", "city", "state", "zip", "email", "date", "year", "make", "model", "type", "cost"],
2: ["first" ,"last", "address", "city", "state", "zip", "email", "year", "make", "model", 'vin', 'ronumber', 'date', 'roamount'],
3: ["first" ,"last", "address", "city", "state", "zip", "email", "date", "year", "make", "model", "type", "front","back","gross"]

}
all_headers=False
service_name=False
while True:
	choice = input("1 for enter for sales\n2 for service - must have proper headers\n3 for sales plus front, back and gross\n4 for all headers (first,last,address,city,state,zip,email must be first seven)\n")
	if len(choice) < 1:
		choice=1
	else:
		choice = int(choice)
		if choice == 2:
			service_name=True
		if choice == 4:
			all_headers=True
			target_headers=None
			break
			#choice=1
	try:
		target_headers = target_headers_dict[choice]
		break
	except:
		print('invalid choice')


mapper_inds, new_headers_dic, new_headers = map_cols(sales_merged, target_headers, all_headers=all_headers) #this is a dictionary mapping the indices of the target headers to their corresponding place in the data - 
# so at the end, write the target headers and the data will line up
#print(mapper_inds, new_headers_dic, new_headers)
#sys.exit()
reverse_mapper={value:key for key,value in new_headers_dic.items()}
target_headers=new_headers
start_date = date(2007,7,7)
end_date = date.today()

sales_to_process = list()
sales_suppression_lst = list()
headers_set = set([])

final_add_dict=dict()
	
for sale in sales_merged_data:
	
	append_sale = list()
	skip=False

	for idx in mapper_inds:

		if str(idx).startswith('missing') and new_headers_dic[idx] != 'type':
			to_add=''

		else:
			to_add=''
			corr_header = new_headers_dic[idx]
			if corr_header == 'first' and len(sale[idx]) < 1:
				print('BLANK FIRST NAME ENTRY SKIPPED - TO KEEP, ENTER VALUE IN SALES DOC AND RESTART')
				skip=True

			elif corr_header == 'date':
				r_date = sale[idx]
				if excel_input:
					try:
						r_date=str(r_date)
						if '-' in r_date:
							r_date=r_date.split(' ')[0].split('-')
							to_add = date(int(r_date[0]), int(r_date[1]), int(r_date[2]))
						else:
							r_date=r_date.split(' ')[0].split('/')
							to_add = date(int(r_date[2]), int(r_date[0]), int(r_date[1]))
						
					except:
						to_add=r_date
						print("Incorrect date format: {}".format(to_add))
				else:
					try:
						r_date = r_date.strip().split("/")
						if len(r_date[2]) != 4:
							r_date[2] = "20" + r_date[2]
						to_add = date(int(r_date[2]), int(r_date[0]), int(r_date[1]))
						if to_add < start_date or to_add > end_date:
							skip=True
					except:
						to_add=r_date
						print("Incorrect date format: {}".format(to_add))

			elif corr_header == 'address':
				local_add=sale[idx]
				if 'pobox' in local_add.replace(' ','').lower():
				#	print(local_add)
					skip=True
				to_add = convert(local_add).upper()
				#print(to_add, local_add)
				final_add_dict[to_add] = local_add.upper()

			elif corr_header == 'first':
				check = sale[idx].split(" ")
				if len(check) > 1:
					if len(check[1]) == 1 or len(check[0]) > 4:
						to_add = check[0]
					else:
						to_add = sale[idx]
				else:
					to_add = sale[idx]

			elif corr_header == 'zip':
				temp = sale[idx].replace("-","")
				if len(temp) == 9:
					to_add = temp[:5]
				elif len(temp) == 8:
					to_add = temp[:4]
				else:
					to_add = sale[idx]

			elif corr_header == 'type':
				if str(idx).startswith('missing'):
					try:
						auto_year = sale[reverse_mapper['year']]
						if int(auto_year) >= date.today().year:
							to_add="NEW"
						else:
							to_add="USED"
					except:
						to_add=''

				elif sale[idx].lower() == "n":
					to_add = "NEW"
				elif sale[idx].lower() == "u":
					to_add = "USED"
				elif sale[idx] == '':
					auto_year = sale[reverse_mapper['year']]
					if int(auto_year) >= date.today().year:
						to_add="NEW"
					else:
						to_add="USED"
				else:
					to_add=sale[idx]
			elif sale[idx] == 'nan':
				to_add=''
			else:
				to_add = sale[idx]
			try:
				to_add=to_add.upper()
			except:
				pass
			try:
				to_add=to_add.replace('$','')
			except:
				pass
			
		if type(to_add) == list:
			to_add=''
		append_sale.append(to_add)
	if skip:
		continue
	append_sale = tuple(append_sale)
	sales_to_process.append(append_sale)

PAP_filename = detect_file(["pap"], "PAP")
try:
	PAP = csv.reader(open(PAP_filename, encoding = 'latin',newline=''), dialect = csv.excel_tab, delimiter = ",", quotechar='"')
except:
	choice = input('\n\n\n*****PAP NOT FOUND, continue with blank PAP input? y/n\n\n\n')
	if choice == 'n':
		sys.exit()
	PAP = [['','','','','','','',''],['','','','','','','','']]
num_reg = r"^\S+\s"
PAP_dic = dict()
print("Processing PAP data...")

for entry in PAP:
	if entry[0] == 'EDID':
		newserver = True
	else:
		newserver = False
	break

for entry in PAP:
	if newserver:
		entry = tuple(entry[1:8])
	else:
		entry = tuple(entry)
	whole = entry[2].strip().lower()
	whole = re.sub(remove_re, "", whole, flags = re.IGNORECASE)
	zip1 = re.sub(r"[^0-9]", "", entry[5])
	
	if len(zip1) == 5 or len(zip1) == 9:
		zip1 = zip1[:5]
	elif len(zip1) == 4 or len(zip1) == 8:
		zip1 = "0" + zip1[:4]
	else:
		zip1 = ""
	try:
		number = re.match(num_reg, whole).group()
	except:
		continue
	address = " ".join(whole.split()[1:])
	PAP_dic[number] = PAP_dic.get(number, dict())
	PAP_dic[number][zip1] = PAP_dic[number].get(zip1, set([]))
	PAP_dic[number][zip1].add((address, entry))
	
suppression_filename = detect_file(["mastermerged", "master", "suppression"], "Suppression")
try:
	suppression = csv.reader(open(suppression_filename, encoding = 'latin'), dialect = csv.excel_tab, delimiter = ",")
except:
	choice = input('\n\n\n*****SUPPRESSION NOT FOUND, continue with blank suppression input? y/n\n\n\n')
	if choice == 'n':
		sys.exit()
	suppression = [['','','','','','','',''],['','','','','','','','']]
sup_dic = dict()
email_dic = dict()
name_dic = dict()
no_email = set(["n","cd", "info", "wng", "email", "none", "na", "no", "dnh", "noemail", "doesnothave",  "declined", "decline", "n/a", "refused", "noname", "nothing"])

print("Processing suppression data...")
skip_set = set()

for entry in suppression:
	entry = tuple(entry[:7])
	if entry in skip_set:
		continue
	
	email = entry[6]
	
	if "@" in email:
		email_check = email[:email.rfind("@")].strip().lower()
		
		if email_check not in no_email:
			email_dic[email.strip().lower()] = entry
			
	first = entry[0].strip().lower()		
	last = entry[1].strip().lower()		
	name = (first, last) 
	name_dic[name] = name_dic.get(name, set([]))  
	name_dic[name].add(entry)
 
	whole = convert(entry[2])
	entry = list(entry)
	entry[2] = whole
	entry = tuple(entry)
	try:
		number = re.match(num_reg, whole).    group()
		address = " ".join(whole.split()[1:])
	except:
		continue

	zip = re.sub(r"[^0-9]", "", entry[5])
	if len(zip) == 5 or len(zip) == 9:
		zip = zip[:5]
	elif len(zip) == 4 or len(zip) == 8:
		zip = "0" + zip[:4]
	else:
		zip = ""

	sup_dic[number] = sup_dic.get(number, dict())
	sup_dic[number][last] = sup_dic[number].get(last, set([])) 
	sup_dic[number][last].add(((zip, address), entry))
	skip_set.add(entry)

match_count = 0

def master (check_lst, sales_headers, check_against_lst, last_name = False,\
	match_val = 1, thresh = .8, final_sup_ = False, sup_ = False, comp_inds={}):
	master_count = len(check_lst)
	now_count = 0

	comp_inds = {"first": 0, "last": 1, "address": 2, "zip": 5, "email": 6}
				
	sales_match_dic = dict()

	def append_ (e = False):
		global match_count
		sales_match_dic[tuple(sale)] = set([])
		sales_match_dic[tuple(sale)].add(record_1)
		if not e:
			match_count += 1
			print("Total: " + str(match_count))
		else:
			match_count += 1
			print("Total: " + str(match_count) + " - EMAIL MATCH")
			
	def present_choice (input1, e = False):
		global exact_name
		percent = str(int(100 * float(now_count) / master_count)) + "%"
		to_present = "\nS: " + s_address_key + " " + s_zip_key + "\nO: " + input1[2].lower() + " " + input1[5].lower() + "\n\nS: " + s_first_key +\
		" " + s_last_key + "\nO: " + input1[0].lower() + " " + input1[1].lower() + "\n\nS: " + s_email_key  + "\nO: " + input1[6].lower() + "\n\nAccept? y/n_ "
		if e:
			choice = input("\n" + percent + ": ******* Potential EMAIL MATCH ******* found: \n" + to_present)
		else:
			choice = input("\n" + percent + ": ******* Potential match found *******: \n" + to_present)
		if len(choice) < 1 or choice == "y":
			append_() 
			return True	
		else:
			return False
		
	for sale in check_lst:
		now_count += 1
		s_email_key = sale[comp_inds['email']].strip().lower()
		s_address_key = sale[comp_inds['address']].strip().lower()
		s_last_key = sale[comp_inds['last']].strip().lower()
		s_first_key = sale[comp_inds['first']].strip().lower()
		
		s_zip_key = re.sub(r"[^0-9]", "", sale[comp_inds['zip']])
		if len(s_zip_key) == 5 or len(s_zip_key) == 9:
			s_zip_key  = s_zip_key[:5]
		
		elif len(s_zip_key) == 4 or len(s_zip_key) == 8:
			s_zip_key = "0" + s_zip_key[:4] 
		
		else:
			s_zip_key = ""
			
		go_on = True
		
		if sup_:
			if match_val != 1:
				if "@" in s_email_key:
					s_e_check = s_email_key[:s_email_key.rfind("@")]
					if len(s_e_check) > 8:
						for email in email_dic:
							if match(email[:email.rfind("@")], s_e_check, match_val_ = 2, thresh = 0.9, e = True):
								record_1 = email_dic[email]
								if present_choice(email_dic[email], e = True):
									go_on = False
									break
							
				if go_on:
					try:
						number = re.match(num_reg, s_address_key).group()
						address = " ".join(s_address_key.split()[1:])
					
					except:
						continue
					try:
						check = sup_dic[number]
					except:
						continue
			
					for record in check:
						if not go_on:
							break
						for entry in check[record]: 
							if not go_on:
								break
							if match(entry[0][1], address, match_val_ = 2, address = True, sup = sup_):
								if match(s_first_key, entry[1][0], match_val_ = 2, name = True) or match(s_first_key, entry[1][1], match_val_ = 2, name = True) or\
								match(s_last_key, entry[1][0], match_val_ = 2, name = True) or match(s_last_key, entry[1][1], match_val_ = 2, name = True):
									record_1 = entry[1]
									if present_choice(entry[1]):
										go_on = False
										break
			else:
				
				check = email_dic.get(s_email_key, 0)
				if check != 0:
					record_1 = email_dic[s_email_key]
					append_(e = True)
					continue
				try:
					try:
						number = re.match(num_reg, s_address_key).group()
						address = " ".join(s_address_key.split()[1:])
						
					except:
						continue
					check = sup_dic[number][s_last_key]
					for record in check:
						if record[0][0] == s_zip_key and match(record[0][1], address, address = True):
							record_1 = record[1]
							append_()
							break
				except:
					continue
					
		else:
		
			try:
				number = re.match(num_reg, s_address_key).group()
				address = " ".join(s_address_key.split()[1:])
			except:
				continue
		
			if match_val != 1:
				try:
					check = PAP_dic[number]
					for entry in check:
						if not go_on:
							break
						if entry == s_zip_key or len(s_zip_key) == 0 or len(entry) == 0:
							
							review_ = check[entry]
							for review in review_:
								
								if match(review[0], address, match_val_ = 2, address = True, sup = sup_):
									record_1 = review[1]
									if present_choice(record_1):
										break 
										go_on = False
				except:
					continue
			else:
				try:
					check = PAP_dic[number][s_zip_key]
					for record_ in check:
						if match(record_[0], address, address = True):
							record_1 = record_[1]
							append_()
							break
				except:
					continue
			
	return sales_match_dic

comp_inds = {"first": 0, "last": 1, "address": 2, "zip": 5, "email": 6}
	
print("\nSUPPRESSION MATCHES:\n")
dummy_headers = [["header", "header", "header", "header", "header", "header", "header"]]
supp_dics = master(sales_to_process, target_headers, dummy_headers , last_name = True, sup_ = True, comp_inds=comp_inds)
more_sup = list()
for item in sales_to_process:
	if item not in supp_dics:
		more_sup.append(item)
		
print("\n" + str(match_count) + " suppression matches found. Checking for possible suppression matches_\n")
manual_sup_dics = master(
	more_sup, target_headers, dummy_headers, 
	match_val = 2, final_sup_ = True, sup_ = True)
	
supp_dics.update(manual_sup_dics) 
clean_sales = list() 
staff_sup_lst = list()
if staff_check: 
	staff_last_check = set([item[1] for item in staff])
	print("\nPerforming staff suppression_\n")

count = 0
master_staff_count = 0
for item in sales_to_process:
	if item not in supp_dics:
		master_staff_count += 1
try:
	if len(staff) >= 100 or len(sales_to_process) >= 500:
		len_num = 4
	else:
		len_num = 3
except:
	len_num = 3
last_len_num = len_num * -1

for item in sales_to_process:
	skip = False
	if item not in supp_dics:
		if not staff_check:
			clean_sales.append(item)
			continue

		s_last_key = item[1].strip().lower()
		s_first_key = item[0].strip().lower()
		sale_name = (s_first_key, s_last_key)
		s_name_dict = dict()
		
		count += 1
		
		for name in staff:
			skip = False
			staff_last = name[1]
			if s_last_key == staff_last: 
				staff_sup_lst.append(sale_name)
				skip = True
				break

			if not skip and abs(len(staff_last) - len(s_last_key)) <= 1 or " " in staff_last or " " in s_last_key or "-" in staff_last or "-" in s_last_key:
				if staff_last[:len_num] == s_last_key[:len_num] or (staff_last[last_len_num:] == s_last_key[last_len_num:] and staff_last[0] == s_last_key[0]):
					try:
						s_name_dict[sale_name].append(name)
					except:
						s_name_dict[sale_name] = list()
						s_name_dict[sale_name].append(name)
		append = True
		
		if not skip:
					
			for raw_name in s_name_dict:
				app_name = raw_name
				name = (raw_name[1], raw_name[0])
				print("\n" + " ".join(name) + " ***")
				display = sorted(s_name_dict[raw_name], key = lambda x: x[1])
				for thing in display:
					print(" ".join((thing[1], thing[0])))
				choice = input("\n\nAccept? y/n_ ")
				if choice == "y" or len(choice) < 1:
					staff_sup_lst.append(app_name)
					append = False
				print(str(int(100 * float(count) / master_staff_count)) + "%")
			if append:
				clean_sales.append(item)

				
if len(staff_sup_lst) > 0:
	print("\nClean sale names suppressed off staff list:\n")
	for name in staff_sup_lst:
		print(" ".join(list(name)))


match_count = 0
print("\nPAP MATCHES:\n")
match_dics = master(clean_sales, target_headers, dummy_headers, sup_ = False,comp_inds=comp_inds)
print("\n" + str(match_count) + " PAP matches found. Checking for possible PAP matches_\n")
partial_match_lst = list()
for item in clean_sales:
	if item not in match_dics: 
		partial_match_lst.append(item)
partial_dics = master(partial_match_lst, target_headers, dummy_headers, match_val = 2, sup_ = False) 
match_dics.update(partial_dics)
				 
add_to_sup = list()
for item in clean_sales:
	if item not in match_dics:
		add_to_sup.append(item)

print("Writing to files... ")

target_headers = [header.title() for header in target_headers]

s_reg = r'[0-9()]'
sales_merged_name = re.sub(r'[0-9\_\-]|sale[s]{,1}|service[s]{,1}', " ", sales_merged_name, flags = re.IGNORECASE)
sales_merged_name = sales_merged_name.replace(".csv","")
sales_merged_name = "_".join(sales_merged_name.split())
file_path = os.getcwd()
today_date = str(date.today())
today_new = today_date.split("-")
today_final = list()
today_final.append(today_new[1])
today_final.append(today_new[2])
today_final.append(today_new[0])
today_final = "-".join(today_final)

orig_dir_name='Data'

for file in os.listdir(os.path.split(os.getcwd())[0]):
	if 'Input' in file:
		orig_dir_name=file[:file.rfind('_Pro')]
		break

#pre = sales_merged_name + "_Processed_" + today_final + "_Output"
if service_name:
	pre = orig_dir_name + "_Processed_" + today_final + "_Output_SERVICE"
else:
	pre = orig_dir_name + "_Processed_" + today_final + "_Output"
directory = os.path.dirname(file_path) +  "/" + pre

try:
	os.stat(directory)
except:
	os.mkdir(directory)
os.chdir(directory)

if not service_name:
	match_name = orig_dir_name + "_Processed_" + today_final + "_Sales_Match_REFERENCE"
	clean_name = orig_dir_name + "_Processed_" + today_final + "_Clean_Sales"
	sup_name = orig_dir_name + "_Processed_" + today_final + "_Suppressed_Sales"
	tbssl_name = orig_dir_name + "_Processed_" + today_final + "_All_Sales"
else:
	match_name = orig_dir_name + "_Processed_" + today_final + "_Service_Match_REFERENCE"
	clean_name = orig_dir_name + "_Processed_" + today_final + "_Clean_Services"
	sup_name = orig_dir_name + "_Processed_" + today_final + "_Suppressed_Services"
	tbssl_name = orig_dir_name + "_Processed_" + today_final + "_All_Services"

clean = csv.writer(open(clean_name +".csv", "w", encoding='latin', newline=''), delimiter=',', quotechar='"')
sales_match = csv.writer(open(match_name +".csv", "w", encoding='latin', newline=''), delimiter=',', quotechar='"')
suppressed_sales = csv.writer(open(sup_name +".csv", "w", encoding='latin', newline=''), delimiter=',', quotechar='"')
raw_sales = csv.writer(open(tbssl_name +".csv", "w", encoding='latin', newline=''), delimiter=',', quotechar='"')

raw_sales.writerow(target_headers)

for item in sales_to_process:
	raw_sales.writerow([sub for sub in item])
	
clean.writerow(target_headers)
		
for item in clean_sales:
	
	if (item[0].strip().lower(), item[1].strip().lower()) in name_dic:
		clean.writerow([sub for sub in item] + ["EXACT MASTER SUPPRESSION NAME MATCH"])
	else:
		clean.writerow([sub for sub in item])

write_items(match_dics, sales_match, sales = True, target_headers=target_headers)
write_items(supp_dics, suppressed_sales, target_headers=target_headers)
