# connections.py
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from snowflake.sqlalchemy import URL
from dotenv import load_dotenv

# ————————————————————————————————————————————
# 0. Load .env *before* any getenv calls
# ————————————————————————————————————————————
load_dotenv()

# ————————————————————————————————————————————
# 1. POSTGRES
# ————————————————————————————————————————————
POSTGRES_URL = os.getenv("POSTGRES_URL")
if not POSTGRES_URL:
    raise RuntimeError("POSTGRES_URL is not set!")

engine_pg   = create_engine(POSTGRES_URL, echo=False)
SessionPG   = sessionmaker(bind=engine_pg)
PostgresBase = declarative_base()

# ————————————————————————————————————————————
# 2. SNOWFLAKE
# ————————————————————————————————————————————
SnowflakeBase = declarative_base()
SF_VARS = ("SNOWFLAKE_USER", "SNOWFLAKE_PASSWORD", "SNOWFLAKE_ACCOUNT",
           "SNOWFLAKE_DATABASE", "SNOWFLAKE_SCHEMA", "SNOWFLAKE_WAREHOUSE")
missing = [v for v in SF_VARS if not os.getenv(v)]
if missing:
    raise RuntimeError(f"Missing Snowflake env vars: {', '.join(missing)}")

# Build the URL with the helper so you get DB, schema, warehouse, role, etc.
snowflake_url = URL(
    account         = os.environ["SNOWFLAKE_ACCOUNT"],
    user            = os.environ["SNOWFLAKE_USER"],
    password        = os.environ["SNOWFLAKE_PASSWORD"],
    database        = os.environ["SNOWFLAKE_DATABASE"],
    schema          = os.environ["SNOWFLAKE_SCHEMA"],
    warehouse       = os.environ["SNOWFLAKE_WAREHOUSE"],
    role            = os.environ.get("SNOWFLAKE_ROLE"),        # optional
    protocol        = "https",                                 # default
)

engine_sf = create_engine(snowflake_url, echo=False)
SessionSF = sessionmaker(bind=engine_sf)