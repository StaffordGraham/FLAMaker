from datetime import datetime, date

class Child:
    def __init__(self, first_name: str, last_name: str, gender: str, dob: date):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender

        # Store the date object
        self.birthday_object = dob

        # Store a formatted string version
        self.dob = dob.strftime("%d/%m/%Y")

        # Optional: compute age
        self.age = self.calculate_age(dob)

        # Useful for narrative sentences
        self.sentence = f"{self.first_name} {self.last_name}, a {self.gender} born on {self.dob}."

    def calculate_age(self, dob: date) -> int:
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
