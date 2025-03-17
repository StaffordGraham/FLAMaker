import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from Person import Person
from Person import Child
from CaseDetails import CaseDetails
from datetime import datetime
from tkcalendar import DateEntry
import os
import subprocess
from docx import Document
from docx.oxml import OxmlElement
from docx.shared import Cm
#import create_order
from create_order import write_order
import functions
from functions import date_format
from tkcalendar import DateEntry
from tkinter import filedialog
import json
import Lists_Dictionaries
from Lists_Dictionaries import titles,kid_genders,days,months,years,notice_values
import create_order
import pprint
import pickle

import sys
case_details=CaseDetails()
applicant =Person
respondent = Person
standard_orders_only=True





#FONTS & STYLES
BACKGROUND_COLOUR="#FFFFCC"
FOREGROUND_COLOUR="#0000FF"
theFont=("Helvetica", 16)
bigFont=("Helvetica", 24)


             
         
test_run=True 


    


class BasePage(tk.Frame):
    def __init__(self,parent,controller,case_details):
        super().__init__(parent)
        self.controller=controller
        self.case_details=case_details
         
    def next_page(self):
        if self.controller.current_page_index+1<len(self.pages):
            self.controller.current_page_index +=1
            self.controller.show_frame(self.pages[self.current_page_index].__name__)
            
    def last_page(self):
        if self.controller.current_page_index >0:
            self.controller.current_page_index-=1
            self.controller.show_frame(self.controller.pages[self.controller.current_page_index].__name__)



class MultiPage(tk.Tk):
    def __init__(self):
        super().__init__()
        style=ttk.Style()
        style.theme_use('winnative')
        self.pages=[Case]
        self.title("FlAgpole")
        self.geometry("880x550")
        self.container=ttk.Frame(self)
        self.container.pack(fill='both',expand=True)
        if standard_orders_only==True:
            self.pages=[Start,Case,all_Orders,Applicant,Respondent,Children,Hearing,Duration, Actions]
        else:
            self.pages=[Start,Case,NonMols,OccOrders,Applicant,Respondent,Children,Hearing,Duration, Actions]
        self.current_page_index=0


        self.frames={}
        
        for F in self.pages:
            page_name=F.__name__
            if F==Case:
                #frame=F(parent=self.container,controller=self,case_details=self.case_info)
                frame=F(parent=self.container,controller=self,case_details=case_details)

                
            else:
                frame = F(parent=self.container, controller=self,case_details=case_details)  

            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')  # Ensure frame can expand   
            
        self.container.grid_rowconfigure(0, weight=1)  # Allow the first row to expand
        self.container.grid_columnconfigure(0, weight=1)  # Allow the first column to expand
        self.show_frame(self.pages[self.current_page_index].__name__)  # This displays the initial frame
        frame=self.frames[page_name]
        
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.on_show()

        frame.tkraise()  # Bring the frame to the front
     
   
             
             
             
        
     
    def next_page(self):
        while self.current_page_index+1<len(self.pages):
            self.current_page_index +=1
            temp_var = self.current_page_index
            next_page=self.pages[self.current_page_index]
            if next_page.__name__=='Undertakings' and case_details.notice !='On Notice':
                continue
            self.show_frame(self.pages[self.current_page_index].__name__)
            break
            
    def last_page(self):
        if self.current_page_index !=0:
            t= self.current_page_index
            self.current_page_index-=1
            t=self.current_page_index
            next_page=self.pages[self.current_page_index].__name__
            
            self.show_frame(next_page)
            
        
    def fill_widgets(self):
        pass
    
 
#HEADER

class Start(BasePage,tk.Frame):
    
    def __init__(self,parent,controller,case_details):
        super().__init__(parent,controller,case_details)
        tk.Frame.__init__(self,parent)
        self.controller=controller
        self.config(bg=BACKGROUND_COLOUR)    
        self.grid_columnconfigure(0,weight=1)
        self.widgets_list=[]
        self.row_no=1
		
