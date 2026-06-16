from datetime import date
from datetime import datetime

class Person:
    def __init__(self, party):
        self.party = party
        self.title=""
        self.first_name = ""
        self.last_name = ""
        self.full_name=""
        self.gender = 0
        self.date_of_birth = None
        self.full_date_of_birth=''
        self.sentence=''
        self.dob=None
        self.dob_object=None
        self.dob_MM = 0
        self.dob_YYYY = 0
        self.dob_day=''
        self.dob_month=''
        self.dob_year=''
        self.father=''
        self.mother=''
        self.school=''
        self.lives_with=''
        self.address_building_and_street = ""
        self.address_second_line = ""
        self.address_town_or_city = ""
        self.address_postcode = ""
        self.short_address=""
        self.full_address=""
        self.phone = ""
        self.party=party
        self.nominative=""
        self.accusative=""
        self.possessive=""
        
        

    
        
        
        
        self.set_pronouns()
        
        
        
        

        
    def to_dict(self):
        return {
        "first_name": self.first_name,
        "last_name": self.last_name,
        "full_name": self.full_name,
        "gender": self.gender,
        "date_of_birth": self.date_of_birth,
        "full_date_of_birth": self.full_date_of_birth,
        "sentence": self.sentence,
        "dob": self.dob,
        "dob_object": self.dob_object,
        "dob_day": self.dob_day,
        "dob_month": self.dob_month,
        "dob_year": self.dob_year,
        "mother": self.mother,
        "father": self.father,
        "school": self.school,
        "lives_with": self.lives_with,
        "nominative": self.nominative,
        "accusative": self.accusative,
        "possessive": self.possessive
        
        }
    
    def set_date_of_birth(self, year, month, day):
        self.date_of_birth = date(year, month, day)
        
    def set_pronouns(self):
        self.s_p(self.gender)
        
    def s_p(self,gender):
        gender=self.gender
        if gender=="Male":
            self.nominative = "he"
            self.accusative="him"
            self.possessive='his'
        else:
            self.nominative='she'
            self.accusative='her'
            self.possessive='her'
            
    
    def set_full_name(self):
        if self.party=='Applicant' or self.party=='Respondent':

            self.full_name=f"{self.first_name} {self.last_name}"
        else:
            self.full_name=f"{self.title} {self.last_name}"
            tip='tap'
        
        
        
    def set_family_home(self):
        full_address = f" {self.address_building_and_street}, {self.address_second_line}, {self.address_town_or_city}, {self.address_postcode}"
        self.full_address=full_address
        self.short_address= self.address_building_and_street
        
    
        
class Child:
    def __init__(self,name1,name2,gender,birthday_object):
        self.first_name = name1
        self.last_name = name2
        self.full_name=name1 =""
        self.gender = gender
        self.date_of_birth = None
        self.full_date_of_birth=''
        self.sentence=''
        self.birthday_object=birthday_object
        self.dob_day=0
        self.dob_month = 0
        self.dob_year = 0
        self.mother=""
        self.father=""
        self.school=""
        self.lives_with=""
       
        self.nominative=""
        self.accusative=""
        self.possessive=""
        if self.gender=='boy':
            self.nominative='he'
            self.accusative='him'
            self.possessive=='his'
        else:
            self.nominative='she'
            self.accusative='her'
            self.possessive=='her'
        try:
            self.full_date_of_birth=self.birthday_object.strftime('%d %b %Y')
        except ValueError:
            self.full_date_of_birth='[    ]'

       
            self.sentence=f"{self.full_name} a {self.gender} born on {self.full_date_of_birth}."
            
        else:
            self.sentence=f"{self.full_name} a {self.gender} born on {self.full_date_of_birth}"
            
    def to_dict(self):
            return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth,
            "full_date_of_birth": self.full_date_of_birth,
            "sentence": self.sentence,
            "dob": self.dob,
            "dob_object": self.dob_object.isoformat() if self.dob_object else None,
            "dob_day": self.dob_day,
            "dob_month": self.dob_month,
            "dob_year": self.dob_year,
            "mother": self.mother,
            "father": self.father,
            "school": self.school,
            "lives_with": self.lives_with,
            "nominative": self.nominative,
            "accusative": self.accusative,
            "possessive": self.possessive,
        }
        
       
            
            
            

            
            
             
             
