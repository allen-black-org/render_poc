#!/usr/bin/env python
import os
from sqlalchemy import create_engine, text
from snowflake.sqlalchemy import URL
from dotenv import load_dotenv

# 1. Load .env into os.environ
load_dotenv()

# 2. Read credentials from environment
USER     = os.getenv("SNOWFLAKE_USER")
PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
ACCOUNT  = os.getenv("SNOWFLAKE_ACCOUNT")
DB       = os.getenv("SNOWFLAKE_DATABASE")
SCHEMA   = os.getenv("SNOWFLAKE_SCHEMA")
WH       = os.getenv("SNOWFLAKE_WAREHOUSE")
ROLE     = os.getenv("SNOWFLAKE_ROLE")

engine = create_engine(
    'snowflake://{user}:{password}@{account_identifier}/'.format(
        user=USER,
        password=PASSWORD,
        account_identifier=ACCOUNT,
    )
)
with engine.connect() as conn:
    # Wrap your SQL in text()
    result = conn.execute(text("select wholesaler_name from dist_perf_db.dist_perf_staging.dim_wholesalers limit 10"))
    for row in result:
        print(row[0])

engine.dispose()
