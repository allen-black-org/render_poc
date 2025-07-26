-- Snowflake-compatible DDL refactored from PostgreSQL source
-- Replaces dist_perf_dw schema with dist_perf_db.dist_perf_schema
-- Adjustments for identity, data types, and constraints as needed

CREATE OR REPLACE DATABASE dist_perf_db;
USE DATABASE dist_perf_db;

CREATE OR REPLACE SCHEMA dist_perf_schema;
USE SCHEMA dist_perf_schema;

CREATE TABLE dist_perf_db.dist_perf_schema.dim_dates (
    id INT AUTOINCREMENT PRIMARY KEY,
    full_date DATE NOT NULL,
    day_of_week_name STRING,
    day_of_week_number INT,
    week_number INT,
    month_number INT,
    quarter_number INT,
    year_number INT,
    is_weekend BOOLEAN,
    is_month_start BOOLEAN,
    is_month_end BOOLEAN,
    is_quarter_start BOOLEAN,
    is_quarter_end BOOLEAN,
    is_year_start BOOLEAN,
    is_year_end BOOLEAN,
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    CONSTRAINT unique_full_date UNIQUE (full_date)
);

CREATE TABLE dist_perf_db.dist_perf_schema.dim_regions (
    id INT AUTOINCREMENT PRIMARY KEY,
    region_name STRING NOT NULL UNIQUE
);

CREATE TABLE dist_perf_db.dist_perf_schema.dim_accounts (
    id INT AUTOINCREMENT PRIMARY KEY,
    account_name STRING NOT NULL,
    account_code STRING NOT NULL,
    base_fee_rate NUMBER,
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    wholesaler_id INT,
    CONSTRAINT unique_account UNIQUE (account_name, account_code)
);

CREATE TABLE dist_perf_db.dist_perf_schema.dim_territories (
    id INT AUTOINCREMENT PRIMARY KEY,
    territory_name STRING NOT NULL,
    territory_code STRING NOT NULL,
    region_id INT,
    country_name STRING NOT NULL,
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    CONSTRAINT unique_territory UNIQUE (territory_name, region_id, country_name)
);

CREATE TABLE dist_perf_db.dist_perf_schema.dim_wholesalers (
    id INT AUTOINCREMENT PRIMARY KEY,
    wholesaler_name STRING NOT NULL,
    team_lead_id INT,
    hire_date DATE,
    territory_id INT,
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE dist_perf_db.dist_perf_schema.dim_firm_types (
    id INT AUTOINCREMENT PRIMARY KEY,
    firm_type_name STRING NOT NULL UNIQUE
);

CREATE TABLE dist_perf_db.dist_perf_schema.dim_firms (
    id INT AUTOINCREMENT PRIMARY KEY,
    firm_name STRING NOT NULL,
    firm_type_id INT,
    headquarters_city STRING,
    headquarters_country STRING,
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    CONSTRAINT unique_firm_name UNIQUE (firm_name)
);

CREATE TABLE dist_perf_db.dist_perf_schema.dim_channels (
    id INT AUTOINCREMENT PRIMARY KEY,
    channel_name STRING NOT NULL UNIQUE
);

CREATE TABLE dist_perf_db.dist_perf_schema.dim_advisors (
    id INT AUTOINCREMENT PRIMARY KEY,
    advisor_name STRING NOT NULL,
    region_id INT,
    channel_id INT,
    firm_id INT,
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    CONSTRAINT unique_advisor_firm UNIQUE (advisor_name, firm_id)
);

CREATE TABLE dist_perf_db.dist_perf_schema.dim_asset_classes (
    id INT AUTOINCREMENT PRIMARY KEY,
    asset_class_name STRING NOT NULL UNIQUE
);

CREATE TABLE dist_perf_db.dist_perf_schema.dim_vehicle_types (
    id INT AUTOINCREMENT PRIMARY KEY,
    vehicle_type_name STRING NOT NULL UNIQUE
);

CREATE TABLE dist_perf_db.dist_perf_schema.dim_products (
    id INT AUTOINCREMENT PRIMARY KEY,
    product_name STRING NOT NULL,
    asset_class_id INT,
    vehicle_type_id INT,
    launch_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    CONSTRAINT unique_product_name UNIQUE (product_name)
);

CREATE TABLE dist_perf_db.dist_perf_schema.dim_expense_categories (
    id INT AUTOINCREMENT PRIMARY KEY,
    category_name STRING NOT NULL UNIQUE
);

CREATE TABLE dist_perf_db.dist_perf_schema.dim_expense_types (
    id INT AUTOINCREMENT PRIMARY KEY,
    expense_type_name STRING NOT NULL,
    expense_type_category_id INT,
    is_fixed BOOLEAN,
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    CONSTRAINT unique_expense_type_name UNIQUE (expense_type_name)
);

CREATE TABLE dist_perf_db.dist_perf_schema.dim_transaction_types (
    id INT AUTOINCREMENT PRIMARY KEY,
    transaction_type_name STRING NOT NULL UNIQUE,
    is_inflow BOOLEAN NOT NULL,
    description STRING
);

CREATE TABLE dist_perf_db.dist_perf_schema.fact_aum_flows (
    id INT AUTOINCREMENT PRIMARY KEY,
    date_id INT NOT NULL,
    account_id INT,
    wholesaler_id INT NOT NULL,
    advisor_id INT NOT NULL,
    product_id INT NOT NULL,
    channel_id INT NOT NULL,
    transaction_type_id INT NOT NULL,
    flow_amount NUMBER NOT NULL,
    account_aum_amount NUMBER,
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE dist_perf_db.dist_perf_schema.fact_retention_snapshots (
    flow_id INT,
    snapshot_date_id INT,
    retained_amount NUMBER NOT NULL,
    retention_pct NUMBER,
    days_since_flow INT,
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (flow_id, snapshot_date_id, days_since_flow)
);

CREATE TABLE dist_perf_db.dist_perf_schema.fact_revenue (
    id INT AUTOINCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    product_id INT NOT NULL,
    wholesaler_id INT NOT NULL,
    revenue_date_id INT,
    fee_rate NUMBER NOT NULL,
    revenue_amount NUMBER NOT NULL,
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE dist_perf_db.dist_perf_schema.fact_distribution_expense (
    id INT AUTOINCREMENT PRIMARY KEY,
    wholesaler_id INT NOT NULL,
    date_id INT NOT NULL,
    expense_type_id INT NOT NULL,
    is_adjustment BOOLEAN DEFAULT FALSE,
    expense_notes STRING,
    expense_amount NUMBER NOT NULL,
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    CONSTRAINT unique_expense_entry UNIQUE (wholesaler_id, date_id, expense_type_id)
);

CREATE TABLE dist_perf_db.dist_perf_schema.fact_wholesaler_comp (
    id INT AUTOINCREMENT PRIMARY KEY,
    wholesaler_id INT NOT NULL,
    date_id INT NOT NULL,
    base_salary NUMBER,
    incentive_comp NUMBER,
    notes STRING,
    created_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP()
);
