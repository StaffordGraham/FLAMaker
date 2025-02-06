import tkinter as tk
from tkinter import ttk

class MultiGridApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # First Grid with 3 Columns at the Top
        tk.Label(self, text="First Grid - Column 1").grid(row=0, column=0)
        tk.Label(self, text="Second Grid - Column 2").grid(row=0, column=1)
        tk.Label(self, text="Third Grid - Column 3").grid(row=0, column=2)

        # Optionally configure column weights for the first grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Adding some space before the second grid
        tk.Label(self, text="").grid(row=1)  # An empty label to create space

        # Second Grid with 7 Columns Below
        for i in range(7):
            tk.Label(self, text=f"Column {i+1}").grid(row=2, column=i)

        # Optionally configure column weights for the second grid
        for i in range(7):
            self.grid_columnconfigure(i, weight=1)

if __name__ == "__main__":
    app = MultiGridApp()
    app.mainloop()
