import pdfplumber
import name_to_list
from name_to_list import load_names
from name_to_list import is_it_name
import spacy
import re
import sys
postcodes=[]

def is_postcode(postcode):
    
    
    postcode=postcode.strip().upper()
    if is_it_name(postcode):
        return False
        
    
    num_spaces=postcode.count(" ")
    if num_spaces>1:
        postcode=postcode.replace(" ","")
        
    if len(postcode)==7:
        postcode=postcode[:4]+" "+postcode[4:]
       
    else:
        return False
    
    char1=postcode[3]
    char2=postcode[4]
    char3=postcode[6]
    if can_convert_to_int(char1)==False or can_convert_to_int(char2) or can_convert_to_int(char3):
        return False
    else:
        return True
    
def clean_postcode(postcode):
    postcode=postcode.strip().upper()
        
    postcode=postcode.replace(" ","")
        
    postcode=postcode[:4]+" "+postcode[4:]
    return postcode
       
 
    
        
    

def can_convert_to_int(s):
        s=s.replace(" ","")
        try:
            int(s)
            return True
        except ValueError:
            return False
        
#OPEN THE FILE WITH PDFPLUMBER 
with pdfplumber.open("FL401.pdf") as pdf:
    text_list=[]
    names_list = load_names("names.txt")
    only_names=[]
    for page in pdf.pages:
        text=page.extract_text()
        if text:
            text_list.extend(text.splitlines())
    for item in text_list:
        print(item)
    sys.exit()
 
    #REMOVE INTEGERS
    iteration1=[]
    for item in text_list:
        if not isinstance(item,(int)):
            iteration1.append(item)
            
	#REMOVE SPACES
            
    for item in iteration1:
        if item.count(" ")>3:
            item.replace(" ","")
        
    for item in iteration1:
    
		
    #REMOVE NUMBERS THAT ARE STRINGS
        if can_convert_to_int(item):
            iteration1.remove(item)
            
	
            
    #for iter in iteration1:
        #print(iter)
    for i in range (len(text_list)):
        
        test_var = text_list[i]
        test_var=is_postcode(test_var)
        if test_var!=False:
            postcodes.append(test_var)
            
    #Put any line that contains a postcode into postcode format 
    for index,item in enumerate (text_list):
        if is_postcode(item):
            text_list[index]=clean_postcode (item)
            
    
            
    for index, item in enumerate(text_list):
        if is_it_name(item) or is_postcode(item):
            text_list[index]=text_list[index]
        else:
            del text_list[index]
            
    for index, item in enumerate(text_list):
        if len(item)>20:
            del text_list[index]
     
     
            
    
    for item in text_list:
        print(item)
        
    
     
            
            
     
         
        
        # if text_list[i] in names_list:
        #     text_list[i].capitalize()
        #     text_list[i+1].capitalize()
        #     only_names.append(text_list[i])
        #     only_names.append(text_list[i+1])
        #     only_names.append(text_list[i+3])
        #     only_names.append(text_list[i+5])
        #     only_names.append(text_list[i+7])
        #     only_names.append(text_list[i+8])
            
   #START WORK WITH SPACY
    # nlp=spacy.load("en_core_web_sm")
        
        
   
                