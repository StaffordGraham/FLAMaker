import PyPDF2
from typing import List
import re
import spacy



def extract_text_from_pdf(pdf_file:str)->List [str]:
		pdf_text=[]

		with open(pdf_file,'rb') as pdf:
			reader=PyPDF2.PdfReader(pdf,strict=False)
			for page in reader.pages:
				content=page.extract_text()
				if content:
					pdf_text.append(content)
     
		pdf_text=' '.join(pdf_text)
		print(pdf_text)
		
def is_clean(entity: str) -> bool:
        entit =entity
        answer =True
    # Define conditions for noise, e.g., if it contains 'Document ID' or is too short
        if 'Zoho Sign Document ID' in entit or len(entit) >10 :
            answer= False
        
     
        return answer
 
            
            
		
            
            

        
def get_name_and_address_with_spacy(text_list):

    results_list=[]
    results_list.append('seed_string')
    combined_text= " ".join(text_list)
    nlp=spacy.load("en_core_web_sm")
    doc=nlp(combined_text)
    for ent in doc.ents:
            i=is_clean(ent.text)
            if i ==True and  ent.text !=None:
                results_list.append(ent.text)
                
    for result in results_list:
        print(result)
    
    return results_list
                
                
   
        
    
if __name__=='__main__':
    extracted_text =extract_text_from_pdf('FL401.pdf')
    get_name_and_address_with_spacy(extracted_text)
   
    #print("Addresses: ",addresses)
    
