import requests
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

print("Step 1: Fetching FDA Adverse Event (FAERS) data...")
# Target the adverse event endpoint
url = "https://api.fda.gov/drug/event.json?limit=100"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()["results"]
    
    # Normalize nested JSON into a flat pandas DataFrame
    df = pd.json_normalize(data)
    print(f"Successfully extracted {len(df)} adverse event records.")
    
    print("Step 2: Transforming and cleaning data...")
    # Safely select available top-level reporting fields
    available_cols = [col for col in ['safetyreportid', 'receivedate', 'serious', 'seriousnesshospitalization'] if col in df.columns]
    df_clean = df[available_cols].copy()
    
    if 'receivedate' in df_clean.columns:
        df_clean['receivedate'] = pd.to_datetime(df_clean['receivedate'], format='%Y%m%d', errors='coerce')
    
    print("Step 3: Saving to Parquet format...")
    table = pa.Table.from_pandas(df_clean)
    pq.write_table(table, 'fda_adverse_events.parquet')
    print("Pipeline complete! Adverse event data saved as 'fda_adverse_events.parquet'.")
else:
    print("API error:", response.status_code)