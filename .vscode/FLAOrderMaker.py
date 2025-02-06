import sys
import os
#sys.path.append(os.path.abspath('C:\Users\sgcam\Projects\FLAOrderMaker'))


import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from Person import Person


def submit_form():
    # Function to handle form submission
    court = "court"
    caseNo = "TP052141"
    # Add further submission logic here

def main():
    # Create the main window
    root = tk.Tk()
    text = "RoyalBlue4"
    background = "ivory"
    label_font = ('Arial', 12)
    root.title("Data Entry Form")
    root.configure(bg="seashell")

    root.columnconfigure(0, weight=1)  # Allow column 0 to expand

    # Create and place form widgets
    row_no = 0
    court_options = ["Brighton", "Hastings", "Horsham", "Worthing", "Guildford", "Reigate", "Kingston"]
    label_court = tk.Label(root, text="Court:", font=label_font)
    label_court.config(bg="seashell", fg="green")
    label_court.grid(row=row_no, column=0, padx=(10), pady=10, sticky='w')
    entry_court = ttk.Combobox(root, values=court_options)
    entry_court.grid(row=row_no, column=1, padx=10, pady=(10, 5), sticky='w')
    row_no += 1

    label_caseNo = tk.Label(root, text="Case Number:", font=label_font)
    label_caseNo.config(bg=background, fg=text)
    label_caseNo.grid(row=row_no, column=0, padx=10, pady=10, sticky='w')
    entry_caseNo = tk.Entry(root)
    entry_caseNo.grid(row=row_no, column=1, padx=10, pady=10, sticky='w')
    row_no += 1

    # Add more widgets as in your code...
    # ...

    submit_button = tk.Button(root, text="Submit", command=submit_form)
    submit_button.grid(row=row_no, column=2, pady=10, sticky='w')

    # Set window dimensions
    window_width = 800
    window_height = 500

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the x and y coordinates for the Tk root window
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)

    # Set the geometry of the window
    root.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")

    root.mainloop()

if __name__ == '__main__':
    main()
