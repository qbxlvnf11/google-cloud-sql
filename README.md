
### 1. Create the .env file & Add Configuration Variables to the .env file

```bash
# Google Cloud SQL Connection Details
# Enter your actual database connection information here.

INSTANCE_CONNECTION_NAME="<YOUR_PROJECT_ID>:<YOUR_REGION>:<YOUR_INSTANCE_CONNECTION_NAME>"
DB_USER="<YOUR_DB_USER_ID>"
DB_PASS="<YOUR_DB_USER_PASSWORD>"
DB_NAME="<YOUR_DB_NAME>"
TABLE_NAME="<YOUR_TABLE_NAME>"
```

### 2. Set default credentials (Application Default Credentials, ADC) for accessing Google Cloud 

```
gcloud auth application-default login
```

### 3. Set environment

```bash
conda create -n google_cloud_sql_env python=3.9
conda activate google_cloud_sql_env 
pip install "cloud-sql-python-connector[pg8000]"  # For PostgreSQL
pip install "cloud-sql-python-connector[pymysql]" # For MySQL
pip install sqlalchemy
pip install python-dotenv
pip install psycopg2-binary
```

### 4. Run test code

```python
python test_google_cloud_sql.py
```
