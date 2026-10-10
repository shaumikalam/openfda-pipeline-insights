import requests
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

print("Step 1: Fetching data from openFDA...")
url = "https://api.fda.gov/drug/enforcement.json?limit=100"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()["results"]
    df = pd.json_normalize(data)
    print(f"Successfully extracted {len(df)} records.")
    
    print("Step 2: Transforming and cleaning data...")
    df_clean = df[['recall_number', 'reason_for_recall', 'product_description', 'distribution_pattern', 'report_date']]
    df_clean['report_date'] = pd.to_datetime(df_clean['report_date'], format='%Y%m%d', errors='coerce')
    df_clean = df_clean.dropna(subset=['recall_number'])
    
    print("Step 3: Saving to Parquet format...")
    table = pa.Table.from_pandas(df_clean)
    pq.write_table(table, 'fda_recalls.parquet')
    print("Pipeline complete! Data transformed and saved as 'fda_recalls.parquet'.")
else:
    print("API error:", response.status_code)