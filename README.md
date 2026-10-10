# OpenFDA Drug Enforcement & Recall Data Pipeline

## Overview
An automated data engineering pipeline designed to ingest, normalize, and transform public health safety data from the openFDA API into a cloud-optimized columnar data lake format (Apache Parquet). Built to bridge clinical regulatory knowledge with modern cloud-native data architecture.

## Architecture & Tech Stack
* **Ingestion:** Python (`requests`), RESTful API integration
* **Processing & Normalization:** Python (`pandas`)
* **Storage Format:** Apache Parquet (Partitioned columnar storage optimized for AWS S3 / Azure Data Lake Storage)
* **Orchestration Ready:** Configurable for automated scheduling via GitHub Actions, AWS Glue, or Azure Data Factory.

## Directory Structure
```text
openfda-pipeline-insights/
├── src/
│   └── app.py              # Ingestion & transformation pipeline script
├── .gitignore              # Ignored generated runtime files
└── README.md               # Pipeline documentation & architecture

## How to Run Locally

1. **Install dependencies:**
   ```bash
   python -m pip install requests pandas pyarrow
2. **Execute Pipeline:**
   ```bash
   python src/app.py
