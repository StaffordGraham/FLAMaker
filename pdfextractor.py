import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog
from  Person import Person 
from Respondent import Respondent

def open_file_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path =filedialog.askopenfilename()
    if file_path:
        return file_path

    if __name__ =="__main__":
        selected_file=   open_file_dialog()
        
    return selected_file

def extract_field_names(pdf_path):
    field_names=set()
    with open(pdf_path,'rb')as file:
        pdf_reader=PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            annotations = page.get('/Annots', None)
            if annotations:
                for annotation in annotations:
                    field_obj = annotation.get_object()
                    field_name = field_obj.get('/T')
                    if field_name:
                        field_names.add(field_name)
    return field_names                
                    
            
def get_App_Data(selected_file):
# Open the PDF file in binary mode
    with open(selected_file, 'rb') as file:
    # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        page = pdf_reader.pages[4]
    
    # Extract form fields and their values
        applicant = Person('Applicant')
        form_fields = page['/Annots',None]
        for field in form_fields:
            field_obj = field.get_object()
            field_name = field_obj.get('/T')  # Get the field name
            field_value = field_obj.get('/V')  # Get the field value
                    
            if field_name=='1 First name(s)':
                applicant.first_name=field_value
                    
            
            if field_name=='1 Last name':
                applicant.last_name=field_value
            
            if field_name=='3 Your date of birth - DD':
                applicant.dob_DD=field_value
                
            if field_name=='3 Your date of birth - MM':
                applicant.dob_MM=field_value
                
            if field_name=='3 Your date of birth - YYYY':
                applicant.dob_YYYY=field_value
                
            if field_name=='5 Your full current address: building and street':
                applicant.address_building_and_street=field_value
                
            if field_name=='5 Your full current address: second line of address':
                applicant.address_second_line=field_value
                
            if field_name=='5 Your full current address: town or city':
                applicant.address_town_or_city=field_value            
            if field_name=='5 Your full current address: postcode':
                applicant.address_postcode=field_value    
            
    
def get_Resp_Data(selected_file,respondent):
    
       
            with open('Application_Form.pdf', 'rb') as file:
   
        
                pdf_reader = PyPDF2.PdfReader(selected_file)
                page2 = pdf_reader.pages[7]

    
    # Extract form fields and their values
            form_fields2 = page2['/Annots']
            for field in form_fields2:
                field_obj = field.get_object()
            field_name = field_obj.get('/T')  # Get the field name
            field_value = field_obj.get('/V')  # Get the field value
            
            if field_name=='1 First name(s)':
                respondent.first_name=field_value      
                
            if field_name=='1 Last name':
                respondent.last_name=field_value
            
            if field_name=="3 The respondent's date of birth - DD":
                respondent.dob_DD=field_value
                
            if field_name=="3 The respondent's date of birth - MM":
                respondent.dob_MM=field_value
                
            if field_name=="3 The respondent's date of birth - YYYY":
                respondent.dob_YYYY=field_value
                
            if field_name =="4 Can your contact details be shared with the respondent? Yes":
                flag = 'flag'
                
            if field_name=="5 Respondent's full current address: building and street":
                respondent.address_building_and_street=field_value
                
            if field_name=="5 Respondent's full current address: Building and street":

                respondent.address_second_line=field_value
                
            if field_name=="5 Respondent's full current address: Town or city":
                respondent.address_town_or_city=field_value            
            if field_name=="5 Respondent's full current address: postcode":
                respondent.address_postcode=field_value    
def main():
    selected_file = open_file_dialog()
    if selected_file:
        applicant = get_App_Data(selected_file)
        respondent = Respondent('Respondent')  # Create a respondent instance
        get_Resp_Data(selected_file, respondent)

        # Example: Print extracted data
        print("Applicant Data:")
        print(f"First Name: {applicant.first_name}")
        print(f"Last Name: {applicant.last_name}")
        print(f"DOB (DD): {applicant.dob_DD}, (MM): {applicant.dob_MM}, (YYYY): {applicant.dob_YYYY}")
        print(f"Address: {applicant.address_building_and_street}, {applicant.address_second_line}, "
              f"{applicant.address_town_or_city}, {applicant.address_postcode}")
        
        print("\nRespondent Data:")
        print(f"First Name: {respondent.first_name}")
        print(f"Last Name: {respondent.last_name}")
        print(f"DOB (DD): {respondent.dob_DD}, (MM): {respondent.dob_MM}, (YYYY): {respondent.dob_YYYY}")
        print(f"Address: {respondent.address_building_and_street}, {respondent.address_second_line}, "
              f"{respondent.address_town_or_city}, {respondent.address_postcode}")

if __name__ == "__main__":
    main()
                    


        
         
            
            
        
        
