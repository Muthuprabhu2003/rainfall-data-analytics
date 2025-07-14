import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

try:
    df = pd.read_csv(r"D:\new comers\powerbi\Rainfall\New folder\rainfall\combined_rainfall_data.csv")
    print("✅ Dataset loaded.")
except FileNotFoundError:
    raise FileNotFoundError("❌ File not found.")

# Rename and clean
df.rename(columns={
    "Date": "date",
    "District": "district",
    "State": "state",
    "Avg_rainfall": "avg_rainfall"
}, inplace=True)

df["date"] = pd.to_datetime(df["date"], errors='coerce')
df["avg_rainfall"] = pd.to_numeric(df["avg_rainfall"], errors='coerce')
df.dropna(subset=["date", "avg_rainfall"], inplace=True)

try:
    engine = create_engine("mysql+mysqlconnector://rainuser:rainpass@localhost/rain_db")
    df.to_sql("rainfall_data", con=engine, if_exists="replace", index=False)
    print("✅ Data uploaded to MySQL.")
except SQLAlchemyError as e:
    print("❌ Upload failed:", str(e))