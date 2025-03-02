import PyPDF2
import Person
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfReader
applicant = Person
with open('Everidge.pdf','rb') as file:
    reader=PdfReader(file)
    fields=reader.get_fields()
    if fields:
        for field in fields.keys():
            field_info=fields[field]
            field_name =field_info.get('/T')
            
            if {field}=='Field Name: 1 First name(s)':
                print({field_info})
            
     
