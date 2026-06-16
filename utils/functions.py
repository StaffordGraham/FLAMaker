from datetime import datetime
from datetime import date
import _tkinter
import pickle
import os
from email.mime import text
from tkinter import ttk
import pdfplumber
from classes.Person import Person
from classes.Child import Child

with open(os.path.join("data", "girl_names_set.pkl"), "rb") as f:
    girl_names = pickle.load(f)
with open(os.path.join("data", "boy_names_set.pkl"), "rb") as f:
    boy_names = pickle.load(f)

def detect_gender(first_name: str) -> str:
    name = first_name.strip().lower()

    if name in girl_names:
        return "Female"
    if name in boy_names:
        return "Male"
    return ""   # unknown / ambiguous

def json_to_case_details(data_json, case_details):
    # 1. Basic fields
    case_details.relationship = data_json.get("relationship", "")
    case_details.case_number = data_json.get("case_number", "")
    case_details.court_name = data_json.get("court_name", "")
    case_details.notice = "Without Notice" if data_json.get("without_notice") else "On Notice"
    case_details.reasons = data_json.get("reasons", "")

    # 2. Application type
    case_details.molestation_order = data_json.get("nonmol", False)
    case_details.occupation_order = data_json.get("occupation", False)

    if case_details.molestation_order and case_details.occupation_order:
        case_details.application = "Occupation & Non-molestation"
    elif case_details.molestation_order:
        case_details.application = "Non-molestation"
    elif case_details.occupation_order:
        case_details.application = "Occupation"
    else:
        case_details.application = ""
    # 3. Applicant
    app = data_json.get("applicant", {})
    case_details.applicant.first_name = app.get("first_name", "")
    case_details.applicant.last_name = app.get("last_name", "")
    case_details.applicant.address = app.get("address", "")
    case_details.applicant.postcode = app.get("postcode", "")
    case_details.applicant.gender=detect_gender(case_details.applicant.first_name)

    # 4. Respondent
    resp = data_json.get("respondent", {})
    addr = resp.get("address", {})
    
    case_details.respondent.first_name = resp.get("first_name", "")
    case_details.respondent.last_name = resp.get("last_name", "")
    case_details.respondent.address_building_and_street = addr.get("line1", "")
    case_details.respondent.address_second_line = addr.get("line2", "")
    case_details.respondent.address_town_or_city = addr.get("town", "")
    case_details.respondent.address_postcode = addr.get("postcode", "")
    case_details.respondent.gender=detect_gender(case_details.respondent.first_name)

    # 5. Children

    for child_json in data_json.get("children", []):
        full_name = child_json.get("name", "").strip()
        dob_string = child_json.get("dob", "").strip()
        try:
            dob_object = datetime.strptime(dob_string, "%d/%m/%Y").date()
        except:
            dob_object = None

        parts = full_name.split()
        first = parts[0] if parts else ""
        last = parts[-1] if len(parts) > 1 else ""

        child = Child(
        first_name=first,
        last_name=last,
        gender="",          # extractor doesn’t provide gender
        dob=dob_object
    )

        case_details.children.append(child)
    


    # 6. Family home
    fh = data_json.get("family_home", {})
    case_details.family_home_building_and_street = fh.get("building_and_street", "")
    case_details.family_home_address_second_line = fh.get("second_line", "")
    case_details.family_home_address_town_or_city = fh.get("town_or_city", "")
    case_details.family_home_postcode = fh.get("postcode", "")

    # 7. Hearing date
    case_details.hearing_date = data_json.get("hearing_date", "")

    # 8. Generate filename
    case_details.name_file()

    return case_details

def extract_date_from_pdf():
    pass
    
#SECTION ONE APPLICANT

page_no = 11
path=r"C:/Users/sgcam/Projects/pdf_Extract/Tudor v Tudor.pdf"

with pdfplumber.open(path) as pdf:
    if page_no < len(pdf.pages):
        page = pdf.pages[page_no]   
        tables=page.extract_tables()
        child_table=tables[0]
        
        if tables:
            child_table=tables[0]
            headers=child_table[0] 
            rows=child_table[1:]
            children =[]


#SECTION TWO RESPONDENT


#SECTION THREE CHILDREN



    
    
    
    

def reduce_pdf_text(text: str) -> str:
    # 1. Normalize whitespace
    text = " ".join(text.split())

    # 2. Split into pseudo-sentences
    chunks = text.split(".")

    # 3. Keep only relevant chunks
    KEYWORDS = ["court", "case", "number", "applicant",
        "respondent", "name", "relationship"
    ]

    filtered = [
        c.strip()
        for c in chunks
        if any(k in c.lower() for k in KEYWORDS)
    ]
    return ". ".join(filtered)  


def date_format(d,long_month):
    long_months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    short_months= ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    if isinstance(d, date):
        day = d.day    
        if long_month:
            month=long_months[d.month-1]
        else:
            month=short_months[d.month-1]
        
        
            year = d.year
    else:
        day, month, year = d.split('/')
        
        day =str(int(day))

        
        if long_month:
            month=long_months[int(month)-1]
        else:
            month=short_months[int(month)-1]
            
        return f" {day} {month} {year}"
    
def article(word):
    if word:
        vowels='aeiou'
        word=word.lower()
        first_letter =word[0]
        if first_letter in vowels:
            return 'an'
        else:
            return 'a'
        
def find_and_strip(lines, line_before,marker):
    
    output=""
    for i, line in enumerate(lines):
            if line_before in line: 
                output = lines[i+1].strip() 
            if marker and marker in output :
                output=output.split(marker)[0].strip()
                
    return output

import re

def normalise_postcode(raw):
    if not raw:
        return ""

    # Remove all spaces
    compact = raw.replace(" ", "")

    # UK postcodes are always last 3 characters for the inward code
    if len(compact) > 3:
        return compact[:-3] + " " + compact[-3:]
    else:
        return compact


    
    
    
        
def convert_dob_to_datetime(child):
    return datetime.strptime(child.dob, '%m/%d/%Y')

class DatePicker(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Initialize day, month, and year values
        self.days = [str(day) for day in range(1, 32)]
        self.months = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        self.years = [str(year) for year in range(1900, 2101)]

        # Create and grid the comboboxes within the frame
        self.day_combobox = ttk.Combobox(self, values=self.days, width=5)
        self.day_combobox.set("Day")
        self.day_combobox.grid(row=0, column=0, padx=2)

        self.month_combobox = ttk.Combobox(self, values=self.months, width=10)
        self.month_combobox.set("Month")
        self.month_combobox.grid(row=0, column=1, padx=2)

        self.year_combobox = ttk.Combobox(self, values=self.years, width=7)
        self.year_combobox.set("Year")
        self.year_combobox.grid(row=0, column=2, padx=2)

    def get_date(self):
        """Get the selected date as a string."""
        day = self.day_combobox.get()
        month = self.month_combobox.get()
        year = self.year_combobox.get()
        return f"{month} {day}, {year}"
    
    def reduce_pdf_text(text: str) -> str:
    # 1. Normalize whitespace
        text = " ".join(text.split())

    # 2. Split into pseudo-sentences
        chunks = text.split(".")

    # 3. Keep only relevant chunks
        KEYWORDS = ["court", "case", "number", "applicant",
        "respondent", "name", "relationship"
    ]

        filtered = [
        c.strip()
        for c in chunks
        if any(k in c.lower() for k in KEYWORDS)
    ]

        return ". ".join(filtered)
