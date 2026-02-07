import pandas as pd
import sys

# Read the Excel file
input_file = 'G2024.xlsx'
output_file = 'G2024_informatic.xlsx'

# Load data
df = pd.read_excel(input_file)

# Filter rows where 'specia' starts with 'IN'
filtered_df = df[df['specia'].astype(str).str.startswith('I')]

# Save to new Excel file
filtered_df.to_excel(output_file, index=False)

print(f"Filtered data saved to {output_file}")
print(f"Total rows: {len(df)}")
print(f"Filtered rows (specia starting with 'IN'): {len(filtered_df)}")
