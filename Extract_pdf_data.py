import PyPDF2
import tkinter as tk
from tkinter import filedialog


def extract_field_names(pdf_path):
    field_names = set()  # Using a set to avoid duplicates

    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Loop through all pages in the PDF
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            annotations = page.get('/Annots', [])
            
            for annotation in annotations:
                field_obj = annotation.get_object()  # Get the field annotation as a dict
                field_name = field_obj.get('/T')  # Get the field name
                if field_name:
                    field_names.add(field_name)

    return field_names

def open_file_dialog():
    # Create a tkinter root window (it will be hidden)
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open the file dialog and return the selected file path
    file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )
    return file_path


if __name__ == '__main__':
    pdf_file_path = open_file_dialog()  # Open file dialog to select PDF

    if not pdf_file_path:  # Check if the user did not select a file
        print("No file was selected.")
    else:
        field_names = extract_field_names(pdf_file_path)

        # Print the discovered field names
        print("Field Names Found:")
        for name in field_names:
            print(name)