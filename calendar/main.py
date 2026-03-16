
# How to create calendar with python code

import calendar

# Input year and month
year = int(input("Enter year (e.g., 2023): "))
month = int(input("Enter month (e.g., 1-12): "))

# Create a calendar instance for the specified year and month
cal = calendar.month(year, month)

# Display the calendar
print(f"Calendar for {calendar.month_name[month]} {year}:")
print(cal)
