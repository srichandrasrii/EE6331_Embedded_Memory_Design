import openpyxl
import re
import os
import numpy as np

# Get the current working directory
current_directory = os.getcwd()

# Define the filename you want to include
filename = 'Reff_sim.log'  # Replace with your actual file name

# Construct the full path to the file
log_file_path = os.path.join(current_directory, filename)

# Open and read the log file
with open(log_file_path, 'r') as file:
    log_contents = file.read()

# Define the regex pattern
pattern = r'Measurement: mac_\d{1,3}[\s\S]*?(?=Measurement: mac_\d{1,3}|$)'

# Find all matches
matches = re.findall(pattern, log_contents)

# Arrays to store the average and standard deviation
averages = []
stddevs = []
mac_numbers = []

# Regex pattern to extract v(out) values
vout_pattern = r'^\s*\d+\s+([\d.]+)'

# Process each measurement block
for match in matches:

    # Extract the mac number
    mac_number = re.search(r'Measurement: (mac_\d{1,3})', match).group(1)
    mac_numbers.append(mac_number)

    # Find all v(out) values in the current measurement block
    vout_values = re.findall(vout_pattern, match, re.MULTILINE)
    vout_values = [float(value) for value in vout_values]

    # Calculate the average and standard deviation using numpy
    if vout_values:
        avg = np.mean(vout_values)
        stddev = np.std(vout_values)  # ddof=1 for sample standard deviation

        # Append to the arrays
        averages.append(avg)
        stddevs.append(stddev)

# Create a new Excel workbook and select the active worksheet
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Measurement Data"

# Write the headers
headers = ["Mac Number", "Average", "Standard Deviation"]
ws.append(headers)

# Write the data to the Excel sheet
for mac, avg, std in zip(mac_numbers, averages, stddevs):
    ws.append([mac, avg, std])

# Save the workbook
wb.save("measurement_data.xlsx")
print("Excel file 'measurement_data.xlsx' created successfully.")