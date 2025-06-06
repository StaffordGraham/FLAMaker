import Person
from Person import Person
import json
from datetime import datetime
import Lists_Dictionaries
from Lists_Dictionaries import notice_values




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
            self.judge_name = "Campbell"
            self.judge_rank="Deputy District Judge"
            self.file_name=""
            self.judge_gender="Male"
            self.case_number =""
            self.hearing_date=""
            self.app_address_secret = True
            self.hearing_date_object=datetime.now()
            self.listed_for="Interim Hearing"
            self.application="Occupation Order"
            self.para_numbers=[]
            self.consent_order =False
            self.notice="On Notice"
            self.reasons="Urgency"
            self.judge_and_hearing=""
            self.applicant = Person('Applicant')
            self.app_rep=Person("Applicant's Representative")
            self.resp_rep=Person("Respondent's Representative")
            self.respondent=Person('Respondent')
            self.statements_read=[]
            self.parties=[]
            self.children=[]
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
        
   
        
    
        
    def load_from_json(self,filename):
        with open(filename,'r') as file:
            data=json.load(file)
        for key,value in data.items():
            if hasattr(self,key):
                setattr(self,key,value)
                
        #print(self.__dict__)
            
            
        # Add any other relevant attributes you'd like to track
        
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
        

   