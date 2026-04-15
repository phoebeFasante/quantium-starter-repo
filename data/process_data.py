import pandas as pd

# Read the 3 source files
df0 = pd.read_csv("daily_sales_data_0.csv")
df1 = pd.read_csv("daily_sales_data_1.csv")
df2 = pd.read_csv("daily_sales_data_2.csv")

# Combine them
df = pd.concat([df0, df1, df2], ignore_index=True)

# Keep only Pink Morsels
df = df[df["product"] == "pink morsel"].copy()

# Clean quantity and price
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["price"] = (
    df["price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .astype(float)
)

# Create sales column
df["Sales"] = df["quantity"] * df["price"]

# Keep only required columns
df = df[["Sales", "date", "region"]].copy()

# Rename columns
df.columns = ["Sales", "Date", "Region"]

# Save output
df.to_csv("formatted_sales_data.csv", index=False)

print("formatted_sales_data.csv created successfully")