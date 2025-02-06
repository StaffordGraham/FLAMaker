from datetime import datetime
from datetime import date
import _tkinter
from tkinter import ttk

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