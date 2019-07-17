#The following script takes an auto dealership website as input, parses the html, prompts
#the user to enter a 'sample' staff member name, determines the html context of the name and subsequently
#uses BeautifulSoup to extract all matching entries.
#It then applies some cleaning to the extracted data and outputs a csv file consisting of first and last names.
#The same script can be customized to extract other kinds of information.

import requests
from bs4 import BeautifulSoup as bs
import re
import os

def func():

    while True:
        manual = False
        dealer_site = input("\nInput dealer staff site_ ")
        if len(dealer_site) < 1:
            for file in os.listdir(os.getcwd()):
                if 'htm' in file:
                    soup = bs(open(file).read(), 'lxml')
                    break
            manual = True
            
        else:
            try:
                file_name = re.search(r"www\.(.+)\.(?:net|com)", dealer_site).groups(0)[0].title() + "_Staff.csv"
                r = requests.get(dealer_site)
                soup = bs(r.text, 'lxml')
            except:
                print("Invalid web address_ ")
                continue

        sample = input("\nEnter sample staff member name_ ")
        
        main_tag, main_attr = '', ''
        
        for tag in soup(True):
            for key, value in tag.attrs.items():
                if value == sample:
                    main_tag, main_attr = tag.name, key
                    break
        
        if len(main_tag) > 0 and len(main_attr) > 0: 
        
            check = soup.find_all(main_tag)
            lst = []
            for tag in check:
                try:
                    lst.append(tag[main_attr])
                except:
                    continue
        else:
            try:
                search_tag = soup.find(text = re.compile(sample)).parent.name
            except:
                print("\nUnable to make staff file - template written to desktop_ ")
                os.chdir("/Users/dataservices/Desktop")
                output = open(file_name, 'w')
                output.write("First,Last\n")
                output.close()
                continue
            
            lstx = [item.text for item in soup.find_all(search_tag)]
            lst = []
            
            for name in lstx:
                
                try:
                    lst.append(re.search(r"([a-z/-]+(?: [a-z/./-]+){1,2})?", name, flags = re.IGNORECASE).group())
                except:
                    continue
            
        def remove_bad (input_list):
            bad = set(['coordinator', 'admin', 'administration', 'assistant', 'greeter', 'pixel', 'used', 'new', 'car', 'auto', 'director', 'manager', 'sales', 'service', 'general', 'internet', 'staff', 'open', 'closed', 'hours'])
            output_set = set()
        
            for entry in input_list:
                if len(entry) < 1:
                    continue
                
                bad_check = False
                check = [name.lower() for name in entry.split()]
                
                if len(check) < 2:
                    continue
       
                for sub in check:
                    if sub in bad:
                        bad_check = True
                        
                if len(check) == 3:
                    if len(check[1].replace(".","")) == 1:
                        check = [check[0], check[-1]]
                        
                    else:
                        check = [check[0], " ".join(check[1:])]
                        
                if not bad_check:
                    output_set.add(" ".join([check[0].title(), check[1].title()]))
                    
            return sorted(list(output_set), key = lambda x: x.split(" ")[-1])
        
        lst = remove_bad(lst)
        os.chdir("/Users/dataservices/Desktop")
        if not manual:
            output = open(file_name, 'w')
            
        else:
            output = open(input('\nEnter dealership name_ ') + "_Staff.csv", 'w')
            
        output.write("First,Last\n")
        for item in lst:
            item = item.split(" ")
            if len(item) > 2:
                item = item[0] + "," + " ".join(item[1:])
            else:
                item = ",".join(item)
            output.write((item) + "\n")
        output.close()
        
        print("\nStaff list created to Desktop with following names:\n")
        
        print("\n".join(lst))
func()
