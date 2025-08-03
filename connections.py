# connections.py
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from snowflake.sqlalchemy import URL
from dotenv import load_dotenv

#
# --- POSTGRES ---
#
POSTGRES_URL = os.getenv("POSTGRES_URL")
if not POSTGRES_URL:
    raise RuntimeError("POSTGRES_URL is not set!")

engine_pg   = create_engine(POSTGRES_URL, echo=False)
SessionPG   = sessionmaker(bind=engine_pg)

#
# --- SNOWFLAKE ---
#
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

engine_sf = create_engine(
    'snowflake://{user}:{password}@{account_identifier}/'.format(
        user=USER,
        password=PASSWORD,
        account_identifier=ACCOUNT,
    )
)
SessionSF = sessionmaker(bind=engine_sf)