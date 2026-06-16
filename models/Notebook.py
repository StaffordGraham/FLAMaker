import tkinter as tk
from tkinter import ttk
import tkcalendar
from tkcalendar import DateEntry
class MultiPageApp(tk.Tk):
     #set fonts and colours
        text = "RoyalBlue4" 
        background="ivory"
        label_font = ('Arial',12)
    
        def __init__(self):
            super().__init__()
            self.title("FLA Injunction")

      
        
       
        
          # Set window dimensions
        
            window_width = 800
            window_height = 500

        # Get the screen width and height
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

        # Calculate the x and y coordinates for the Tk root window
            x_coordinate = (screen_width / 2) - (window_width / 2)
            y_coordinate = (screen_height / 2) - (window_height / 2)

        # Set the geometry of the window
            self.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")

        # Create a notebook (tabbed interface) to hold multiple pages
            self.notebook = ttk.Notebook(self)
            self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create and add pages to the notebook
            self.court = Court(self.notebook)
            self.notebook.add(self.court, text="Court")

            self.Applicant = Applicant (self.notebook)
            self.notebook.add(self.Applicant, text="Applicant ")

            self.parties = Parties(self.notebook)
            self.notebook.add(self.parties, text="Parties")
            
            self.children=Children(self.notebook)
            self.notebook.add(self.children, text="Children")
            
            self.hearing=Hearing(self.notebook)
            self.notebook.add(self.hearing, text ="Hearing")
            self.order=Order(self.notebook)
            self.notebook.add(self.order,text="Order")
       

class Court(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        row_no = 0 
        
        court_options=["Brighton","Hastings","Horsham","Worthing","Guildford","Reigate","Kingston"]
        label_court= tk.Label(self, text="Court:",font=('Arial',12))
        label_court.config(bg = "ivory", fg="#6A5ACD")
        label_court.grid(row=row_no, column=0, padx=(10), pady=10,sticky='w')
        
        entry_court=ttk.Combobox(self,values = court_options)
        entry_court.grid(row=row_no, column=1, padx=10, pady=(10,5), sticky='w')
        row_no +=1
        
        judge_options=["DDJ Graham Campbell","DDJ Jane Campbell"]
        label_judge=tk.Label(self,text="Judge:",font=('Arial',12))
        label_judge.config(bg = "ivory", fg="#6A5ACD")
        label_judge.grid(row=row_no,column=0,padx=10,pady=10,sticky='w')
        entry_judge=ttk.Combobox(self,values=judge_options)
        entry_judge.grid(row=row_no,column=1,padx=10,pady=10,sticky='w')
        row_no +=1
        label_court_email=tk.Label(self,text="Email for orders",font=('Arial',12))
        label_court_email.config(bg="ivory",fg = "#6A5ACD")
        label_court_email.grid(row=row_no,column=0,padx=10,pady=10,sticky='w')
        entry_court_email=ttk.Combobox(self, values ="")
        entry_court_email.grid(row=row_no,column=1,padx=10,pady=10,sticky='w')
        row_no +=1
        label_caseNo = tk.Label(self, text="Case Number:",font=('Arial',12))
        label_caseNo.config(bg="ivory",fg = "#6A5ACD")
        label_caseNo.grid(row=row_no, column=0, padx=10, pady=10,sticky='w')
        entry_caseNo = tk.Entry(self)
        entry_caseNo.grid(row=row_no, column=1, padx=10, pady=10,sticky='w')
        row_no+=1
        label_applicant_name=tk.Label(self,text="Applicant: ",font=('Arial',12))
        entry_app_name=tk.Entry(self)
        label_applicant_name.grid(row=row_no, column=0,padx=10,pady=10,sticky='w')
        entry_app_name.grid(row=row_no,column=1,padx=10,pady=10,sticky='w')
        entry_app_name2=tk.Entry(self)
        entry_app_name2.grid(row=row_no,column = 2, padx=10,pady=10,sticky='w')
        row_no +=1
        label_respondent_name=tk.Label(self,text="Respondent: ",font=('Arial',12))
        entry_resp_name=tk.Entry(self)
        entry_resp_name2 =tk.Entry(self)
        label_respondent_name.grid(row=row_no, column=0,padx=10,pady=10,sticky='w')
        entry_resp_name.grid(row=row_no,column=1,padx=10,pady=10,sticky='w')
        entry_resp_name2.grid(row=row_no,column=2,padx=10,pady=10,sticky='w')
        
        
            

class Applicant(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        row_no=0
        label = tk.Label(self, text="Applicant")
        label_applicant_name=tk.Label(self,text="Name: ",font=('Arial',12))
        entry_app_name=tk.Entry(self)
        label_applicant_name.grid(row=row_no, column=0,padx=10,pady=10,sticky='w')
        entry_app_name.grid(row=row_no,column=1,padx=10,pady=10,sticky='w')
        entry_app_name2=tk.Entry(self)
        entry_app_name2.grid(row=row_no,column = 0, padx=10,pady=10,sticky='w')
        row_no +=1

        label_applicant_dob=tk.Label(self,text= "Date of Birth: ", font=('Arial',12))
        label_applicant_dob.grid(row=row_no,column=0,sticky='w')
        app_dob=DateEntry(self,width=12,
background='darkblue',foreground='white',borderwidth = 2)
        app_dob.grid(row=row_no,column =1,padx=10,pady=10,sticky ='w')
        

class Parties(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Parties")
        label.pack(padx=10, pady=10)
        
        
        
        
class Children(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Children")
        label.pack(padx=10, pady=10)
        
class Hearing(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text="Hearing")
        label.pack(padx=10, pady=10)
class Order(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        label=tk.Label(self,text="Orders")
        label.pack(padx=10,pady=10)

if __name__ == "__main__":
    app = MultiPageApp()
    app.mainloop()
