import pandas as pd

# Load CSV files
df1 = pd.read_csv("daily_sales_data_0.csv")
df2 = pd.read_csv("daily_sales_data_1.csv")
df3 = pd.read_csv("daily_sales_data_2.csv")

# Combine them
df = pd.concat([df1, df2, df3])

# Filter only pink morsel
df = df[df["product"] == "pink morsel"]

# Create Sales column
df["Sales"] = df["quantity"] * df["price"]

# Keep only required columns
df = df[["Sales", "date", "region"]]

# Rename columns
df.columns = ["Sales", "Date", "Region"]

# Save result
df.to_csv("formatted_sales_data.csv", index=False)

print("Done!")