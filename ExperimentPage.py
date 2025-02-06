import tkinter as tk
from tkinter import ttk


from tkcalendar import DateEntry
root = tk.Tk()
cal = DateEntry(root, width=12, year=2019, month=6, day=22, 
background='darkblue', foreground='white', borderwidth=2)
cal.grid(row=0,column=0,padx=10, pady=10)
root.mainloop()