#TITLE Frame

        self.top_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.top_frame.grid(row=0,column=0,sticky='ew')
        page_title=tk.Label(self.top_frame,text="Start Session",font=bigFont,bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.top_frame.grid_columnconfigure(0,weight=1)
        page_title.grid(row=self.row_no,column=0, padx=0,pady=10,sticky='ew')
		
#WIDGET Frame
	
        self.input_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.input_frame.grid(row=1,column=0,sticky='w')
        self.input_frame.grid_columnconfigure(0,weight=0)
        
        open_file_button=tk.Button(self.input_frame, text='Open File',command=self.file_open)
        open_file_button.config(background=FOREGROUND_COLOUR,fg=BACKGROUND_COLOUR)
        open_file_button.grid(row=self.row_no,column=1,padx=(10,10),pady=10,sticky='w')
        self.row_no+=1
        
        new_case_button=tk.Button(self.input_frame, text='New Case',command=self.new_case)
        new_case_button.config(background=FOREGROUND_COLOUR,fg=BACKGROUND_COLOUR)
        new_case_button.grid(row=self.row_no,column=1,padx=(10,10),pady=10,sticky='w')
        self.row_no+=1

#NEXT AND BACK BUTTON Frame

        self.bottom_frame=tk.Frame(self,bg=BACKGROUND_COLOUR,height=50)
        self.bottom_frame.place(relx=0.5,rely=1.0,anchor='s',y=-20)
        self.bind("<Configure>", self.update_bottom_frame_width)  # Bind resize event

        back_button=tk.Button(self.bottom_frame,text="Back",command=self.back_step)
        next_button =tk.Button(self.bottom_frame, text="Next",command=self.front_step)
        back_button.grid(row=1,column=0,padx=10,pady=(0,10),sticky='w')
        next_button.grid(row=1,column=1,padx=10,pady=(0,10), sticky='e')
        self.bottom_frame.grid_columnconfigure(0,weight =1)
        self.bottom_frame.grid_columnconfigure(1,weight=1)

#FUNCTIONS

    def update_bottom_frame_width(self,event=None):
        self.bottom_frame.place_configure(width=self.winfo_width())
        
    def new_case(self):
        
        if self.case_details:
            self.case_details.reset()
            self.front_step()
            
        
   
        
    def file_open(self):
        
        try:
            if case_details is not None:
                del case_details            
        except NameError:
            
            pass
        
        filepath =self.open_file_dialog()
    
        if filepath:
            with open (filepath,'rb') as file:
              case_details=pickle.load(file)
            
        self.front_step()
            
        
        
        
    def open_file_dialog(self):
        root=tk.Tk()
        root.withdraw()
        filepath=filedialog.askopenfilename(
            title="Select File",
            filetypes=[("SAP Files","*.ord"),("All Files","*.*")]
        )
        return filepath
    
    
        
    def on_show(self):
        p = case_details.case_name
        pass

    def update():
        pass

    def back_step(self):
        #self.update(self.controller)
        self.controller.last_page()

    def front_step(self):
        #self.update(self.controller)
        self.controller.next_page()


		
		
           
        
    
            

class Case (BasePage,tk.Frame):
    def __init__(self,parent,controller,case_details):
        tk.Frame.__init__(self,parent)

        super().__init__(parent,controller,case_details)
        self.child_count=0
        self.input_controls =[]
        applications=['Occupation Order','Non-Molestation Order','Occupation & Non-Molestation Orders']
        self.row_no = 0
        self.check_var = True
        


        self.config(bg=BACKGROUND_COLOUR)
        self.grid(sticky='nsew')
        self.grid_columnconfigure(0,weight=1)
        
        #THE FRAME SHOWING THE PAGE TITLE
        
        self.top_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.top_frame.grid(row=0,column=0,sticky='ew')
        page_title=tk.Label(self.top_frame,text="The Case ",font=bigFont,bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.top_frame.grid_columnconfigure(0,weight=1)
        page_title.grid(row=self.row_no,column=0, padx=0,pady=10,sticky='ew')
        self.top_frame.bind("<Double-1>",self.on_double_click)


        self.row_no+=1
        
        
       
       
        #THE FRAME CONTAINING THE INPUT WIDGETS
        self.row_no +=1
        
        
        #THE COURT
        court_options = ["Brighton", "Medway","Hastings", "Horsham", "Worthing", "Guildford", "Croydon", "Kingston"]
        label_court = tk.Label(self, text="Court:", font=theFont,anchor='w')
        label_court.config(bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR)
        label_court.grid(row=self.row_no, column=0, padx=(2,5), pady=10, sticky='e')
        self.combo_court_name =ttk.Combobox(self,values=court_options,style="Custom.TCombobox",width=20)
        self.combo_court_name.config(background='white')
        self.combo_court_name.grid(row=self.row_no,column=1,padx=(5,0),pady=10,sticky='w')
        self.grid_columnconfigure(0,weight=0)
        self.grid_columnconfigure(1, weight=1)
        #self.combo_court_name.config(relief="solid")         
        
        self.row_no +=1
        
        
         #THE CASE NUMBER
        
        case_number_lbl =tk.Label(self,text="Case Number",font=('Helvetica',12),anchor='e',width=20)
        case_number_lbl.config(bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR)

        case_number_lbl.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='e')
        self.entry_case_number =tk.Entry(self,background="white",fg="green")
        self.entry_case_number.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        #self.entry_case_number.insert(0,'ME F240089')
        self.row_no +=1
        
        #THE APPLICATION
        application_label=tk.Label(self,text='Application Made',font=('Helvetica',12),anchor='e',width=20)
        application_label.config(bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR)
        application_label.grid(row=self.row_no,column=0,padx=(10,10),pady=10,sticky='e')
        self.combo_application=ttk.Combobox(self,values=applications,style="Custom.TCombobox")
        self.combo_application.grid(row=self.row_no,column=1,padx=(10,10),pady=10,sticky='w')
        self.row_no +=1
        
        #THE RELATIONSHIP
        rel_values =["Marriage","Civil Partnership","Cohabitee","Intimate Significant Duration"]
        relat_lbl=tk.Label(self,text="Marriage/Civil Partnership",font=('Helvetica',12),anchor='e',width=20)
        relat_lbl.config(background=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        relat_lbl.grid(row=self.row_no,column=0,padx=(10,10),pady=(1),sticky='w')
        self.relat_combo=ttk.Combobox(self,values=rel_values,style="Custom.TCombobox")
        self.relat_combo.grid(row=self.row_no,column=1,padx=(10,10),pady=10,sticky='w')
        self.row_no+=1
        
        
       
        self.row_no+=1
        
        
        
          #THE JUDGE TITLE
        judge_options=["District Judge","Deputy District Judge","Recorder","Circuit Judge","High Court Judge","Deputy High Court Judge"]
        label_judge_title=tk.Label(self, text="Judge Title", font=theFont,anchor='e')
        label_judge_title.config(bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR)
        label_judge_title.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')

        self.combo_judge_rank= ttk.Combobox(self, values=judge_options,style='Custom.TCombobox')
        self.combo_judge_rank.set("Deputy District Judge")
        self.combo_judge_rank.grid(row=self.row_no,column=1,padx=10,pady=(10),sticky='w')
        
        self.row_no +=1
                

        #THE JUDGE NAME
        self.label_judge_name =tk.Label(self,text="Judge Name",anchor='e',font=theFont)
        self.label_judge_name.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.label_judge_name.config(bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR)
        self.entry_judge_name=tk.Entry(self,background=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.entry_judge_name.config(background="White",fg=FOREGROUND_COLOUR)
        self.entry_judge_name.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no +=1
        
        #THE JUDGE GENDER
        label_judge_gender=tk.Label(self, text="Judge Gender",font=theFont)
        label_judge_gender.config(bg=BACKGROUND_COLOUR, fg=FOREGROUND_COLOUR)
        label_judge_gender.grid(row=self.row_no,column=0,padx=(10,10),pady=10,sticky='w')
        self.combo_judge_gender=ttk.Combobox(self,values =('Male','Female'),style='Custom.TCombobox')
        self.combo_judge_gender.grid(row=self.row_no,column=1,padx=(10,10),pady=10,sticky='w')
        
        
        
        
        
        
        
       #To be put in 
        
        #THE FRAME FOR THE NEXT AND BACK BUTTONS WITH RELATED FUNCTION
        
        self.bottom_frame=tk.Frame(self,bg=BACKGROUND_COLOUR,height=50)
        self.bottom_frame.place(relx=0.5,rely=1.0,anchor='s',y=-20)
        self.bind("<Configure>", self.update_bottom_frame_width)  # Bind resize event
        #self.update_bottom_frame_width()
       

        back_button=tk.Button(self.bottom_frame,text="Back",command=self.last_action)
        next_button =tk.Button(self.bottom_frame, text="Next",command=self.next_action)
        back_button.grid(row=1,column=0,padx=10,pady=(0,10),sticky='w')
        next_button.grid(row=1,column=1,padx=10,pady=(0,10), sticky='e')
        self.bottom_frame.grid_columnconfigure(0,weight =1)
        self.bottom_frame.grid_columnconfigure(1,weight=1)
        self.bottom_frame.bind("<Double-1>",self.on_double_click)
        self.fill_widgets()
        
    def on_double_click(self,event):
        self.fill_widgets()
        
    def app_secret():
        pass
    
    def on_show(self):
        if case_details.judge_rank:
            self.combo_judge_rank=case_details.judge_rank
        else:
            self.combo_judge_rank="Deputy District Judge"
        if case_details.judge_gender:
            self.combo_judge_gender=case_details.judge_gender
        else:
            self.combo_judge_gender="Male"
        if case_details.judge_name:
            self.entry_judge_name=case_details.judge_name
        else:
            self.entry_judge_name="Compbell"
            
        if case_details.case_number:
            self.entry_case_number=case_details.case_number
        else:
            self.entry_case_number="ME 25 0924"
        
    def update_bottom_frame_width(self,event=None):
       self.bottom_frame.place_configure(width=self.winfo_width())
       
 
    def on_double_click(self,event):
        pass
            
    def update(self):

        
        case_details.court_name=self.combo_court_name.get()
        case_details.case_number=self.entry_case_number.get()
        case_details.judge_rank=self.combo_judge_rank.get()
        case_details.judge_name=self.entry_judge_name.get()
        case_details.relationship=self.relat_combo.get()
        case_details.application=self.combo_application.get()
        case_details.judge_rank=self.combo_judge_rank.get()
        case_details.judge_gender=self.combo_judge_gender.get()
            

        
        
        

        
        
        
    def last_action(self):
            self.update()
            self.controller.last_page()
            
    def next_action(self):
            self.update()
            self.controller.next_page()
            
    def fill_widgets(self):
        test_run=True
        if test_run==True:
            self.combo_application.set('Occupation Order')
            self.combo_court_name.set('Medway')
            self.entry_case_number.insert(0,'ME F240089')
            self.relat_combo.set('Marriage')
            self.combo_judge_rank.set('Deputy District Judge')
            self.entry_judge_name.insert(0,'Campbell')
            
    def on_show(self):
            if case_details.application ==0:
                self.combo_application.set(self.combo_application['values'][0])
            else:
                self.combo_application.set(case_details.application)
                
            if case_details.court_name==0:
                self.combo_court_name.set(self.combo_court_name['values'][0])
            else:
                self.combo_court_name.set(case_details.court_name)
                
            self.entry_case_number.delete(0,'end')
            self.entry_case_number.insert(0,case_details.case_number)
            
            self.relat_combo.set(case_details.relationship)
            self.combo_judge_rank.set(case_details.judge_rank)
            self.entry_judge_name.delete(0,'end')
            self.entry_judge_name.insert(0,case_details.judge_name)
            self.combo_judge_gender.set(case_details.judge_gender)
            
            
class Property (BasePage,tk.Frame):
    def __init__(self,parent,controller,case_details):
        super().__init__(parent,controller,case_details)
        tk.Frame.__init__(self,parent)
        self.case_details=case_details
        self.controller=controller
        self.config(bg=BACKGROUND_COLOUR)    
        self.grid_columnconfigure(0,weight=1)
        self.widgets_list=[]
        self.row_no=1
		
#TITLE Frame
        self.top_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.top_frame.grid(row=0,column=0,sticky='ew')
        page_title=tk.Label(self.top_frame,text="The Property ",font=bigFont,bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.top_frame.grid_columnconfigure(0,weight=1)
        page_title.grid(row=self.row_no,column=0, padx=0,pady=10,sticky='ew')
		
#WIDGET Frame
	
        self.input_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.input_frame.grid(row=1,column=0,sticky='w')
        self.input_frame.grid_columnconfigure(0,weight=0)
        
        self.add1_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no+=1
        self.add2_label=tk.Label(self.input_frame,text="Address 2", font=("Helvetica",12))
        self.add2_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.add2_entry =tk.Entry(self.input_frame,background="white",fg=FOREGROUND_COLOUR)
        self.applicant_widgets.append(self.add2_entry)
        self.add2_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.add2_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no+=1
        #Town/City
        town_label=tk.Label(self.input_frame,text="Town/City", font=("Helvetica",12))
        town_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.town_entry =tk.Entry(self.input_frame,background="white",fg=FOREGROUND_COLOUR)
        self.applicant_widgets.append(self.town_entry)
        town_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.town_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no+=1
        
        #PostCode
        postcode_label=tk.Label(self.input_frame,text="Post Code", font=("Helvetica",12))
        postcode_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.postcode_entry =tk.Entry(self.input_frame,background="white",fg=FOREGROUND_COLOUR)
        self.applicant_widgets.append(self.postcode_entry)
        postcode_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.postcode_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.check_var=tk.IntVar()


#NEXT AND BACK BUTTON Frame

        self.bottom_frame=tk.Frame(self,bg=BACKGROUND_COLOUR,height=50)
        self.bottom_frame.place(relx=0.5,rely=1.0,anchor='s',y=-20)
        self.bind("<Configure>", self.update_bottom_frame_width)  # Bind resize event

        back_button=tk.Button(self.bottom_frame,text="Back",command=self.back_step)
        next_button =tk.Button(self.bottom_frame, text="Next",command=self.front_step)
        back_button.grid(row=1,column=0,padx=10,pady=(0,10),sticky='w')
        next_button.grid(row=1,column=1,padx=10,pady=(0,10), sticky='e')
        self.bottom_frame.grid_columnconfigure(0,weight =1)
        self.bottom_frame.grid_columnconfigure(1,weight=1)

#FUNCTIONS

    def update_bottom_frame_width(self,event=None):
            self.bottom_frame.place_configure(width=self.winfo_width())
        

    def on_show(self):
            pass

    def update(self):
            pass

    def back_step(self):
            self.update(self)
            self.controller.last_page()

    def front_step(self):
        self.update(self)
        self.controller.next_page()

            

        
            

        
    
            
   
class Applicant(BasePage,tk.Frame):
    
    def __init__(self,parent,controller,case_details):
        
        super().__init__(parent,controller,case_details)
        tk.Frame.__init__(self,parent)
        tk.Frame.__init__(self,parent)
        self.controller=controller
        self.config(bg=BACKGROUND_COLOUR)
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        self.grid_columnconfigure(0,weight=1)
        self.row_no=1
        #The Frame showing the Page Title
		
        self.top_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.top_frame.grid(row=0,column=0,sticky='ew')
        page_title=tk.Label(self.top_frame,text="The Applicant ",font=bigFont,bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.top_frame.grid_columnconfigure(0,weight=1)
        page_title.grid(row=self.row_no,column=0, padx=0,pady=10,sticky='ew')
        
        #FRAME SHOWING WIDGETS
        #THE FRAME CONTAINING THE INPUT WIDGETS
        self.row_no+=1
        self.applicant_widgets=[]
        
        self.input_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.input_frame.grid(row=1,column=0,sticky='w')
        self.input_frame.grid_columnconfigure(0,weight=0)
        self.input_frame.bind("<Double-1>",self.on_double_click)
       
        self.row_no+=1
       
               
        
        self.row_no+=1
        label_title =tk.Label(self.input_frame,text="Title",font=("Helvetica",12))
        label_title.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        label_title.grid(row=self.row_no, column=0, padx=(10), pady=10, sticky='w')
        self.combo_title=ttk.Combobox(self.input_frame,values=["Mr","Miss","Mrs","Ms"],style="Custom.TCombobox")
        self.combo_title.set('Ms')
        self.combo_title.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='e')
        
        self.row_no +=1
        
        first_name_label=tk.Label(self.input_frame,text="First Name",font=("Helvetica",12))
        first_name_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.first_name_entry=tk.Entry(self.input_frame,background='white',fg=FOREGROUND_COLOUR)
        self.applicant_widgets.append(self.first_name_entry)
        first_name_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.first_name_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no+=1

        surname_label=tk.Label(self.input_frame,text="Surname",font=("Helvetica",12))
        surname_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.surname_entry=tk.Entry(self.input_frame,background="white",fg=FOREGROUND_COLOUR)
        self.applicant_widgets.append(self.surname_entry)
        surname_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.surname_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no +=1
        
        
        gender_label=tk.Label(self.input_frame,text="Gender",font=('Helvetica',12))
        gender_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.gender_combo=ttk.Combobox(self.input_frame,values=["Male","Female"],style="Custom.TCombobox")
        self.gender_combo.set('Female')
        self.applicant_widgets.append(self.gender_combo)
        gender_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.gender_combo.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.applicant_widgets.append(self.gender_combo)

        
        self.row_no+=1
        add1_label=tk.Label(self.input_frame,text="Address 1", font=("Helvetica",12))
        add1_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.add1_entry=tk.Entry(self.input_frame,background="white",fg=FOREGROUND_COLOUR)
        add1_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.applicant_widgets.append(self.add1_entry)

        self.add1_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no+=1
        self.add2_label=tk.Label(self.input_frame,text="Address 2", font=("Helvetica",12))
        self.add2_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.add2_entry =tk.Entry(self.input_frame,background="white",fg=FOREGROUND_COLOUR)
        self.applicant_widgets.append(self.add2_entry)
        self.add2_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.add2_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no+=1
            #Town/City
        town_label=tk.Label(self.input_frame,text="Town/City", font=("Helvetica",12))
        town_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.town_entry =tk.Entry(self.input_frame,background="white",fg=FOREGROUND_COLOUR)
        self.applicant_widgets.append(self.town_entry)
        town_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.town_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no+=1
            
            #PostCode
        postcode_label=tk.Label(self.input_frame,text="Post Code", font=("Helvetica",12))
        postcode_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.postcode_entry =tk.Entry(self.input_frame,background="white",fg=FOREGROUND_COLOUR)
        self.applicant_widgets.append(self.postcode_entry)
        postcode_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.postcode_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.check_var=tk.IntVar()

       
       
       
      
        
         #THE FRAME FOR THE NEXT AND BACK BUTTONS WITH RELATED FUNCTION -CHILDREN
        
        self.bottom_frame=tk.Frame(self,bg=BACKGROUND_COLOUR,height=50)
        self.bottom_frame.place(relx=0.5,rely=1.0,anchor='s',y=-20)
        self.bind("<Configure>", self.update_bottom_frame_width)  # Bind resize event
        #self.update_bottom_frame_width()
       
        #NEXT AND BACK BUTTONS CHILDREN
        back_button=tk.Button(self.bottom_frame,text="Back",command=self.last_action)
        next_button =tk.Button(self.bottom_frame, text="Next",command=self.next_action)
        back_button.grid(row=1,column=0,padx=10,pady=(0,10),sticky='w')
        next_button.grid(row=1,column=1,padx=10,pady=(0,10), sticky='e')
        self.bottom_frame.grid_columnconfigure(0,weight =1)
        self.bottom_frame.grid_columnconfigure(1,weight=1)
        
    def on_show(self):
        if case_details.applicant.title=='':
            self.combo_title.set('Ms')
            self.gender_combo.set('Female')
        else:
            self.combo_title.set(case_details.applicant.title)
            self.gender_combo.set(case_details.applicant.gender)
            
        self.first_name_entry.delete(0,'end')
        self.first_name_entry.insert(0,case_details.applicant.first_name)
        self.surname_entry.delete(0,'end')
        self.surname_entry.insert(0,case_details.applicant.last_name)
        self.add1_entry.delete(0,'end')
        self.add1_entry.insert(0,case_details.applicant.address_building_and_street)
        self.add2_entry.delete(0,'end')
        self.add2_entry.insert(0,case_details.applicant.address_second_line)
        self.town_entry.delete(0,'end')
        self.town_entry.insert(0,case_details.applicant.address_town_or_city)
        self.postcode_entry.delete(0,'end')
        self.postcode_entry.insert(0,case_details.applicant.address_postcode)
       
       
       
       

    def on_double_click(self,event):
        self.fill_widgets()
    def fill_widgets(self):
        if test_run==True:
            for widget in self.applicant_widgets:
                if isinstance(widget,tk.Entry):
                    widget.delete(0,tk.END)

            
            self.combo_title.set('Mrs')
            self.first_name_entry.delete(0,tk.END)
            
            self.first_name_entry.insert(0,'Angela')
            self.surname_entry.insert(0,'Ashes')
            self.gender_combo.set('Female')

            self.add1_entry.insert(0,'20 Petersen Gardens')
            self.add2_entry.insert(0,'Tonbridge')
            self.town_entry.insert(0,'Kent')
            self.postcode_entry.insert(0,'PN3 0H5')
            
        
    def update_bottom_frame_width(self,event=None):
       self.bottom_frame.place_configure(width=self.winfo_width())
        
    def last_action(self):
            self.update(self.controller)
            tempo='tempo'
            self.controller.last_page()
            
    def next_action(self):
            self.update(self.controller)
            self.controller.next_page()
        
        
        
    def update(self,controller):
        case_details.applicant.title=self.combo_title.get()
        name1=self.first_name_entry.get()
        name2=self.surname_entry.get()
        full_name=f"{name1} {name2}"
        case_details.applicant.first_name=name1
        case_details.applicant.last_name=name2
        case_details.applicant.full_name=full_name
        
        case_details.applicant.full_name=case_details.applicant.first_name +" "+case_details.applicant.last_name
        case_details.applicant.gender=self.gender_combo.get()
        case_details.applicant.address_building_and_street=self.add1_entry.get()
        case_details.applicant.address_second_line=self.add2_entry.get()
        case_details.applicant.address_town_or_city=self.town_entry.get()
        case_details.applicant.address_postcode=self.postcode_entry.get()
        
        case_details.applicant.set_pronouns()
        case_details.applicant.set_full_name()
        case_details.applicant.set_family_home()
        temp_var=self.check_var.get()
        if temp_var==1:
            par_var = (f" The 'family home' is the property at {case_details.applicant.address_building_and_street}, "
            f"{case_details.applicant.address_second_line}, "
            f"{case_details.applicant.address_town_or_city}, " 
            f"{case_details.applicant.address_postcode}")
            case_details.definitions.append(par_var)
            temp_var3=case_details.definitions[0]
            temp_var3=temp_var3
            
            
            
            

        
        
        
        
        
        
       
        
        
        
        
class Respondent(BasePage,tk.Frame):
    def __init__(self,parent,controller,case_details):
        
        super().__init__(parent,controller,case_details)
        tk.Frame.__init__(self,parent)
        tk.Frame.__init__(self,parent)
        self.config(bg=BACKGROUND_COLOUR)
        
        self.grid(sticky='nsew')
        self.grid_columnconfigure(0,weight=1)
        self.row_no=1
        self.respondent_widgets=[]
        #The Frame showing the Page Title
		
        self.top_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.top_frame.grid(row=0,column=0,sticky='ew')
        page_title=tk.Label(self.top_frame,text="The Respondent ",font=bigFont,bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.top_frame.grid_columnconfigure(0,weight=1)
        page_title.grid(row=self.row_no,column=0,columnspan=3, padx=0,pady=10,sticky='ew')
        
        #FRAME SHOWING WIDGETS
        #THE FRAME CONTAINING THE INPUT WIDGETS
        
        self.widget_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.widget_frame.grid(row=1,column=0,sticky='nsew')
        self.widget_frame.grid_columnconfigure(0,weight=0)
        self.widget_frame.bind("<Double-1>",self.on_double_click)
        
        
        
        
        
        
        self.row_no=1
        label_title =tk.Label(self.widget_frame,text="Title",font=("Helvetica",12))
        label_title.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        label_title.grid(row=self.row_no, column=0, padx=(10), pady=10, sticky='w')
        self.combo_title=ttk.Combobox(self.widget_frame,values=["Mr","Miss","Mrs","Ms"],style="Custom.TCombobox")
        self.combo_title.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='e')
        self.row_no +=1
        
        first_name_label=tk.Label(self.widget_frame,text="First Name",font=("Helvetica",12))
        first_name_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.first_name_entry=tk.Entry(self.widget_frame,background='white',fg=FOREGROUND_COLOUR)
        first_name_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.respondent_widgets.append(self.first_name_entry)
        self.first_name_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no+=1

        surname_label=tk.Label(self.widget_frame,text="Surname",font=("Helvetica",12))
        surname_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.surname_entry=tk.Entry(self.widget_frame,background="white",fg=FOREGROUND_COLOUR)
        surname_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.respondent_widgets.append(self.surname_entry)
        self.surname_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no +=1
        gender_label=tk.Label(self.widget_frame,text="Gender",font=('Helvetica',12))
        gender_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.gender_combo=ttk.Combobox(self.widget_frame,values=["Male","Female"],style="Custom.TCombobox")
        self.respondent_widgets.append(self.gender_combo)
        gender_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.gender_combo.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no+=1
        add1_label=tk.Label(self.widget_frame,text="Address 1", font=("Helvetica",12))
        add1_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.add1_entry=tk.Entry(self.widget_frame,background="white",fg=FOREGROUND_COLOUR)
        add1_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.respondent_widgets.append(self.add1_entry)
        self.add1_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no+=1
        self.add2_label=tk.Label(self.widget_frame,text="Address 2", font=("Helvetica",12))
        self.add2_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.add2_entry =tk.Entry(self.widget_frame,background="white",fg=FOREGROUND_COLOUR)
        self.respondent_widgets.append(self.add2_entry)
        self.add2_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.add2_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no+=1
        #Town/City
        town_label=tk.Label(self.widget_frame,text="Town/City", font=("Helvetica",12))
        town_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.town_entry =tk.Entry(self.widget_frame,background="white",fg=FOREGROUND_COLOUR)
        self.respondent_widgets.append(self.town_entry)
        town_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.town_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no+=1
        
        #PostCode
        postcode_label=tk.Label(self.widget_frame,text="Post Code", font=("Helvetica",12))
        postcode_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.postcode_entry =tk.Entry(self.widget_frame,background="white",fg=FOREGROUND_COLOUR)
        postcode_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.postcode_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.respondent_widgets.append(self.postcode_entry)
        self.row_no+=1
       
               
        #NEXT AND BACK BUTTONS
        
          #THE FRAME FOR THE NEXT AND BACK BUTTONS WITH RELATED FUNCTION -CHILDREN
        
        self.bottom_frame=tk.Frame(self,bg=BACKGROUND_COLOUR,height=50)
        self.bottom_frame.place(relx=0.5,rely=1.0,anchor='s',y=-20)
        self.bind("<Configure>", self.update_bottom_frame_width)  # Bind resize event
        #self.update_bottom_frame_width()
       
        #NEXT AND BACK BUTTONS CHILDREN
        back_button=tk.Button(self.bottom_frame,text="Back",command=self.last_action)
        next_button =tk.Button(self.bottom_frame, text="Next",command=self.next_action)
        back_button.grid(row=1,column=0,padx=10,pady=(0,10),sticky='w')
        next_button.grid(row=1,column=1,padx=10,pady=(0,10), sticky='e')
        self.bottom_frame.grid_columnconfigure(0,weight =1)
        self.bottom_frame.grid_columnconfigure(1,weight=1)
        #self.fill_widgets()
       
    def on_double_click(self,event):
        print ('in double click')
        self.fill_widgets()
        
   
    
    def on_show(self):
        if case_details.respondent.title=="":
            self.combo_title.set('Mr')
            self.gender_combo.set('Male')
        else:
            self.combo_title.set(case_details.respondent.title)
            self.gender_combo.set(case_details.respondent.gender)
        
        self.first_name_entry.delete(0,'end')
        if case_details.respondent.first_name:
            self.first_name_entry.insert(0,case_details.respondent.first_name)
        if case_details.respondent.last_name:
            self.surname_entry.delete(0,'end')
            self.surname_entry.insert(0,case_details.respondent.last_name)
        if case_details.respondent.address_building_and_street:
            self.add1_entry.delete(0,'end')
            self.add1_entry.insert(0,case_details.respondent.address_building_and_street)
        if case_details.respondent.address_second_line:
            self.add2_entry.delete(0,'end')
            self.add2_entry.insert(0,case_details.respondent.address_second_line)
            
        if case_details.respondent.address_town_or_city:
            self.town_entry.delete(0,'end')
            self.town_entry.insert(0,case_details.respondent.address_town_or_city)
        if case_details.respondent.address_postcode:
            self.postcode_entry.delete(0,'end')
            self.postcode_entry.insert(0,case_details.respondent.address_postcode)
    
    def fill_widgets(self):
        if test_run==True:
            for widget in self.respondent_widgets:
                if isinstance(widget,tk.Entry):
                    widget.delete(0,tk.END)
            self.combo_title.set('Mr')
            self.first_name_entry.insert(0,'Charles')
            self.surname_entry.insert(0,'Ashes')
            self.gender_combo.set('Male')

            self.add1_entry.insert(0,'The Bridges')
            self.add2_entry.insert(0,'Hailsham Lane')
            self.town_entry.insert(0,'East Sussex')
            self.postcode_entry.insert(0,'PNBN27 0J2')
            
        
    def update_bottom_frame_width(self,event=None):
       self.bottom_frame.place_configure(width=self.winfo_width())
        
    def last_action(self):
            self.update(self.controller)
            self.controller.last_page()
            
    def next_action(self):
            self.update(self.controller)
            self.controller.next_page()
        
        
        
    def update(self,controller):
       
        case_details.respondent.title=self.combo_title.get()
        case_details.respondent.first_name=self.first_name_entry.get() 
        case_details.respondent.last_name=self.surname_entry.get()
        case_details.respondent.gender=self.gender_combo.get()
        case_details.respondent.address_building_and_street=self.add1_entry.get()
        case_details.respondent.address_second_line=self.add2_entry.get()
        case_details.respondent.address_town_or_city=self.town_entry.get()
        case_details.respondent.address_postcode=self.postcode_entry.get()
        case_details.respondent.set_pronouns()
        case_details.respondent.set_full_name()
        
         
         
        
	
class Hearing(BasePage,tk.Frame):
    def __init__(self,parent,controller,case_details):
        
        super().__init__(parent,controller,case_details)
        tk.Frame.__init__(self,parent)
        self.case_details=case_details
        style=ttk.Style()
        self.config(bg=BACKGROUND_COLOUR)
        self.row_no =0
        self.notice_row_no=0
        self.grid(sticky='w')
        self.grid_columnconfigure(0,weight=0)
        
   
       
        listed_for_values=['Interim Hearing','Final Hearing','Directions Hearing']
        
        
        notices=['On Notice','Without Notice','On Short Notice']
        self.reasons=["","Urgency","Risk of harm","welfare of children","Frustrate order"]
        
		
		#THE FRAME SHOWING THE PAGE TITLE
        
        self.top_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.top_frame.grid(row=0,column=0,sticky='ew')
        page_title=tk.Label(self.top_frame,text="The Hearing",font=bigFont,bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.top_frame.grid_columnconfigure(0,weight=1)
        page_title.grid(row=self.row_no,column=0,padx=0,pady=0)
        
        self.row_no+=1
        
        def clear_placeholder(self,event,entry,placeholder):
            if entry.get()==placeholder:
                entry.delete(0,tk.END)
                entry.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
            
        def add_placeholder(event,entry,placeholder):
            if entry.get()=='':
                entry.insert(0,placeholder)
                entry.config(FOREGROUND_COLOUR='gray',font=('Helvetica',10,'italic'))
        
        #:THE FRAME CONTAINING THE INPUT WIDGETS       
        self.input_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.input_frame.grid(row=self.row_no,column=0,sticky='w')
        self.input_frame.grid_columnconfigure(0,weight=0)
        self.input_frame.grid_columnconfigure(1,weight=0)
        self.input_frame.grid_columnconfigure(2,weight=0)
        self.input_frame.grid_columnconfigure(3,weight=0)
        
        
        
        #THE DATE
        now=datetime.now()
        self.row_no+=1
        label_date = tk.Label(self.input_frame, text="Date", bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font =("Helvetica",12))
        label_date.grid(row=self.row_no, column=0, padx=0, pady=0, sticky='w')
        self.cal = DateEntry(self.input_frame, width=12, year=now.year, month=now.month, day=now.day,
            bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font =("Helvetica",12),
            date_pattern='dd-mm-yyyy')
        
        self.cal.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no+=1
        
        

        
        #LISTED FOR
        label_listed_for=tk.Label(self.input_frame,text="Listed For ",font =("Helvetica,16"))
        label_listed_for.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        label_listed_for.grid(row=self.row_no,column=0,padx=(10),pady=(10),sticky='w')
        self.comb_listed_for =ttk.Combobox(self.input_frame,values = listed_for_values,style="Custom.TCombobox")
        self.comb_listed_for.grid(row=self.row_no,column=1,padx=(10),pady=(10),sticky='w')
        
        
        self.row_no+=1
        
        #NOTICE GIVEN
        label_notice=tk.Label(self.input_frame,text="On Notice/ExParte",font=("Helvetica,16"))
        label_notice.grid(row=self.row_no,column=0,padx=(10),pady=(10),sticky='w')
        label_notice.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.combo_notice=ttk.Combobox(self.input_frame,values=notice_values,style="Custom.TCombobox")
        self.combo_notice.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.combo_notice.set(notices[1])
        self.combo_notice.bind("<<ComboboxSelected>>",self.on_combo_notice_selected)

        
        self.row_no+=1
        
        
        #REASON
        self.label_notice_reason=tk.Label(self.input_frame,text="Reason for lack of notice",font=("Helvetica,16"))
        self.label_notice_reason.config(background=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.label_notice_reason.grid(row=self.row_no,column=0,padx=(10,10),pady=(10,10),sticky='w')
        self.combo_reasons=ttk.Combobox(self.input_frame,values=self.reasons)
        self.combo_reasons.config(background=BACKGROUND_COLOUR,foreground=FOREGROUND_COLOUR)
        self.combo_reasons.grid(row=self.row_no,column=1,padx=(10,10),pady=(10,10),sticky='w')
        self.combo_reasons.current(0)
        self.combo_reasons.config(state='disabled')
        self.row_no+=1
        
        #CONSENT ORDER 
        
        
        #STATEMENT READ
        self.statements_label=tk.Label(self.input_frame,text="Statements Read by the Court")
        self.statements_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
        self.statements_label.grid(row=self.row_no,column=0,padx=(0,0),pady=10,sticky='w')
        self.row_no+=1
        self.statement_of_label=tk.Label(self.input_frame,text="Statement  of ")
        self.statement_of_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
        self.statement_of_label.grid(row=self.row_no,column=0,padx=(0,0),pady=10,sticky='w')
        
        self.wit_name1_text=tk.Entry(self.input_frame,background="white",fg=FOREGROUND_COLOUR)
        self.wit_name1_text.grid(row=self.row_no,column=1,padx=(0,0),pady=10,sticky='w')
        self.dated_label=tk.Label(self.input_frame, text=' dated ')
        self.dated_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
        self.dated_label.grid(row=self.row_no,column=2,padx=(10,10),pady=10,sticky='w')        
        now=datetime.now()
        self.stat_date=DateEntry(self.input_frame, width=12, year=now.year, month=now.month, day=now.day,
                                 date_pattern="dd//mm//yyyy")
        self.stat_date.grid(row=self.row_no,column=3,padx=(0,10),pady=10,sticky='w')
        
        
        
        #SEPARATOR
        app_appearance_values = ['Applicant in person','Applicant represented by ','no appeance by Applicant']
        resp_appearance_values =['Respondent in person','Respondent represented by','no appearance by Respondent']
        
        #REPRESENTATION
        label_appearance=tk.Label(self.input_frame,text="Appearing at this Hearing",font=theFont,anchor='w')
        label_appearance.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        label_appearance.grid(row=self.row_no,column=0,padx=0,pady=0,sticky='w')
        self.row_no+=2
        self.applic_appearance_combo=ttk.Combobox(self.input_frame,values=app_appearance_values)
        self.applic_appearance_combo.config(background=BACKGROUND_COLOUR,foreground=FOREGROUND_COLOUR,width=20)
        placeholder = app_appearance_values[0]
        self.applic_appearance_combo.set(placeholder)
        self.applic_appearance_combo.grid(row=self.row_no,column=0,padx=(10,10),pady=10, sticky='w')
        self.applic_rep_title=ttk.Combobox(self.input_frame,values=titles)
        self.applic_rep_title.config(background=BACKGROUND_COLOUR,foreground=FOREGROUND_COLOUR,width=5)
        rep_name_pholder="Enter Applicant's Representative Name"
        self.applic_rep_name=tk.Entry(self.input_frame,bg='white',fg='gray',font=theFont)
        placeholderA='Enter name of applicant representative'
        self.applic_rep_name.insert(0,placeholderA)

        self.applic_rep_name.bind("<FocusIn>",lambda  event, e=self.applic_rep_name,p=placeholderA: clear_placeholder(event,e,p))
        self.applic_rep_name
        self.applic_rep_title.grid(row=self.row_no,column=1,padx=0,pady=0,sticky='w')
        titplac=titles[0]
        self.applic_rep_title.set(titplac)
        self.applic_rep_name.grid(row=self.row_no,column=2,padx=0,pady=0,sticky='w')
        
        self.row_no+=1
        self.resp_appearance_combo=ttk.Combobox(self.input_frame,values=resp_appearance_values)
        self.resp_appearance_combo.config(background=BACKGROUND_COLOUR,foreground=FOREGROUND_COLOUR)
        placeholder=resp_appearance_values[2]
        self.resp_appearance_combo.grid(row=self.row_no, column=0, padx=(10,10),pady=0,sticky='w')
        self.resp_appearance_combo.set(placeholder)
        self.resp_rep_title=ttk.Combobox(self.input_frame,values=titles)
        self.resp_rep_title.set(titplac)
        self.resp_rep_title.config(background=BACKGROUND_COLOUR,foreground=FOREGROUND_COLOUR,width=5)
        self.resp_rep_name=tk.Entry(self.input_frame,bg='white',fg=FOREGROUND_COLOUR,font=theFont)
        self.resp_rep_title.grid(row=self.row_no,column=1,padx=0,pady=0,sticky='w')
        self.resp_rep_name.grid(row=self.row_no,column=2,padx=0,pady=0,sticky='w')
        

        
        #APPLICANT REPRESENTATIVE
        
       
        self.row_no+=1
        
        #RESPONDENT REPRESENTATIVE
        
        # label_resp_rep=tk.Label(self,text="Respondent Representative",font=theFont,anchor='w')
        # label_resp_rep.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        # label_resp_rep.grid(row=self.row_no,column=0,padx=0,pady=10,sticky ='w')
        # self.combo_resp_rep_title=ttk.Combobox(self,values=titles,style="Custom.TCombobox",width=5)
        # self.combo_resp_rep_title.grid(row=self.row_no,column=1,padx=0,pady=10,sticky='w')
       
        self.row_no+=1
        self.bind("<Double-1>",self.on_double_click)

        
        self.input_frame.grid_columnconfigure(0,weight=0)
        self.input_frame.grid_columnconfigure(1,weight=0)
        self.input_frame.grid_columnconfigure(2,weight=0)
        self.input_frame.grid_columnconfigure(3,weight=0)
        
        #NEXT AND BACK BUTTONS
        
        self.bottom_frame=tk.Frame(self,bg=BACKGROUND_COLOUR,height=50)
        self.bottom_frame.place(relx=0.5,rely=1.0,anchor='s',y=-20)
        self.bind("<Configure>", self.update_bottom_frame_width)  # Bind resize event
        #self.update_bottom_frame_width()
       

        back_button=tk.Button(self.bottom_frame,text="Back",command=self.last_action)
        next_button =tk.Button(self.bottom_frame, text="Next",command=self.next_action)
        back_button.grid(row=1,column=0,padx=10,pady=(0,10),sticky='w')
        next_button.grid(row=1,column=1,padx=10,pady=(0,10), sticky='e')
        self.bottom_frame.grid_columnconfigure(0,weight =1)
        self.bottom_frame.grid_columnconfigure(1,weight=1)
        
        
   
        
        frame=tk.Frame(parent,bg=BACKGROUND_COLOUR)
        frame.grid(row=self.row_no,column=0)
        
   
        
        
            
            
        
        #self.fill_widgets()
        
    def another_witness():
        pass
        
        
    def on_combo_notice_selected(self,event):
        if self.combo_notice.get() =="On Notice":
            self.label_notice_reason.grid_forget()
            self.combo_reasons.grid_forget()
            self.combo_reasons.config(state='disabled')
            self.statement_of_label.grid_forget()
            self.wit_name1_text.grid_forget()
            self.dated_label.grid_forget()
            self.stat_date.grid_forget()
            self.statements_label.grid_forget()
            
            
        else:
            self.label_notice_reason.grid()
            self.combo_reasons.grid()
            self.combo_reasons.config(state='normal')
            self.statement_of_label.grid()
            self.wit_name1_text.grid()
            self.dated_label.grid()
            self.stat_date.grid()
            wit_name=case_details.applicant.full_name
            self.wit_name1_text.insert(0,wit_name)
            
            

    def on_double_click(self,event):
       self.entry_app_repN1.delete(0,tk.END)
       self.entry_app_repN1.insert(0,'Charles')
       self.entry_app_repN2.delete(0,tk.END)
       self.entry_app_repN2.insert(0,'Wide')
       
       self.entry_resp_repN1.delete(0,tk.END)
       self.entry_resp_repN1.insert(0,'Simon')
       self.entry_resp_repN2.delete(0,tk.END)
       self.entry_resp_repN2.insert(0,'Slim')
       self.combo_app_rep_title.current(0)
       self.combo_resp_rep_title.current(0)
       
        
        
        
    def on_show(self):
        self.cal.set_date(case_details.hearing_date_object)
        self.comb_listed_for.set(case_details.listed_for)
        if case_details.notice:
            self.combo_notice.set(case_details.notice)
            
        else:
            self.combo_notice=="Without Notice"
                
        if case_details.notice=="On Notice":
            self.label_notice_reason.grid_forget()
            self.combo_reasons.grid_forget()
            self.combo_reasons.config(state='disabled')
            self.statement_of_label.grid_forget()
            self.wit_name1_text.grid_forget()
            self.dated_label.grid_forget()
            self.stat_date.grid_forget()
            self.statements_label.grid_forget()
            self.label_notice_reason.grid_remove()
            self.combo_reasons.grid_remove()
            
            
        self.combo_reasons.set(case_details.reasons)
        # self.combo_app_rep_title.set(case_details.app_rep.title)
        # self.entry_app_repN1.delete(0,'end')
        # self.entry_app_repN1.insert(0,case_details.app_rep.first_name)  
        # self.entry_app_repN2.delete(0,'end')
        # self.entry_app_repN2.insert(0,case_details.app_rep.last_name)
        # self.combo_resp_rep_title.set(case_details.resp_rep.title)
        # self.entry_resp_repN1.delete(0,'end')
        # self.entry_resp_repN1.insert(0,case_details.resp_rep.first_name)
        # self.entry_resp_repN2.delete(0,'end')
        # self.entry_resp_repN2.insert(0,case_details.resp_rep.last_name)



        
    def last_action(self):
            temp ='emp'
            self.update()
            self.controller.last_page()
            
    def next_action(self):
            self.update()
            self.controller.next_page()
            
    def update(self):
        case_details.notice=""
        hearing_date_string= self.cal.get()
        hearing_date_object = datetime.strptime(hearing_date_string, '%d-%m-%Y').date()
        case_details.hearing_date_object=hearing_date_object
        l_for =self.comb_listed_for.current()
        case_details.notice=self.combo_notice.get()
        case_details.app_rep.set_full_name()
        
        
         
       
        
         

        case_details.reasons=self.combo_reasons.get()
         
            
        
            
    def update_bottom_frame_width(self,event=None):
       self.bottom_frame.place_configure(width=self.winfo_width())
       
    def fill_widgets(self):
        test_run==True
        if test_run==True:
            self.comb_listed_for.set('Interim Hearing')
            self.combo_notice.set('On Notice')
            self.combo_reasons.set(self.reasons[1])
           



            
class  Children(BasePage,tk.Frame):
    def __init__(self,parent,controller,case_details):
        
        super().__init__(parent,controller,case_details)
        tk.Frame.__init__(self,parent)
        self.case_details=case_details
        self.child_count=0
        self.input_controls =[]
        self.row_no = 0
        self.child_widgets_list = []
        self.name1_widgets=[]
        self.name2_widgets=[]
        self.gender_widgets=[]
        self.dob_widgets=[]
        test_names=[]
        



        self.config(bg=BACKGROUND_COLOUR)
        self.grid(sticky='nsew')
        self.grid_columnconfigure(0,weight=1)
        
        #THE FRAME SHOWING THE PAGE TITLE CHILDREN
        self.row_no+=1
        self.top_frame=tk.Frame(self,bg='lightblue')
        self.top_frame.grid(row=0,column=0,sticky='ew')
        page_title=tk.Label(self.top_frame,text="Children",font=bigFont,bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.top_frame.grid_columnconfigure(0,weight=1)
        page_title.grid(row=self.row_no,column=0,padx=0,pady=0,sticky='ew')
        self.row_no +=1
       
        #THE FRAME CONTAINING THE INPUT WIDGETS CHILDREN
        
        self.child_input_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.child_input_frame.grid(row=self.row_no,column=0,sticky='nsew')
        self.child_input_frame.grid_columnconfigure(0,weight=1)
        self.child_input_frame.bind("<Double-1>",self.on_double_click)
        
        
        self.child_input_frame.grid_columnconfigure(0, weight=0)
        self.child_input_frame.grid_columnconfigure(1, weight=0)
        self.child_input_frame.grid_columnconfigure(2, weight=0)
        self.child_input_frame.grid_columnconfigure(3,weight=0)
        self.child_input_frame.grid_columnconfigure(4,weight=0)
        self.grid_columnconfigure(5,weight=0)
        
       
       
        
        
       

        
        #LABEL DISPLAY 1ST Name 
        child_head_name1=tk.Label(self.child_input_frame,text='1st Name',bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
        child_head_name2=tk.Label(self.child_input_frame,text='2nd Name',bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
        child_head_gender=tk.Label(self.child_input_frame,text='M/F',font=theFont,background=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,width=5)
        child_head_dob=tk.Label(self.child_input_frame,text='DoB',font=theFont,background=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,width=5)
        child_head_name1.grid(row=self.row_no,column=1,sticky='e')
        child_head_name2.grid(row=self.row_no,column=2,sticky='e')
        child_head_gender.grid(row=self.row_no,column=3,sticky='e')
        child_head_dob.grid(row=self.row_no,column=5,sticky='e')
        
        #FIRST LINE OF CHILDREN WIDGETS
        self.child_count+=1
        
        
        
        child_text_id="Child "+str(self.child_count)
        
    #    #Create Widgets 
        child_text_id = "Child " + str(self.child_count)
        
        dob=datetime.now()
        

        now=datetime.now()

        child_text_id="Child "+str(self.child_count)
        
    #    #Create Widgets 
        child_text_id = "Child " + str(self.child_count)
       
        now=datetime.now()
        ten_years_ago = now.replace(year=now.year - 10)
        now=ten_years_ago
        
        self.row_no+=1
        
        self.child_widgets={
                        'label':tk.Label(self.child_input_frame,
                        text=child_text_id,
                        bg=BACKGROUND_COLOUR,
                        fg=FOREGROUND_COLOUR,
                        font=theFont),
                        'name1': tk.Entry(self.child_input_frame),
                        'name2':tk.Entry(self.child_input_frame),
                        'gender':ttk.Combobox(self.child_input_frame,
                                        values = kid_genders,
                                        style="Custom.TCombobox",width=5),
                        'birthday':DateEntry(self.child_input_frame, width=12, year=now.year, month=now.month, day=now.day,
            bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font =("Helvetica",12),
            date_pattern='dd/mm/yyyy'),                    
            'another_child': tk.Button(self.child_input_frame,
                                                   text="Another Child",
                                                   bg=FOREGROUND_COLOUR,
                                                   fg=BACKGROUND_COLOUR,
                                                   command= self.another_kid)
        }
       

        self.child_widgets_list.append(self.child_widgets)
        self.child_widgets['label'].grid(row=self.row_no,column=0, padx=(10,10),pady=10,sticky='w')
        self.child_widgets['name1'].grid (row=self.row_no,column=1, padx=(10,10),pady=10,sticky='w')  
        self.child_widgets['name2'].grid (row=self.row_no,column=2, padx=(10,10),pady=10,sticky='w')  
        self.child_widgets['gender'].grid (row=self.row_no,column=3, padx=(10,10),pady=10,sticky='w')  
        self.child_widgets['birthday'].grid (row=self.row_no,column=4, padx=(10,0),pady=10,sticky='w') 
        self.child_widgets['another_child'].grid (row=self.row_no,column=5, padx=(10,10),pady=10,sticky='w')
       
        
        
        #THE FRAME FOR THE NEXT AND BACK BUTTONS WITH RELATED FUNCTION -CHILDREN
        
        self.bottom_frame=tk.Frame(self,bg=BACKGROUND_COLOUR,height=50)
        self.bottom_frame.place(relx=0.5,rely=1.0,anchor='s',y=-20)
        self.bind("<Configure>", self.update_bottom_frame_width)  # Bind resize event
        #self.update_bottom_frame_width()
       
        #NEXT AND BACK BUTTONS CHILDREN
        back_button=tk.Button(self.bottom_frame,text="Back",command=self.back_step)
        next_button =tk.Button(self.bottom_frame, text="Next",command=self.front_step)
        back_button.grid(row=1,column=0,padx=10,pady=(0,10),sticky='w')
        next_button.grid(row=1,column=1,padx=10,pady=(0,10), sticky='e')
        self.bottom_frame.grid_columnconfigure(0,weight =1)
        self.bottom_frame.grid_columnconfigure(1,weight=1)
        
    #FUNCTIONS CHILDREN
    def latest_dob(self):
        
       
        youngest_dob=None
        
        
        for child in self.child_widgets_list:
            child_birthday =child['birthday'].get_date()
            if youngest_dob is None or child_birthday > youngest_dob:
                youngest_dob=child_birthday
                
        return youngest_dob
                
                
                
    
    def fill_widgets(self):
        
            widget_values=[]
            the_surname=case_details.respondent.last_name
            child1=('Arthur',the_surname,'boy','01','01','2021')
            widget_values.append(child1)
            child2=('Belinda',the_surname,'girl','02','02','2022')
            widget_values.append(child2)
            child3=('Charlie',the_surname,'boy','03','03','2020')
            widget_values.append(child3)
            x = len(widget_values)
            y=len(self.child_widgets_list)
            for index,widgets in enumerate(self.child_widgets_list):
                i=index
            #widgets['label'].
                widgets['name1'].delete(0,tk.END)
                widgets['name1'].insert(0,widget_values[i][0])
                widgets['name2'].delete(0,tk.END)
                widgets['name2'].insert(0,widget_values[i][1])
                widgets['gender'].set(widget_values[i][2])
                bday=widget_values[i][3]
                bmonth=widget_values[i][4]
                byear=widget_values[i][5]
                boithdoy=f"{bday}/{bmonth}/{byear}"
            
                widgets['birthday'].set_date(boithdoy)
           
            
    def show_the_kids(self,child):
        
        now=datetime.now()
        ten_years_ago = now.replace(year=now.year - 10)
        now=ten_years_ago
        
        namen=child.first_name
        child_number=1
        string_child_number = str(child_number)
        child_text_id=f"Child {string_child_number}"
        
        child_widget_dict={
                        'label':tk.Label(self.child_input_frame,
                        text=child_text_id,
                        bg=BACKGROUND_COLOUR,
                        fg=FOREGROUND_COLOUR,
                        font=theFont),
                        'name1': tk.Entry(self.child_input_frame),
                        'name2':tk.Entry(self.child_input_frame),
                        'gender':ttk.Combobox(self.child_input_frame,
                                        values = kid_genders,
                                        style="Custom.TCombobox",width=5),
                        'birthday':DateEntry(self.child_input_frame, width=12, year=now.year, month=now.month, day=now.day,
            bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font =("Helvetica",12),
            date_pattern='dd/mm/yyyy'),      
                            
                        
                        
                        'another_child': tk.Button(self.child_input_frame,
                                                   text="Another Child",
                                                   bg=FOREGROUND_COLOUR,
                                                   fg=BACKGROUND_COLOUR,
                                                   command= self.another_kid)
                        
        }
        child_widget_dict['name1'].insert(0,child.first_name)
        child_widget_dict['name2'].insert(0,child.last_name)
        child_widget_dict['gender'].set(child.gender)
        
        child_widget_dict['birthday'].set_date(child.birthday_object)

        
        self.child_widgets_list.append(child_widget_dict)
        child_widget_dict['label'].grid(row=self.row_no,column=0, padx=(10,10),pady=10,sticky='w')
        child_widget_dict['name1'].grid (row=self.row_no,column=1, padx=(10,10),pady=10,sticky='w')  
        child_widget_dict['name2'].grid (row=self.row_no,column=2, padx=(10,10),pady=10,sticky='w')  
        child_widget_dict['gender'].grid (row=self.row_no,column=3, padx=(10,10),pady=10,sticky='w')  
        child_widget_dict['birthday'].grid (row=self.row_no,column=4, padx=(10,0),pady=10,sticky='w') 
        child_widget_dict['another_child'].grid (row=self.row_no,column=5, padx=(10,10),pady=10,sticky='w')
       
        
        
        
    def on_double_click(self,event):
        self.fill_widgets()
        
        
    def on_show(self):
        
        
        
       
        
        if case_details.children:
            case_details.children = sorted(case_details.children, key=lambda child: child.birthday_object)
            for child in case_details.children:
                self.show_the_kids(child)
                self.row_no+=1
                
            case_details.children.clear()
            
        if case_details:
            if len(case_details.children)==0:
                t =case_details.respondent.last_name
            
        self.child_widgets['name2'].insert(0,t)
            
        
        
       
       
        
        

    def back_step(self):
        self.update()
        self.child_widgets_list.clear()
        self.controller.last_page()
        
    def front_step(self):
        self.update()
        self.child_widgets_list.clear()
        self.controller.next_page()
        
    def lowest_date():
        pass
    
    def update(self):
        #case_details.children.clear()
        for widgets in self.child_widgets_list:
            name1=widgets['name1'].get()
            name2=widgets['name2'].get()
            gender=widgets['gender'].get()
            birthday=widgets['birthday'].get()
            birthday_date_object= datetime.strptime(birthday, '%d/%m/%Y')
        
            #formatted_birthday=birthday_date_object.strftime('%d %b %Y')
            
           
            child=Child(name1,name2,gender,birthday_date_object)
            
            case_details.children.append(child)
            for child in case_details.children:
                child.sentence=f"{child.first_name} {child.last_name}, a {child.gender} born on {birthday}." 
            
        for widget_dict in self.child_widgets_list:
            for widget in widget_dict.values():
                widget.destroy()            
        
        self.child_widgets_list.clear()
            
            
            
        
        
    def update_bottom_frame_width(self,event=None):
       self.bottom_frame.place_configure(width=self.winfo_width())
        
        
    def another_kid(self):
        youngest_birthday=self.latest_dob()
        set_year = youngest_birthday.year
        

        if self.child_widgets_list:
            last_row_widgets = self.child_widgets_list[-1]  # Get the last added dictionary
            last_row_widgets['another_child'].grid_forget()  # Hide the button
         
     
            
        self.row_no+=1
        self.child_count+=1        
        child_text_id="Child "+str(self.child_count)
        
    #    #Create Widgets 
        child_text_id = "Child " + str(self.child_count)
       
        now=datetime.now()
        
        self.child_widgets={
                        'label':tk.Label(self.child_input_frame,
                        text=child_text_id,
                        bg=BACKGROUND_COLOUR,
                        fg=FOREGROUND_COLOUR,
                        font=theFont),
                        'name1': tk.Entry(self.child_input_frame),
                        'name2':tk.Entry(self.child_input_frame),
                        'gender':ttk.Combobox(self.child_input_frame,
                                        values = kid_genders,
                                        style="Custom.TCombobox",width=5),
                        'birthday':DateEntry(self.child_input_frame, 
                                             width=12, year=set_year, 
                                             month=now.month, 
                                             day=now.day,
                                             bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,
                                             font =("Helvetica",12),
                                             date_pattern='dd/mm/yyyy'),                               
                        'another_child': tk.Button(self.child_input_frame,
                                                   text="Another Child",
                                                   bg=FOREGROUND_COLOUR,
                                                   fg=BACKGROUND_COLOUR,
                                                   command= self.another_kid)
        }
        self.child_widgets['birthday'].bind("<<DateEntrySelected>>", lambda event: self.lowest_date())

        self.child_widgets_list.append(self.child_widgets)  
        self.child_widgets['label'].grid(row=self.row_no,column=0, padx=(10,10),pady=10,sticky='w')
        self.child_widgets['name1'].grid (row=self.row_no,column=1, padx=(10,10),pady=10,sticky='w')  
        self.child_widgets['name2'].grid (row=self.row_no,column=2, padx=(10,10),pady=10,sticky='w')  
        self.child_widgets['gender'].grid (row=self.row_no,column=3, padx=(10,10),pady=10,sticky='w')  
        self.child_widgets['birthday'].grid(row=self.row_no,column=4,padx=(10,10),pady=10,sticky='w')
        self.child_widgets['another_child'].grid (row=self.row_no,column=5, padx=(10,10),pady=10,sticky='w')
        self.row_no+=1 
        
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
        
       
            
       
                
       
    


        
   #END CHILDREN
            
class Recitals(BasePage,tk.Frame):
    def __init__(self,parent,controller,case_details):
        
        super().__init__(parent,controller,case_details)
        tk.Frame.__init__(self,parent)
        tk.Frame.__init__(self,parent)
        self.config(bg=BACKGROUND_COLOUR)
        self.recital_widgets=[]
        self.grid(sticky='nsew')
        self.grid_columnconfigure(0,weight=1)
        self.checked_items=[]
        self.checkbox_texts=[
            "Legal Aid",
            "Remote Hearing",
            "Covid",
            "Prohibition of Cross-Examination",
            ]
       
        self.checkbox_vars=[]
        self.row_no=0
		
        #RECITALS THE FRAME SHOWING THE PAGE TITLE
        self.row_no +=1
        self.top_frame=tk.Frame(self,bg='lightblue')
        self.top_frame.grid(row=0,column=0,sticky='ew')
        page_title=tk.Label(self.top_frame,text="Recitals",font=bigFont,bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.top_frame.grid_columnconfigure(0,weight=1)  
        page_title.grid(row=self.row_no,column=0,sticky='ew')
        
        #RECITALS:THE FRAME CONTAINING THE INPUT WIDGETS       
        self.input_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.input_frame.grid(row=self.row_no,column=0,sticky='nw')
        self.input_frame.grid_columnconfigure(0,weight=0)
        
        #RECITALS THE INPUT WIDGETS
        self.checked_items=[]
        for text in self.checkbox_texts:
            check_var=tk.IntVar()
            self.checkbox_vars.append(check_var)
            chkbutton=tk.Checkbutton(self.input_frame,text=text,variable=check_var)
            chkbutton.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
            chkbutton.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
            
            self.row_no+=1
            
        statements_label=tk.Label(self.input_frame,text="Statements Read")
        statements_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
        statements_label.grid(row=self.row_no,column=0,padx=(10,10),pady=10,sticky='w')
        self.row_no+=1
        statement_of_label=tk.Label(self.input_frame,text="Statement of ")
        statement_of_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
        statement_of_label.grid(row=self.row_no,column=0,padx=(10,10),pady=10,sticky='w')
        
        self.wit_name1_text=tk.Entry(self.input_frame,background="white",fg=FOREGROUND_COLOUR)
        self.wit_name1_text.grid(row=self.row_no,column=1,padx=(10,0),pady=10,sticky='w')
        dated_label=tk.Label(self.input_frame, text=' dated ')
        dated_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
        dated_label.grid(row=self.row_no,column=2,padx=(10,10),pady=10,sticky='w')        
        now=datetime.now()
        self.stat_date=DateEntry(self.input_frame, width=12, year=now.year, month=now.month, day=now.day,
                                 date_pattern="dd//mm//yyyy")
        self.stat_date.grid(row=self.row_no,column=3,padx=(0,10),pady=10,sticky='w')
        
        another_button=tk.Button(self.input_frame,text='Another Statement',command=self.another_witness)
        another_button.config(bg=FOREGROUND_COLOUR,fg=BACKGROUND_COLOUR)
        another_button.grid(row=self.row_no,column=4,padx=0,pady=0,sticky='w')
        
       
        
            
            
        
        
        
         #THE FRAME FOR THE NEXT AND BACK BUTTONS WITH RELATED FUNCTION
        
        self.bottom_frame=tk.Frame(self,bg=BACKGROUND_COLOUR,height=50)
        self.bottom_frame.place(relx=0.5,rely=1.0,anchor='s',y=-20)
        self.bind("<Configure>", self.update_bottom_frame_width)  # Bind resize event
        #self.update_bottom_frame_width()
       

        back_button=tk.Button(self.bottom_frame,text="Back",command=self.back_step)
        next_button =tk.Button(self.bottom_frame, text="Next",command=self.front_step)
        back_button.grid(row=1,column=0,padx=10,pady=(0,10),sticky='w')
        next_button.grid(row=1,column=1,padx=10,pady=(0,10), sticky='e')
        self.bottom_frame.grid_columnconfigure(0,weight =1)
        self.bottom_frame.grid_columnconfigure(1,weight=1)
        
    def article(self,word):
        vowels='aeiou'
        if word:
            word=word.lower()
            first_letter =word[0].lower()
            if first_letter in vowels:
                return 'an '
            else:
                return 'a '
            
    def another_witness(self):
        print('In another witness')
        
        
    def on_show(self):
        
        self.wit_name1_text.delete(0,tk.END)
        self.wit_name1_text.insert(0,case_details.applicant.full_name)
    
    def back_step(self):
        tempvar=self.case_details.notice
        self.update()
        self.controller.last_page()
        
    def front_step(self):
        self.update()
        self.controller.next_page()
        
    def update(self):
        app_type =case_details.application
        
    
        
        
        artic=self.article(app_type)
        the_notice = case_details.notice_string
        the_notice=the_notice.lower()
        
        if type(case_details.application) is not int:
            app_type=case_details.application
            app_type.lower()
            
       
        recitals_dict={
            "Standard":(
                f"This is {artic} {app_type} made against the respondent "
            f"{case_details.respondent.first_name}  {case_details.respondent.last_name} on "
            f"{case_details.hearing_date_object.strftime('%d %B %Y').replace(' 0', ' ') if case_details.hearing_date_object.day < 10 else case_details.hearing_date_object.strftime('%d %B %Y')} "
            f"by {case_details.judge_rank} {case_details.judge_name} "
            f"on the application of the applicant {case_details.applicant.first_name}  {case_details.applicant.last_name}"
            ),
            
             "Legal Aid":("The court records the following information for the purposes of the Family Advocacy Scheme (FAS):\n"
"\ta.	the advocates met for pre-hearing discussions between [time] and [time];\n"
"\tb.	the hearing started at [start time] and ended at [end time] ; \n"
"\tc.	the court allowed [time} thereafter for preparation and agreement of the order between [time] and [time];\n"
"\td.	{advocate_name} is entitled to a bolt on because {advocate_nominative_pronoun} is representing a client who is facing allegations that they have caused significant harm to a child and these are a live issue in proceedings;\n"
"\te.	all advocates are entitled to a bolt on because an independent expert witness was cross-examined and substantially challenged by a party at the hearing; and"
"\tf.	the advocates bundle page count is [number].),"
             ),
            "Remote Hearing":"",
            "Covid":("The court determined that in the exceptional circumstances of the current national public health emergency" 
                     "this case is suitable for hearing remotely (“remote hearing”) by means of [insert]."),
            "Prohibition of Cross-Examination":"Some random placeholder text",
            "Short Notice":(f"This order was made at a hearing {the_notice.lower()} to the respondent."
            f"The reason why the order was made {the_notice.lower()} to the respondent was {case_details.reasons}."
            f"The respondent has the right to apply to the court to vary or discharge the order" 
            f" see paragraph  below."),
            "On Notice":"This order was made at a hearing on notice to the respondent."
            
        }
        recitals_list=["Standard"]
        if case_details.notice !='On Notice':
                recitals_list.append("Short Notice")
        else:
            recitals_list.append("On Notice")
        
        for text,var in zip(self.checkbox_texts,self.checkbox_vars):
           
            if var.get()==1:
                recitals_list.append(text)
                
        for key in recitals_list:
            case_details.recitals.append(recitals_dict[key])
        
        tempvar = case_details.notice
            
                     
        
        
                
        
        
        
    def update_bottom_frame_width(self,event=None):
       self.bottom_frame.place_configure(width=self.winfo_width())
       
        
        

        

        
            
            
class Undertakings(BasePage,tk.Frame):
    def __init__(self,parent,controller,case_details):
        
        super().__init__(parent,controller,case_details)
        tk.Frame.__init__(self,parent)
        tk.Frame.__init__(self,parent)
        self.config(bg=BACKGROUND_COLOUR)
        self.grid(sticky='nsew')
        self.grid_columnconfigure(0,weight=1)
        self.row_no=0
        
        #UNDERTAKINGS THE FRAME SHOWING THE PAGE TITLE
        self.row_no +=1
        self.top_frame=tk.Frame(self,bg='lightblue')
        self.top_frame.grid(row=0,column=0,sticky='ew')
        page_title=tk.Label(self.top_frame,text="Recitals",font=bigFont,bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.top_frame.grid_columnconfigure(0,weight=1)
		
		#UNDERTAKINGS THE FRAME SHOWING THE PAGE TITLE
        self.row_no +=1
        self.top_frame=tk.Frame(self,bg='lightblue')
        self.top_frame.grid(row=0,column=0,sticky='ew')
        page_title=tk.Label(self.top_frame,text="Undertakings",font=bigFont,bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.top_frame.grid_columnconfigure(0,weight=1)
        page_title.grid(row=1,column=0,padx=0,pady=0,sticky='ew')
        self.chkIss =tk.BooleanVar()
        


 
 
 #UNDERTAKINGS:THE FRAME CONTAINING THE INPUT WIDGETS
 
        self.widget_input_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.widget_input_frame.grid(row=1,column=0,sticky='nsew')
 
       
        self.widget_input_frame.grid(row=1,column=0,sticky='nsew')
        self.widget_input_frame.grid_columnconfigure(0,weight=1)
        self.widget_input_frame.grid_columnconfigure(0, weight=0)
        self.widget_input_frame.grid_columnconfigure(1, weight=0)
        self.widget_input_frame.grid_columnconfigure(5,weight=0)

        
        #UNDERTAKINGS. THE INPUT WIDGETS. 
        
        self.checked_items=[]
        self.checkbox_texts=[
           "Issue Application Notice",
           "File Witness Statement",
           "Serve the Respondent"
           
            ]
        self.checkbox_vars=[]
        self.row_no=0
        
        for text in self.checkbox_texts:
            txt=text
            check_var=tk.IntVar()
            self.checkbox_vars.append(check_var)
            length=len(self.checkbox_vars)
            chkbutton=tk.Checkbutton(self.widget_input_frame,text=text,variable=check_var)
            chkbutton.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
            chkbutton.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')  
            self.row_no+=1
        
        

		
	#UNDERTAKINGS:THE FRAME FOR THE NEXT AND BACK BUTTONS WITH RELATED FUNCTION
  
        self.bottom_frame=tk.Frame(self,bg=BACKGROUND_COLOUR,height=50)
        self.bottom_frame.place(relx=0.5,rely=1.0,anchor='s',y=-20)
        self.bind("<Configure>", self.update_bottom_frame_width)  # Bind resize event
        self.update_bottom_frame_width()
        
        #NEXT AND BACK BUTTONS
       

        back_button=tk.Button(self.bottom_frame,text="Back",command=self.last_action)
        next_button =tk.Button(self.bottom_frame, text="Next",command=self.next_action)
        back_button.grid(row=1,column=0,padx=10,pady=(0,10),sticky='w')
        next_button.grid(row=1,column=1,padx=10,pady=(0,10), sticky='e')
        self.bottom_frame.grid_columnconfigure(0,weight =1)
        self.bottom_frame.grid_columnconfigure(1,weight=1)
		
	
#UNDERTAKINGS FUNCTIONS
    def update_bottom_frame_width(self,event=None):
       self.bottom_frame.place_configure(width=self.winfo_width())
       
    def on_show(self):
        pass
	   
    def last_action(self):
            self.update()
            self.controller.last_page()
            
    def next_action(self):
        
            self.update()
            self.controller.next_page()
            
    def update(self):
        #tody =datetime.date.today()
        from datetime import date, timedelta
        tody=date.today()
        date_and_time = tody + timedelta(days=3)
        Undertakings_dict={
            "Issue Application Notice":f"By {date_and_time} the applicant shall: \n\t a.  issue an application claiming the appropriate relief; and "
            "\n\t b.  file a witness statement substantially in the same terms of the draft witness statement "
            "produced to the court.",
            "Serve the Respondent": (f"By  the applicant shall use {self.case_details.applicant.possessive} best endeavours personally to serve"
            " upon the respondent by posting to the respondent's usual address, together with this order:"
            "\n\ta.  a copy of this application;"
            "\n\tb.  copies of the witness statement(s)and exhibits containing the evidence relied upon by the applicant "
            "and any other documents provided to the court on the making of the application; and"
            f"\n\tc.  a note prepared by {self.case_details.applicant.possessive}  solicitor recording the substance of "
            "the dialogue with the court at the hearing and the reasons given by the court for making the order, which note "
            "shall include(but not be limited to) any allegation of fact made orally to the court where such allegation"
            " is not contained in the witness statements or draft witness statements read by the judge"),
            "File Witness Statement": f"By {date} the applicant shall:\n\t"
            "a. file a witness s\tatement substantially in the terms of the draft witness statement produced to the court."       
            
        }
        for text,var in zip(self.checkbox_texts,self.checkbox_vars):
           
            if var.get()==1:
                txt_para=Undertakings_dict [text]
                case_details.undertakings.append(txt_para)
                
        if case_details.notice !="on notice":
            parpar=("The statement of service of this order on the respondent shall be filed at court and shall be in a form "
            "which complies with section 9 of the Criminal Justice Act 1967 and shall include the following signed declaration:"
            "'This statement is true tot he best of my knowledge and belief and I make it knowing that, "
            "if it were tendered in evidence, I would be liable for prosecution if I wilfully stated in it anything which I know to "
            "be false or did not believe to be true'")
            case_details.undertakings.append(parpar)
            
            
class all_Orders(BasePage):
    def __init__(self, parent, controller, case_details):
        super().__init__(parent, controller, case_details)
        tk.Frame.__init__(self,parent)
        self.case_details=case_details
        self.controller=controller
        self.config(bg=BACKGROUND_COLOUR)    
        self.grid_columnconfigure(0,weight=1)
        self.widgets_list=[]
        self.row_no=1
		
#TITLE Frame

        self.top_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.top_frame.grid(row=0,column=0,sticky='ew')
        page_title=tk.Label(self.top_frame,text="Orders ",font=bigFont,bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.top_frame.grid_columnconfigure(0,weight=1)
        page_title.grid(row=self.row_no,column=0, padx=0,pady=10,sticky='ew')
		
#WIDGET Frame
        
        self.input_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.input_frame.grid(row=1,column=0,sticky='w')
        self.input_frame.grid_columnconfigure(0,weight=0)
        self.row_no+=1
        
        checkbox_var = tk.IntVar()
        non_mol_checkbox = tk.Checkbutton(self.input_frame, text="Standard Non Mol", variable=checkbox_var)
        non_mol_checkbox.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
        non_mol_checkbox.grid(row=self.row_no, column=0, padx=10, pady=10,sticky='w')
        self.row_no+=1
        
        checkbox_var = tk.IntVar()
        non_com_checkbox = tk.Checkbutton(self.input_frame, text="Standard No Communicate", variable=checkbox_var)
        non_com_checkbox.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
        non_com_checkbox.grid(row=self.row_no, column=0, padx=10, pady=10,sticky='w')
        self.row_no+=1
        
        checkbox_var = tk.IntVar()
        kid_non_mol_checkbox = tk.Checkbutton(self.input_frame, text="Standard Non Mol Children", variable=checkbox_var)
        kid_non_mol_checkbox.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
        kid_non_mol_checkbox.grid(row=self.row_no, column=0, padx=10, pady=10,sticky='w')
        self.row_no+=1
        
        
        checkbox_var = tk.IntVar()
        ouster_checkbox = tk.Checkbutton(self.input_frame, text="Standard Ouster", variable=checkbox_var)
        ouster_checkbox.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
        ouster_checkbox.grid(row=self.row_no, column=0, padx=10, pady=10,sticky='w')
        self.row_no+=1
        
        checkbox_var = tk.IntVar()
        allow_entry_checkbox = tk.Checkbutton(self.input_frame, text="Standard Allow Entry", variable=checkbox_var)
        allow_entry_checkbox.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
        allow_entry_checkbox.grid(row=self.row_no, column=0, padx=10, pady=10,sticky='w')
        self.row_no+=1
        
        checkbox_var = tk.IntVar()
        zonal_checkbox = tk.Checkbutton(self.input_frame, text="Standard Zonal", variable=checkbox_var)
        zonal_checkbox.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
        zonal_checkbox.grid(row=self.row_no, column=0, padx=10, pady=10,sticky='w')
        self.row_no+=1
        


#NEXT AND BACK BUTTON Frame

        self.bottom_frame=tk.Frame(self,bg=BACKGROUND_COLOUR,height=50)
        self.bottom_frame.place(relx=0.5,rely=1.0,anchor='s',y=-20)
        self.bind("<Configure>", self.update_bottom_frame_width)  # Bind resize event

        back_button=tk.Button(self.bottom_frame,text="Back",command=self.back_step)
        next_button =tk.Button(self.bottom_frame, text="Next",command=self.front_step)
        back_button.grid(row=1,column=0,padx=10,pady=(0,10),sticky='w')
        next_button.grid(row=1,column=1,padx=10,pady=(0,10), sticky='e')
        self.bottom_frame.grid_columnconfigure(0,weight =1)
        self.bottom_frame.grid_columnconfigure(1,weight=1)

#FUNCTIONS

    def update_bottom_frame_width(self,event=None):
       self.bottom_frame.place_configure(width=self.winfo_width())
        

    def on_show(self):
        pass

    def update(self):
        pass

    def back_step(self):
        self.update(self)
        self.controller.last_page()

    def front_step(self):
        self.update(self)
        self.controller.next_page()
        
            
    
class OccOrders(BasePage):
    
    def __init__(self,parent,controller,case_details):
        
        super().__init__(parent,controller,case_details)
        self.config(bg=BACKGROUND_COLOUR)
        self.grid(sticky='nsew')
        self.grid_columnconfigure(0,weight=1)
        self.row_no=0
		
        #OCCUPATION ORDERS (test) THE FRAME SHOWING THE PAGE TITLE
        self.row_no +=1
        self.top_frame=tk.Frame(self,bg='lightblue')
        self.top_frame.grid(row=0,column=0,sticky='ew')
        page_title=tk.Label(self.top_frame,text="Occupation Orders",font=bigFont,bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.top_frame.grid_columnconfigure(0,weight=1)  
        page_title.grid(row=self.row_no,column=0,sticky='ew')
        
        #OCCUPATION ORDERS:THE FRAME CONTAINING THE INPUT WIDGETS       
        self.input_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.input_frame.grid(row=self.row_no,column=0,sticky='nsew')
        self.input_frame.grid_columnconfigure(0,weight=1)
        
        #OCCUPATION ORDERS THE INPUT WIDGETS
        self.checked_items=[]
        self.checkbox_col1_vars=[]
        self.checkbox_col2_vars=[]
        self.checkbox_texts_col1=[
            "Declaration of Mat Home Rights",
            "Mat Home Rights Survive Divorce",
            "R Allow Occupy  of Mat Home",
            "R Must Not Occupy Mat Home",
            "R leave Mat Home",
            "R Not Return to Mat Home",
            "Not Obstruct A's Occupation",
            "Right of Entry",
            "Right Not to be Evicted"]
        self.checkbox_col2_vars=[]
        self.checkbox_texts_col2=[        
        "R pay Mortgage",
        "A maintain",
        "R maintain",
        "A discharge outgoings",
        "R discharge outgoings",
        "A pay Occupation Rent",
        "A Care for Contents",
        "A return furniture",
        "R return furniture",
        "A keep secure",
        "R keep secure"
    ]



        
        for text in self.checkbox_texts_col1:
            var =tk.IntVar()
            self.checkbox_col1_vars.append(var)
            chk=tk.Checkbutton(self.input_frame,text=text,variable=var)
            chk.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
            chk.grid(row=self.row_no,column=0,padx=1,pady=10,sticky='w')
            self.row_no+=1
            
        self.row_no=0            
        for text in self.checkbox_texts_col2:
            var = tk.IntVar()
            self.checkbox_col2_vars.append(var)
            chk=tk.Checkbutton(self.input_frame,text=text,variable=var)
            chk.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
            chk.grid(row=self.row_no,column=1,padx=0,pady=10,sticky='w')
            self.row_no+=1
            
            self.input_frame.grid_columnconfigure(0,weight=1)
            self.input_frame.grid_columnconfigure(1,weight=1)        
		
        
         #THE FRAME FOR THE NEXT AND BACK BUTTONS WITH RELATED FUNCTION
        
        self.bottom_frame=tk.Frame(self,bg=BACKGROUND_COLOUR,height=50)
        self.bottom_frame.place(relx=0.5,rely=1.0,anchor='s',y=-20)
        self.bind("<Configure>", self.update_bottom_frame_width)  # Bind resize event
        #self.update_bottom_frame_width()
       

        back_button=tk.Button(self.bottom_frame,text="Back",command=self.back_step)
        next_button =tk.Button(self.bottom_frame, text="Next",command=self.front_step)
        back_button.grid(row=1,column=0,padx=10,pady=(0,10),sticky='w')
        next_button.grid(row=1,column=1,padx=10,pady=(0,10), sticky='e')
        self.bottom_frame.grid_columnconfigure(0,weight =1)
        self.bottom_frame.grid_columnconfigure(1,weight=1)
        
    #ORDERS FUNCTIONS
        
    def on_show(self):
        pass
    def update(self):
        for i, var in enumerate(self.checkbox_col1_vars):
            if var.get() == 1:  # If the checkbox is checked
                case_details.order_choices.append(self.checkbox_texts_col1[i])
                
      
        
        
        
        

        

    def back_step(self):
        self.update()
        self.controller.last_page()
        
    def front_step(self):
       
        self.update()
        self.controller.next_page()
        
    def update_bottom_frame_width(self,event=None):
       self.bottom_frame.place_configure(width=self.winfo_width())
       
       
class NonMols(BasePage):
    
    def __init__(self,parent,controller,case_details):
        
        super().__init__(parent,controller,case_details)
        self.config(bg=BACKGROUND_COLOUR)
        self.grid(sticky='nsew')
        self.grid_columnconfigure(0,weight=1)
        self.row_no=0
		
        #NON MOLESTATION  ORDERS THE FRAME SHOWING THE PAGE TITLE
        self.row_no +=1
        self.top_frame=tk.Frame(self,bg='lightblue')
        self.top_frame.grid(row=0,column=0,sticky='ew')
        page_title=tk.Label(self.top_frame,text="Non Molestation Orders",font=bigFont,bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.top_frame.grid_columnconfigure(0,weight=1)  
        page_title.grid(row=self.row_no,column=0,sticky='ew')
        
        #OCCUPATION ORDERS:THE FRAME CONTAINING THE INPUT WIDGETS       
        self.input_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.input_frame.grid(row=self.row_no,column=0,sticky='nsew')
        self.input_frame.grid_columnconfigure(0,weight=1)
        
        #OCCUPATION ORDERS THE INPUT WIDGETS
        self.checked_items=[]
        self.checkbox_col1_vars=[]
        self.checkbox_col2_vars=[]
        self.checkbox_texts_col1=[
            "Use or threaten violence",
            "Not intimidate,harass or pester",
            "Not communicate",
            "Not damage property",
            "Not damage family home",
            "Not Enter family home",
            "Non mol zonal",
            "Not intimidate, harass or pester children",
            "Not communicate with children",
            "Not enter children's school"
            ]
        



        
        for text in self.checkbox_texts_col1:
            var =tk.IntVar()
            self.checkbox_col1_vars.append(var)
            chk=tk.Checkbutton(self.input_frame,text=text,variable=var)
            chk.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
            chk.grid(row=self.row_no,column=0,padx=1,pady=10,sticky='w')
            self.row_no+=1
            
        self.row_no=0       
             
       
            
        self.input_frame.grid_columnconfigure(0,weight=1)
        self.input_frame.grid_columnconfigure(1,weight=1)        
		
        
         #THE FRAME FOR THE NEXT AND BACK BUTTONS WITH RELATED FUNCTION
        
        self.bottom_frame=tk.Frame(self,bg=BACKGROUND_COLOUR,height=50)
        self.bottom_frame.place(relx=0.5,rely=1.0,anchor='s',y=-20)
        self.bind("<Configure>", self.update_bottom_frame_width)  # Bind resize event
        #self.update_bottom_frame_width()
       

        back_button=tk.Button(self.bottom_frame,text="Back",command=self.back_step)
        next_button =tk.Button(self.bottom_frame, text="Next",command=self.front_step)
        back_button.grid(row=1,column=0,padx=10,pady=(0,10),sticky='w')
        next_button.grid(row=1,column=1,padx=10,pady=(0,10), sticky='e')
        self.bottom_frame.grid_columnconfigure(0,weight =1)
        self.bottom_frame.grid_columnconfigure(1,weight=1)
        
    #NON MOLS FUNCTIONS
        
    def on_show(self):
        pass
    def update(self,controller):
        #The following puts the checkbox text of ticked checkboxes in the list case_details.order_choices
        for i, var in enumerate(self.checkbox_col1_vars):
            if var.get() == 1:  # If the checkbox is checked
                 case_details.order_choices.append(self.checkbox_texts_col1[i])
        
        
        
        
      
        
        
        
#
        
        
       
       
                    
        
        
        

        

    def back_step(self):
        ord="cow"
        self.update(self.controller)
        self.controller.last_page()
        
    def front_step(self):
        self.update(self.controller)
        self.controller.next_page()
        
    def update_bottom_frame_width(self,event=None):
       self.bottom_frame.place_configure(width=self.winfo_width())
       

class Duration(BasePage,tk.Frame):
    def __init__(self,parent,controller,case_details):
        
        super().__init__(parent,controller,case_details)
        tk.Frame.__init__(self,parent)
        tk.Frame.__init__(self,parent)
        self.config(bg=BACKGROUND_COLOUR)
        self.case_details=case_details
        self.grid(sticky='nsew')
        self.grid_columnconfigure(0,weight=1)
        self.combo_list=[]
        
        self.row_no=0
        #DURATION THE FRAME SHOWING THE PAGE TITLE
        self.row_no +=1
        self.top_frame=tk.Frame(self,bg='lightblue')
        self.top_frame.grid(row=0,column=0,sticky='ew')
        page_title=tk.Label(self.top_frame,text="Duration of Order",font=bigFont,bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.top_frame.grid_columnconfigure(0,weight=1)  
        page_title.grid(row=self.row_no,column=0,sticky='ew')
        
        #DURATION:THE FRAME CONTAINING THE INPUT WIDGETS       
        self.input_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.input_frame.grid(row=self.row_no,column=0,sticky='nsew')
        self.input_frame.grid_columnconfigure(0,weight=0)
        self.row_no=1
        effect_list=['On Service','made aware']
        last_list=['1','2','3','6','12']
        lbl_effect=tk.Label(self.input_frame,text="Order effective from: ",font=theFont)
        lbl_effect.grid(row=self.row_no,column=0,padx=(10,10),pady=10,sticky='w')
        lbl_effect.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.comb_effect=ttk.Combobox(self.input_frame, values=effect_list,font=theFont)
        self.comb_effect.grid(row=self.row_no,column=1,padx=(10,10),pady=10,sticky='w')
        self.combo_list.append(self.comb_effect)
        self.row_no+=1
        lbl_ord_last=tk.Label(self.input_frame,text="The Order lasts for: ",font=theFont)
        lbl_ord_last.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        lbl_ord_last.grid(row=self.row_no,column=0,padx=(10,10),pady=10,sticky='w')
        self.combo_or_last=ttk.Combobox(self.input_frame,values=last_list,font=theFont, style="Custom.TCombobox",width=5)
        self.combo_or_last.grid(row=self.row_no,column=1,padx=(10,0),pady=10,sticky='w')
        self.combo_list.append(self.combo_or_last)
        lbl_mnths=tk.Label(self.input_frame,text="months",font=theFont)
        lbl_mnths.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        lbl_mnths.grid(row=self.row_no,column=2,padx=(2,10),pady=10,sticky='w')
        self.row_no+=1
        
        
      #DURATION:THE FRAME FOR THE NEXT AND BACK BUTTONS WITH RELATED FUNCTION
  
        self.bottom_frame=tk.Frame(self,bg=BACKGROUND_COLOUR,height=50)
        self.bottom_frame.place(relx=0.5,rely=1.0,anchor='s',y=-20)
        self.bind("<Configure>", self.update_bottom_frame_width)  # Bind resize event
        self.update_bottom_frame_width()
        
        #DURATION NEXT AND BACK BUTTONS
       

        back_button=tk.Button(self.bottom_frame,text="Back",command=self.last_action)
        next_button =tk.Button(self.bottom_frame, text="Next",command=self.next_action)
        back_button.grid(row=1,column=0,padx=10,pady=(0,10),sticky='w')
        next_button.grid(row=1,column=1,padx=10,pady=(0,10), sticky='e')
        self.bottom_frame.grid_columnconfigure(0,weight =1)
        self.bottom_frame.grid_columnconfigure(1,weight=1)
		
	
#DURATION FUNCTIONS
    def update_bottom_frame_width(self,event=None):
       self.bottom_frame.place_configure(width=self.winfo_width())
       
    def on_show(self):
        self.comb_effect.current(0)
        self.combo_or_last.current(3)
        
    def update(self):
        pass
    
        
    
    def last_action(self):
        self.update()
        self.controller.last_page()
            
    def next_action(self):   
            tempo='tempo' 
            self.update()    
            self.controller.next_page()
            
    def add_time(self,months):
        from dateutil.relativedelta import relativedelta
        today=datetime.now()
        mon = int(months)
        later = today + relativedelta(months=mon) 
        return later
    
    
    def format_date(self,date_object):
        day = date_object.day  # This returns the day of the month as an integer
        formatted_date = f"{day} {date_object.strftime('%B %Y')}"  # Format with the month and year
        return formatted_date
        
       

            
    def update(self):
        from datetime import date, timedelta
        app_name=[]
        app_name1 =case_details.applicant.first_name
        app_name2=case_details.applicant.last_name
        app_name=app_name1+" "+app_name2
        resp_name1=case_details.respondent.first_name
        resp_name2=case_details.respondent.last_name
        resp_name=resp_name1+" "+resp_name2
              
        mat_home1=case_details.applicant.address_building_and_street
        mat_home2=case_details.applicant.address_second_line
        mat_home3=case_details.applicant.address_town_or_city
        mat_home4=case_details.applicant.address_postcode
        mat_home=mat_home1+", "+mat_home2+", "+mat_home3+", "+mat_home4
        relat=self.case_details.relationship
        tody=date.today()
        leave_date = tody + timedelta(days=7)
        mnths=self.combo_or_last.get()
        if isinstance(mnths,int)==False:
            mnths='6'
        
            
            
            
            tempdate=self.add_time(mnths)
            form_ord_last=self.format_date(tempdate)
            case_details.order_last=form_ord_last
        
        tempord1=f"This order shall be effective against the respondent {resp_name} once it is personally served on {case_details.respondent.accusative}."
        case_details.orders.append(tempord1)
        tempord2 =f"This order shall last until {case_details.order_last} unless it is set aside or varied before then by an order of the court."   
        case_details.orders.append(tempord2)
        
       
        

#HEADER

class Actions(BasePage,tk.Frame):
    
    def __init__(self,parent,controller,case_details):
        super().__init__(parent,controller,case_details)
        tk.Frame.__init__(self,parent)
        self.controller=controller
        self.config(bg=BACKGROUND_COLOUR)    
        self.grid_columnconfigure(0,weight=1)
        self.widgets_list=[]
        self.row_no=1
		
#TITLE Frame

        self.top_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.top_frame.grid(row=0,column=0,sticky='ew')
        page_title=tk.Label(self.top_frame,text="Actions",font=bigFont,bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.top_frame.grid_columnconfigure(0,weight=1)
        page_title.grid(row=self.row_no,column=0, padx=0,pady=10,sticky='ew')
		
#WIDGET Frame
        
        self.input_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.input_frame.grid(row=1,column=0,sticky='w')
        self.input_frame.grid_columnconfigure(0,weight=0)
        self.row_no=0
        
#THE WIDGETS
#Consent Order Check box
        self.row_no+=1
        
        self.consent_var=tk.BooleanVar()
        self.chk_consent=tk.Checkbutton(self.input_frame,
                text='Tick if Consent Order',
                variable=self.consent_var,
                font=theFont,
                anchor='e'
                )
        self.chk_consent.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.chk_consent.grid(row=self.row_no, column=0, padx=10, pady= 10,sticky='w')
        self.row_no+=1
        print_button = tk.Button(self.input_frame,text="Create Order",command=self.produce_order)
        print_button.config(background=FOREGROUND_COLOUR,fg=BACKGROUND_COLOUR)
        print_button.grid(row=self.row_no,column=0,padx=(10,10),pady=10,sticky='w')
        self.row_no+=1
        save_button=tk.Button(self.input_frame,text="Save File",command=self.save_file)
        save_button.config(bg=FOREGROUND_COLOUR,fg=BACKGROUND_COLOUR )
        save_button.grid(row=self.row_no,column=0, padx=(10,10),pady=10,sticky='w')

#NEXT AND BACK BUTTON Frame

        self.bottom_frame=tk.Frame(self,bg=BACKGROUND_COLOUR,height=50)
        self.bottom_frame.place(relx=0.5,rely=1.0,anchor='s',y=-20)
        self.bind("<Configure>", self.update_bottom_frame_width)  # Bind resize event

        back_button=tk.Button(self.bottom_frame,text="Back",command=self.back_step)
        next_button =tk.Button(self.bottom_frame, text="Next",command=self.front_step)
        back_button.grid(row=1,column=0,padx=10,pady=(0,10),sticky='w')
        next_button.grid(row=1,column=1,padx=10,pady=(0,10), sticky='e')
        self.bottom_frame.grid_columnconfigure(0,weight =1)
        self.bottom_frame.grid_columnconfigure(1,weight=1)

#FUNCTIONS

    def update_bottom_frame_width(self,event=None):
       self.bottom_frame.place_configure(width=self.winfo_width())
        

    def on_show(self):
        pass
    

    def update(self):
        pass
    
    def front_step(self):
        pass

    def back_step(self):
        self.update(self)
        self.controller.last_page()
        
    def produce_order(self):
        self.case_details.name_file()
        write_order(case_details=case_details)
        
    def save_file(self):
        self.case_details.name_file()
        suffix ='.ord'
        file_name =case_details.file_name+suffix
        with open(file_name, 'wb') as file:
            pickle.dump(case_details, file)
    
        
#HEADER

class Further_Info(BasePage,tk.Frame):
    
    def __init__(self,parent,controller,case_details):
        super().__init__(parent,controller,case_details)
        tk.Frame.__init__(self,parent)
        self.case_details=case_details
        self.controller=controller
        self.config(bg=BACKGROUND_COLOUR)    
        self.grid_columnconfigure(0,weight=1)
        self.widgets_list=[]
        self.applicant_widgets=[]
        self.combo_list=[]

        self.row_no=1
		
#TITLE Frame
        self.top_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.top_frame.grid(row=0,column=0,sticky='ew')
        page_title=tk.Label(self.top_frame,text="Further Information ",font=bigFont,bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.top_frame.grid_columnconfigure(0,weight=1)
        page_title.grid(row=self.row_no,column=0, padx=0,pady=10,sticky='ew')
		
#WIDGET Frame
	
        self.input_frame=tk.Frame(self,bg=BACKGROUND_COLOUR)
        self.input_frame.grid(row=1,column=0,sticky='w')
        self.input_frame.grid_columnconfigure(0,weight=0)
        
#THE WIDGETS

        self.consent_var=tk.BooleanVar()
        self.chk_consent=tk.Checkbutton(self.input_frame,
                text='Tick if Consent Order',
                variable=self.consent_var,
                font=theFont,
                anchor='e'
                )
        
        self.chk_consent.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.chk_consent.grid(row=self.row_no,column=0,padx=(10,10),pady=10,sticky='w')
        self.row_no+=2
        
        effect_list=['On Service','made aware']
        last_list=['1','2','3','6','12']
        lbl_effect=tk.Label(self.input_frame,text="Order effective from: ",font=theFont)
        lbl_effect.grid(row=self.row_no,column=0,padx=(10,10),pady=10,sticky='w')
        lbl_effect.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.comb_effect=ttk.Combobox(self.input_frame, values=effect_list,font=theFont)
        self.comb_effect.grid(row=self.row_no,column=1,padx=(10,10),pady=10,sticky='w')
        self.combo_list.append(self.comb_effect)
        self.row_no+=1
        lbl_ord_last=tk.Label(self.input_frame,text="The Order lasts for: ",font=theFont)
        lbl_ord_last.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        lbl_ord_last.grid(row=self.row_no,column=0,padx=(10,10),pady=10,sticky='w')
        self.combo_or_last=ttk.Combobox(self.input_frame,values=last_list,font=theFont, style="Custom.TCombobox",width=5)
        self.combo_or_last.grid(row=self.row_no,column=1,padx=(10,0),pady=10,sticky='w')
        self.combo_list.append(self.combo_or_last)
        lbl_mnths=tk.Label(self.input_frame,text="months",font=theFont)
        lbl_mnths.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        lbl_mnths.grid(row=self.row_no,column=2,padx=(2,10),pady=10,sticky='w')
        #Property Address
        self.row_no +=1
        self.title_label=tk.Label(self.input_frame,text="Address of Property for Occupation Order")
        self.title_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR,font=theFont)
        self.title_label.grid(row=self.row_no,column=0,padx=0,pady=0,sticky='w')
        
        self.row_no+=1
        self.add1_label=tk.Label(self.input_frame,text="Address 1", font=("Helvetica",12))
        self.add1_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.add1_entry=tk.Entry(self.input_frame,background="white",fg=FOREGROUND_COLOUR)
        self.add1_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.applicant_widgets.append(self.add1_entry)

        self.add1_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no+=1
        self.add2_label=tk.Label(self.input_frame,text="Address 2", font=("Helvetica",12))
        self.add2_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.add2_entry =tk.Entry(self.input_frame,background="white",fg=FOREGROUND_COLOUR)
        self.applicant_widgets.append(self.add2_entry)
        self.add2_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.add2_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no+=1
        #Town/City
        town_label=tk.Label(self.input_frame,text="Town/City", font=("Helvetica",12))
        town_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.town_entry =tk.Entry(self.input_frame,background="white",fg=FOREGROUND_COLOUR)
        self.applicant_widgets.append(self.town_entry)
        town_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.town_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')
        self.row_no+=1
        
        #PostCode
        postcode_label=tk.Label(self.input_frame,text="Post Code", font=("Helvetica",12))
        postcode_label.config(bg=BACKGROUND_COLOUR,fg=FOREGROUND_COLOUR)
        self.postcode_entry =tk.Entry(self.input_frame,background="white",fg=FOREGROUND_COLOUR)
        self.applicant_widgets.append(self.postcode_entry)
        postcode_label.grid(row=self.row_no,column=0,padx=10,pady=10,sticky='w')
        self.postcode_entry.grid(row=self.row_no,column=1,padx=10,pady=10,sticky='w')




#NEXT AND BACK BUTTON Frame

        self.bottom_frame=tk.Frame(self,bg=BACKGROUND_COLOUR,height=50)
        self.bottom_frame.place(relx=0.5,rely=1.0,anchor='s',y=-20)
        self.bind("<Configure>", self.update_bottom_frame_width)  # Bind resize event

        back_button=tk.Button(self.bottom_frame,text="Back",command=self.back_step)
        next_button =tk.Button(self.bottom_frame, text="Next",command=self.front_step)
        back_button.grid(row=1,column=0,padx=10,pady=(0,10),sticky='w')
        next_button.grid(row=1,column=1,padx=10,pady=(0,10), sticky='e')
        self.bottom_frame.grid_columnconfigure(0,weight =1)
        self.bottom_frame.grid_columnconfigure(1,weight=1)

#FUNCTIONS

    def update_bottom_frame_width(self,event=None):
       self.bottom_frame.place_configure(width=self.winfo_width())
        

    def on_show(self):
        pass

    def update(self):
        if self.chk_consent==True:
            case_details.consent_order=True
            
        case_details.effective =  self.comb_effect.get()
        case_details.order_last= self.combo_or_last.get()
       
           
        
        pass

    def back_step(self):
        self.update(self)
        self.controller.last_page()

    def front_step(self):
        self.update(self)
        self.controller.next_page()


    def front_step(self):
            self.update()
            self.controller.next_page()
            
    def produce_order(self):
        write_order(case_details)
    
    def save_file(self):
       
        filename=f"{case_details.applicant.last_name} v {case_details.respondent.last_name} {case_details.case_number}"
        filename=filename+".json"

        
        self.to_dict()
        self.save_to_json(filename)
        
    def to_dict(self):
        tempo = self.case_details.children[0]
        tompo=tempo.first_name
        return {
            "children": [child.to_dict() for child in self.case_details.children],
            "relationship": self.case_details.relationship,
            "court_name": self.case_details.court_name,
            "case_name": self.case_details.case_name,
            "judge_name": self.case_details.judge_name,
            "judge_rank": self.case_details.judge_rank,
            "case_number": self.case_details.case_number,
            "hearing_date": self.case_details.hearing_date,
            "listed_for": self.case_details.listed_for,
            "application": self.case_details.application,
            "para_numbers": self.case_details.para_numbers,
            "consent_order": self.case_details.consent_order,
            "notice": self.case_details.notice,
            "reasons": self.case_details.reasons,
            "judge_and_hearing": self.case_details.judge_and_hearing,
            "applicant": self.case_details.applicant.to_dict(),
            "app_rep": self.case_details.app_rep.to_dict(),
            "resp_rep": self.case_details.resp_rep.to_dict(),
            "respondent": self.case_details.respondent.to_dict(),
            "parties": self.case_details.parties,
            "definitions": self.case_details.definitions,
            "recitals": self.case_details.recitals,
            "undertakings": self.case_details.undertakings,
            "orders": self.case_details.orders,
            "order_last": self.case_details.order_last,
            "effective": self.case_details.effective,
        }

    def save_to_json(self, filename):
        with open(filename, 'w') as json_file:
            json.dump(self.to_dict(), json_file, indent=4)

    
       
if __name__ =="__main__":
            app = MultiPage()
            app.geometry("800x600")
            app.mainloop()