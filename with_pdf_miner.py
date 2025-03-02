from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams


output_string=StringIO()
with open('FL401.pdf') as in_file:
    extract_text_to_fp(in_file,output_string,laparams=LAParams(),output_type='text')
    content = output_string.getvalue()
    print(content)
    

