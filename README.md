# OpenFDA Adverse Events (FAERS) Data Lake Pipeline

## Overview
An enterprise-grade data engineering pipeline designed to ingest, flatten nested JSON payloads, clean, and store public health safety data from the openFDA Adverse Event Reporting System (FAERS). Built to bridge clinical regulatory expertise with modern cloud-native data lake architectures.

## Key Engineering Highlights
* **Nested JSON Normalization:** Flattens complex, multi-level hierarchical API payloads into tabular schemas ready for analytical querying.
* **Cloud-Style Data Lake Partitioning:** Implements Hive-style partitioning (`report_year=` / `serious=`) using Apache Parquet, optimizing query performance and storage efficiency for cloud object stores like AWS S3 or Azure Data Lake Storage (ADLS).
* **Robust Data Typing & Cleaning:** Standardizes date formats, handles null values, and enforces strict schema compliance.

## Architecture & Tech Stack
* **Ingestion:** Python (`requests`), RESTful API integration
* **Processing & Normalization:** Python (`pandas`, `pyarrow`)
* **Storage Format & Layout:** Columnar Apache Parquet with Hive-style partitioning
* **Orchestration Ready:** Configurable for automated execution via GitHub Actions, AWS Glue, or Azure Data Factory.

## Project Structure
'''text
fda-pipeline/
├── src/
│   └── app.py                  # Ingestion, flattening, partitioning & storage script
├── faers_partitioned_lake/     # Hive-style partitioned Parquet data lake output
├── .gitignore                  # Ignored generated runtime/lake files
└── README.md                   # Pipeline documentation & architecture

## How to Run Locally
1. **Install dependencies:**
   ```bash
   python -m pip install requests pandas pyarrow
2. **Execute pipeline:**
   ```bash
   python src/app.py
