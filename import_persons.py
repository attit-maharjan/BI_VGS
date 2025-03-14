#!/usr/bin/env python

import os
import django
import pandas as pd
from datetime import datetime

# Set the path to your Django project's settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BI_VGS.settings")  # Adjust to your project name

# Set the path to your project directory
project_dir = r"C:\Users\im_co\Desktop\College web dev project\BI_VGS"
os.chdir(project_dir)  # Change the working directory to the project directory

# Initialize Django
django.setup()

# Import your models
from office.models import Person, Role  # Adjust to your app name

# Set the path to your Excel file
excel_file_path = os.path.join(project_dir, "persons.xlsx")

# Load Excel file
df = pd.read_excel(excel_file_path)

# Loop through and create Person objects
for index, row in df.iterrows():
    try:
        # Get the Role instance based on the role name in the Excel file
        role_instance = Role.objects.get(role_name=row['role'])  # Use `role_name` instead of `name`
        
        # Parse the date_of_birth from the Excel file (assuming it's in a column named 'date_of_birth')
        date_of_birth = None
        if isinstance(row['date_of_birth'], pd.Timestamp):
            date_of_birth = row['date_of_birth'].date()  # Direct conversion if pandas Timestamp
        else:
            date_str = str(row['date_of_birth']).split()[0]  # Take only the date part (before space)
            date_of_birth = datetime.strptime(date_str, "%Y-%m-%d").date()

        
        # Create the Person object with the Role instance and date_of_birth
        person = Person.objects.create(
            first_name=row['first_name'],
            last_name=row['last_name'],
            role=role_instance,  # Assign the Role instance
            email=row['email'],
            date_of_birth=date_of_birth  # Add the date_of_birth field
        )
        print(f"Added: {person.first_name} {person.last_name} as {person.role.role_name} (DOB: {person.date_of_birth})")
    except Role.DoesNotExist:
        print(f"Role '{row['role']}' does not exist in the database.")
    except KeyError as e:
        print(f"Missing column in Excel file: {e}")
    except Exception as e:
        print(f"Error adding person at row {index}: {e}")

print("Import completed!")