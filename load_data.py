import pandas as pd

# Define the file path
excel_file = "production_history.xlsx"

# Read the excel file
xls = pd.ExcelFile(excel_file)

# Get sheet names
sheet_names = xls.sheet_names
print(f"Sheet names: {sheet_names}")

# Load each sheet into a dictionary of DataFrames
# I will load all sheets by their names to inspect them.
bales_produced_df = pd.read_excel(excel_file, sheet_name='bales_produced')
cotton_used_df = pd.read_excel(excel_file, sheet_name='cotton_used_in_production')
acceptable_weight_df = pd.read_excel(excel_file, sheet_name='acceptable_weight_per_bale')
daily_target_df = pd.read_excel(excel_file, sheet_name='daily_target')
monthly_target_df = pd.read_excel(excel_file, sheet_name='monthly_target')


print("\n--- bales_produced ---")
print(bales_produced_df.head())

print("\n--- cotton_used_in_production ---")
print(cotton_used_df.head())

print("\n--- acceptable_weight_per_bale ---")
print(acceptable_weight_df.head())

print("\n--- daily_target ---")
print(daily_target_df.head())

print("\n--- monthly_target ---")
print(monthly_target_df.head())
