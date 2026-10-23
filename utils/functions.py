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

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

with open(os.path.join(DATA_DIR, "girl_names_set.pkl"), "rb") as f:
    girl_names = pickle.load(f)
with open(os.path.join(DATA_DIR, "boy_names_set.pkl"), "rb") as f:
    boy_names = pickle.load(f)
    
def standard_entries(case_details):
    std_non_mol=[]
    std_occ_ord=[]
    std_recital=[]

    std_non_mol.append( "Use or threaten violence")
    std_non_mol.append("Not intimidate,harass or pester")
    std_non_mol.append("Not communicate")
    std_non_mol.append("Not damage property")
    std_non_mol.append("Not damage family home")
    std_occ_ord.append("Declaration of Mat Home Rights",)
    std_occ_ord.append("R Allow Occupy  of Mat Home")
    std_occ_ord.append("R Allow Occupy  of Mat Home")
    std_occ_ord.append( "R Must Not Occupy Mat Home")
    std_occ_ord.append("R Not Return to Mat Home")
    std_recital.append("Upon reading the statement of the Applicant dated ")
    if case_details.molestation_order==True:
        case_details.orders.extend(std_non_mol)
        
    if case_details.occupation_order==True:
        case_details.orders.extend(std_occ_ord)
    




    
    


def detect_gender(first_name: str) -> str:
    # The name sets are stored in title case, e.g. "Archer"
    name = first_name.strip().title()

    if name in girl_names:
        return "Female"
    if name in boy_names:
        return "Male"
    return ""   # unknown / ambiguous

def is_ticked(value):
    # PDF form checkboxes come through as e.g. "/Yes" or "/Off"; the OCR extractor gives True/False
    if isinstance(value, bool):
        return value
    return value not in (None, "", "/Off", "Off")

RELATIONSHIP_NAMES = {
    "married": "Marriage",
    "formerly_married": "Marriage",
    "engaged": "Engaged",
    "formerly_engaged": "Engaged",
    "live_together": "Cohabitee",
    "formerly_lived_together": "Cohabitee",
    "cohabitees": "Cohabitee",
    "former_cohabitees": "Cohabitee",
    "partner_not_living_together": "Intimate Significant Duration",
    "former_partner_not_living_together": "Intimate Significant Duration",
    "partners_not_living_together": "Intimate Significant Duration",
    "former_partners_not_living_together": "Intimate Significant Duration",
}

def relationship_from_json(rel):
    # Form-field extractor: {"married": "/Yes", ...}; OCR extractor: {"relationship_category": "married"}
    if isinstance(rel, str):
        return rel
    if not isinstance(rel, dict):
        return ""
    category = rel.get("relationship_category")
    if category:
        return RELATIONSHIP_NAMES.get(category, "")
    for key, name in RELATIONSHIP_NAMES.items():
        if is_ticked(rel.get(key)):
            return name
    return ""

def json_to_case_details(data_json, case_details):
    # 1. Basic fields
    case_details.relationship = relationship_from_json(data_json.get("relationship"))
    case_details.case_number = data_json.get("case_number", "")
    case_details.court_name = data_json.get("court_name", "")

    # Only the "Yes" box counts - the "No" box being ticked must not make it a without notice hearing
    wn = data_json.get("without_notice") or {}
    without_notice = is_ticked(wn.get("apply_yes")) or wn.get("without_notice") is True
    case_details.notice = "Without Notice" if without_notice else "On Notice"
    case_details.reasons = data_json.get("reasons", "")

    # 2. Application type
    nonmol = data_json.get("nonmol") or {}
    orders_requested = data_json.get("orders_requested") or {}
    case_details.molestation_order = (is_ticked(nonmol.get("apply_yes"))
                                      or orders_requested.get("non_molestation_order") is True)
    case_details.occupation_order = orders_requested.get("occupation_order") is True

    if case_details.molestation_order and case_details.occupation_order:
        case_details.application = "Occupation & Non-molestation"
    elif case_details.molestation_order:
        case_details.application = "Non-molestation"
    elif case_details.occupation_order:
        case_details.application = "Occupation"
    else:
        case_details.application = ""
    # 3. Applicant
    app = data_json.get("applicant") or {}
    app_addr = app.get("address") or {}
    case_details.applicant.first_name = app.get("first_name", "")
    case_details.applicant.last_name = app.get("last_name", "")
    case_details.applicant.address_building_and_street = app_addr.get("line1", "")
    case_details.applicant.address_second_line = app_addr.get("line2", "")
    case_details.applicant.address_town_or_city = app_addr.get("town", "")
    case_details.applicant.address_postcode = app_addr.get("postcode", "")
    case_details.applicant.gender=detect_gender(case_details.applicant.first_name)
    case_details.applicant.set_pronouns()

    # FL401 question 2.4: can the applicant's contact details be shared with the respondent?
    if is_ticked(app.get("share_contact_details_no")):
        case_details.app_address_secret = True
    elif is_ticked(app.get("share_contact_details_yes")):
        case_details.app_address_secret = False

    # 4. Respondent
    resp = data_json.get("respondent") or {}
    addr = resp.get("address") or {}
    
    case_details.respondent.first_name = resp.get("first_name", "")
    case_details.respondent.last_name = resp.get("last_name", "")
    case_details.respondent.address_building_and_street = addr.get("line1", "")
    case_details.respondent.address_second_line = addr.get("line2", "")
    case_details.respondent.address_town_or_city = addr.get("town", "")
    case_details.respondent.address_postcode = addr.get("postcode", "")
    case_details.respondent.gender=detect_gender(case_details.respondent.first_name)
    case_details.respondent.set_pronouns()

    # 5. Children
    case_details.children = []
    for child_json in data_json.get("children", []):
        full_name = (child_json.get("name") or "").strip()
        dob_string = (child_json.get("dob") or "").strip()
        try:
            dob_object = datetime.strptime(dob_string, "%d/%m/%Y").date()
        except ValueError:
            dob_object = None

        parts = full_name.split()
        first = parts[0] if parts else ""
        last = parts[-1] if len(parts) > 1 else ""

        # The extractor doesn't give the child's gender, so guess it from the first name
        child_gender = {"Male": "boy", "Female": "girl"}.get(detect_gender(first), "")
        child = Child(
        first_name=first,
        last_name=last,
        gender=child_gender,
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
