import classes.Person as Person
from classes.Person import Person
from classes.Child import Child
import json
from datetime import datetime
import utils.Lists_Dictionaries as Lists_Dictionaries
from utils.Lists_Dictionaries import notice_values




class CaseDetails:
    _instance=None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance=super(CaseDetails,cls).__new__(cls)
            return cls._instance
        else:
            return cls._instance
    
    
    def __init__(self):
        
        if not hasattr(self,'_initialized'):
            
            self._initialized =True
            self.children =[]
            self.relationship='Marriage'
            self.court_name = 0
            self.case_name=""
            self.judge_name = "Jane Campbell"
            self.judge_rank="Deputy District Judge"
            self.file_name=""
            self.judge_gender="Female"
            self.case_number =""
            self.hearing_date=""
            self.app_address_secret = True
            self.hearing_date_object=datetime.now()
            self.listed_for="Interim Hearing"
            self.molestation_order =False
            self.occupation_order = False
            self.para_numbers=[]
            self.consent_order =False
            self.notice="On Notice"
            self.reasons=""
            self.judge_and_hearing=""
            self.applicant = Person('Applicant')
            self.app_rep=Person("Applicant's Representative")
            self.resp_rep=Person("Respondent's Representative")
            self.respondent=Person('Respondent')
            self.statements_read=[]
            self.parties=[]
            self.children=[]
            self.family_home_building_and_street=""
            self.family_home_address_second_line=""
            self.family_home_address_town_or_city=""
            self.family_home_postcode=""
            self.definitions=[]
            self.recitals=[]
            self.undertakings=[]
            self.order_choices=[]
            self.directions=[]
            self.orders=[]
            self.order_last=""
            self.effective=""
            self.application_values=[]
            self.notice_index=0
            self.notice_string=''
            self.application =''
   
    def name_file(self):
        A = self.applicant.last_name  
        R=self.respondent.last_name
        N=self.case_number
        self.file_name=f"{A} v {R} {N}"  
        
            
    def reset(self):
        self.children =[]
        self.relationship="Marriage"
        self.court_name = 0
        self.case_name=""
        self.judge_name = ""
        self.judge_rank=0
        self.case_number =""
        self.hearing_date_object=datetime.now()
        self.listed_for=0
        self.application=0
        self.para_numbers=[]
        self.consent_order =False
        self.notice=''
        self.reasons=0
        self.listed_for=0
        self.judge_and_hearing=""
        self.applicant = Person('Applicant')
        self.app_rep=Person("Applicant's Representative")
        self.resp_rep=Person("Respondent's Representative")
        self.respondent=Person('Respondent')
        self.parties.clear()
        self.children.clear()
        self.definitions.clear()
        self.recitals.clear()
        self.undertakings.clear()
        self.orders.clear()
        self.order_last=""
        self.effective=""
        self.applications_names=['Occupation Order','Non-Molestation Order','Occupation & Non-Molestation Orders']
        
   
    def update_from_dict(self,data):
        self.court_name=data.get('court_name',self.court_name)
        self.case_number = data.get("case_number", self.case_number)
        if "applicant_first_name" in data:
            self.applicant.first_name = data["applicant_first_name"]       
        if "applicant_last_name" in data:
            self.applicant.last_name = data["applicant_last_name"]
        if "respondent_first_name" in data:
            self.respondent.first_name = data["respondent_first_name"]
        if "respondent_last_name" in data:
            self.respondent.last_name = data["respondent_last_name"]
            
        pass
    
        
    def load_from_json(self, data):

    # --- CASE DETAILS ---
        case = data.get("case", {})
        self.court_name = case.get("court_name", "")
        self.case_number = case.get("case_number", "")
        self.relationship = case.get("relationship", "")
        self.judge_rank = case.get("judge_rank", "")
        self.judge_name = case.get("judge_name", "")
        self.judge_gender = case.get("judge_gender", "")

    # Application type → set booleans
        app_type = case.get("application_type", "")
        self.molestation_order = "Molestation" in app_type
        self.occupation_order = "Occupation" in app_type

    # --- APPLICANT ---
        applicant = data.get("applicant", {})
        self.applicant.first_name = applicant.get("first_name", "")
        self.applicant.last_name = applicant.get("last_name", "")
        self.applicant.dob = applicant.get("dob", "")
        self.applicant.gender = applicant.get("gender", "")

        addr = applicant.get("address", {})
        self.applicant.address_building_and_street = addr.get("line1", "")
        self.applicant.address_second_line = addr.get("line2", "")
        self.applicant.address_town_or_city = addr.get("town", "")
        self.applicant.address_postcode = addr.get("postcode", "")

    # --- RESPONDENT ---
        respondent = data.get("respondent", {})
        self.respondent.first_name = respondent.get("first_name", "")
        self.respondent.last_name = respondent.get("last_name", "")
        self.respondent.dob = respondent.get("dob", "")
        self.respondent.gender = respondent.get("gender", "")

        raddr = respondent.get("address", {})
        self.respondent.address_building_and_street = raddr.get("line1", "")
        self.respondent.address_second_line = raddr.get("line2", "")
        self.respondent.address_town_or_city = raddr.get("town", "")
        self.respondent.address_postcode = raddr.get("postcode", "")

    # --- CHILDREN ---
        self.children = []
        for child in data.get("children", []):
            dob_string = child.get("dob", "")
            dob_object = datetime.strptime(dob_string, "%Y-%m-%d").date()
            
            
            
            kid = Child(
            child.get("first_name", ""),
            "",  # last name (optional)
            "",  # gender (optional)
        dob_object
    )

        self.children.append(kid)

    # --- FAMILY HOME ---
        fh = data.get("family_home", {})
        self.family_home_building_and_street = fh.get("line1", "")
        self.family_home_address_second_line = fh.get("line2", "")
        self.family_home_address_town_or_city = fh.get("town", "")
        self.family_home_postcode = fh.get("postcode", "")

    # --- HEARING ---
        hearing = data.get("hearing", {})
        self.hearing_date = hearing.get("date", "")
        self.listed_for = hearing.get("type", "")
        self.notice = hearing.get("notice", "")
        self.hearing_time = hearing.get("time", "")

    # --- ORDERS REQUESTED ---
        orders = data.get("orders_requested", {})
        self.molestation_order = orders.get("non_molestation", False)
        self.occupation_order = orders.get("occupation", False)
        self.undertakings = orders.get("undertakings", False)

        
    def use_ai(self):
        data = {
    "case": {
        "court_name": "Brighton",
        "case_number": "BN23F01234",
        "application_type": "Non-Molestation Order",
        "relationship": "Marriage",
        "judge_rank": "District Judge",
        "judge_name": "Harrington",
        "judge_gender": "Male"
    },

    "applicant": {
        "first_name": "Emily",
        "last_name": "Turner",
        "address": {
            "line1": "14 Willow Close",
            "line2": "",
            "town": "Eastbourne",
            "postcode": "BN21 4AB"
        },
        "dob": "1987-03-12",
        "gender": "Female"
    },

    "respondent": {
        "first_name": "Daniel",
        "last_name": "Turner",
        "address": {
            "line1": "22 Marine Road",
            "line2": "Flat 3",
            "town": "Hailsham",
            "postcode": "BN27 1DP"
        },
        "dob": "1985-11-02",
        "gender": "Male"
    },

    "children": [
        {
            "first_name": "Sophie",
            "dob": "2015-06-21"
        },
        {
            "first_name": "Oliver",
            "dob": "2018-09-14"
        }
    ],

    "family_home": {
        "line1": "22 Marine Road",
        "line2": "Flat 3",
        "town": "Hailsham",
        "postcode": "BN27 1DP"
    },

    "hearing": {
        "date": "2026-05-20",
        "time": "10:00",
        "type": "Interim Hearing",
        "notice": "On Notice"
    },

    "orders_requested": {
        "non_molestation": True,
        "occupation": False,
        "undertakings": False
    }
}
           
       
        case = data.get("case", {})
        self.court_name = case.get("court_name", "")
        self.case_number = case.get("case_number", "")
        self.relationship = case.get("relationship", "")
        self.judge_rank = case.get("judge_rank", "")
        self.judge_name = case.get("judge_name", "")
        self.judge_gender = case.get("judge_gender", "")

    # Application type → set booleans
        app_type = case.get("application_type", "")
        self.molestation_order = "Molestation" in app_type
        self.occupation_order = "Occupation" in app_type

    # --- APPLICANT ---
        applicant = data.get("applicant", {})
        self.applicant.first_name = applicant.get("first_name", "")
        self.applicant.last_name = applicant.get("last_name", "")
        self.applicant.dob = applicant.get("dob", "")
        self.applicant.gender = applicant.get("gender", "")

        addr = applicant.get("address", {})
        self.applicant.address_building_and_street = addr.get("line1", "")
        self.applicant.address_second_line = addr.get("line2", "")
        self.applicant.address_town_or_city = addr.get("town", "")
        self.applicant.address_postcode = addr.get("postcode", "")

    # --- RESPONDENT ---
        respondent = data.get("respondent", {})
        self.respondent.first_name = respondent.get("first_name", "")
        self.respondent.last_name = respondent.get("last_name", "")
        self.respondent.dob = respondent.get("dob", "")
        self.respondent.gender = respondent.get("gender", "")

        raddr = respondent.get("address", {})
        self.respondent.address_building_and_street = raddr.get("line1", "")
        self.respondent.address_second_line = raddr.get("line2", "")
        self.respondent.address_town_or_city = raddr.get("town", "")
        self.respondent.address_postcode = raddr.get("postcode", "")

    # --- CHILDREN ---
        self.children = []
        for child in data.get("children", []):
            kid = Person("child")
            kid.first_name = child.get("first_name", "")
            kid.dob = child.get("dob", "")
            self.children.append(kid)

    # --- FAMILY HOME ---
        fh = data.get("family_home", {})
        self.family_home_building_and_street = fh.get("line1", "")
        self.family_home_address_second_line = fh.get("line2", "")
        self.family_home_address_town_or_city = fh.get("town", "")
        self.family_home_postcode = fh.get("postcode", "")

    # --- HEARING ---
        hearing = data.get("hearing", {})
        self.hearing_date = hearing.get("date", "")
        self.listed_for = hearing.get("type", "")
        self.notice = hearing.get("notice", "")
        self.hearing_time = hearing.get("time", "")

    # --- ORDERS REQUESTED ---
        orders = data.get("orders_requested", {})
        self.molestation_order = orders.get("non_molestation", False)
        self.occupation_order = orders.get("occupation", False)
        self.undertakings = orders.get("undertakings", False)
    
    def update_bottom_frame_width(self,event=None):
        self.bottom_frame.place_configure(width=self.winfo_width())
        
    def new_case(self):
        if self.case_details:
            self.case_details.reset()
            self.front_step()
            
   
    
    def to_dict(self):
        return{
            'relationship': self.relationship,
            'court_name': self.court_name,
            'case_name': self.case_name,
            'judge_name': self.judge_name,
            'judge_rank': self.judge_rank,
            'case_number': self.case_number,
            'hearing_date': self.hearing_date_object.isoformat() if self.hearing_date_object else None,
            'listed_for': self.listed_for,
            'application': self.application,
            'para_numbers': self.para_numbers,
            'consent_order': self.consent_order,
            'notice': self.notice,
            'reasons': self.reasons,
            'judge_and_hearing': self.judge_and_hearing,
            'applicant': self.applicant.to_dict(),
            'app_rep': self.app_rep.to_dict(),
            'resp_rep': self.resp_rep.to_dict(),
            'respondent': self.respondent.to_dict(),
            'parties': [party.to_dict() for party in self.parties],
            'children': [child.to_dict() for child in self.children],
            'definitions': self.definitions,
            'recitals': self.recitals,
            'undertakings': self.undertakings,
            'orders': self.orders,
            'order_last': self.order_last,
            'effective': self.effective
            
            
        }
        

   