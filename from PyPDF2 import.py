from PyPDF2 import PdfReader
reader = PdfReader("FL401.pdf")
form_data=reader.get_fields()
if form_data:
    for field_name, field_info in form_data.items():
        field_value=field_info.get('/V','')
        print(f"Field:{field_name}, Value:{field_value}")