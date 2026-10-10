import os
import requests
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

print("Step 1: Fetching FDA Adverse Event (FAERS) data...")
url = "https://api.fda.gov/drug/event.json?limit=100"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()["results"]
    
    # Normalize nested JSON structures into a flat pandas DataFrame
    df = pd.json_normalize(data)
    print(f"Successfully extracted and flattened {len(df)} adverse event records.")
    
    print("Step 2: Transforming, cleaning, and engineering partition keys...")
    target_cols = ['safetyreportid', 'receivedate', 'serious', 'seriousnesshospitalization']
    available_cols = [col for col in target_cols if col in df.columns]
    df_clean = df[available_cols].copy()
    
    # Handle dates and derive partition keys (Year / Serious status)
    if 'receivedate' in df_clean.columns:
        df_clean['receivedate'] = pd.to_datetime(df_clean['receivedate'], format='%Y%m%d', errors='coerce')
        df_clean['report_year'] = df_clean['receivedate'].dt.year.fillna(0).astype(int)
    
    if 'serious' in df_clean.columns:
        df_clean['serious'] = df_clean['serious'].fillna(0).astype(str)
        
    df_clean = df_clean.dropna(subset=['safetyreportid'])
    
    print("Step 3: Writing cloud-style partitioned Parquet dataset...")
    table = pa.Table.from_pandas(df_clean)
    
    # Define output directory mimicking an AWS S3 / ADLS data lake landing zone
    output_dir = "faers_partitioned_lake"
    
    # Write Hive-style partitioned dataset (mimicking AWS S3 / Azure Data Lake storage patterns)
    pq.write_to_dataset(
        table,
        root_path=output_dir,
        partition_cols=['report_year', 'serious']
    )
    
    print(f"Pipeline complete! Hive-style partitioned data lake created under '{output_dir}/'.")
else:
    print("API error:", response.status_code)