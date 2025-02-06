import PyPDF2
import tkinter as tk
from tkinter import filedialog

def extract_field_names(pdf_path):
    field_names=set()
    with open(pdf_path,'rb')as file:
        pdf_reader=PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            annotations=page.get('//Annots',[])
            for annotation in annotations:
                field_obj=annotation.get_object()
                field_name=field_obj.get('/T')
                if field_name:
                    field_names.add(field_name)
    return field_names  

if __name__ == '__main__':
    # Example usage
    pdf_file_path = input("Enter the path to your PDF file: ")  # Prompt for PDF path
    field_names = extract_field_names(pdf_file_path)

    # Print the discovered field names
    print("Field Names Found:")
    for name in field_names:
        print(name)
              