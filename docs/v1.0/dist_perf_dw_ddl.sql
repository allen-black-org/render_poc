CREATE SCHEMA IF NOT EXISTS dist_perf_dw;

CREATE TABLE IF NOT EXISTS dist_perf_dw.dim_dates (
    id SERIAL PRIMARY KEY,
    full_date DATE NOT NULL,
    day_of_week_name TEXT,
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
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_full_date UNIQUE (full_date)
);
-----------------------------------------------------------------------------------------	
CREATE TABLE IF NOT EXISTS dist_perf_dw.dim_regions (
    id SERIAL PRIMARY KEY,
    region_name TEXT NOT NULL UNIQUE
);
-----------------------------------------------------------------------------------------	
CREATE TABLE IF NOT EXISTS dist_perf_dw.dim_territories (
    id SERIAL PRIMARY KEY,
	territory_name TEXT NOT NULL,
	territory_code TEXT NOT NULL,
    region_id INT REFERENCES dist_perf_dw.dim_regions(id),
    country_name TEXT NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT unique_territory UNIQUE (territory_name, region_id, country_name)
);
-----------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dist_perf_dw.dim_wholesalers (
    id SERIAL PRIMARY KEY,
    wholesaler_name TEXT NOT NULL,
    team_lead_id INT REFERENCES dist_perf_dw.dim_wholesalers(id),
    hire_date DATE NULL,
    territory_id INT REFERENCES dist_perf_dw.dim_territories(id),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-----------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dist_perf_dw.dim_firm_types (
    id SERIAL PRIMARY KEY,
    firm_type_name TEXT NOT NULL UNIQUE
);
-----------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dist_perf_dw.dim_firms (
    id SERIAL PRIMARY KEY,
    firm_name TEXT NOT NULL,
    firm_type_id INT REFERENCES dist_perf_dw.dim_firm_types(id),
    headquarters_city TEXT,
    headquarters_country TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_firm_name UNIQUE (firm_name)
);
-----------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dist_perf_dw.dim_channels (
    id SERIAL PRIMARY KEY,
    channel_name TEXT NOT NULL UNIQUE
);
-----------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dist_perf_dw.dim_advisors (
    id SERIAL PRIMARY KEY,
    advisor_name TEXT NOT NULL,
    region_id INT REFERENCES dist_perf_dw.dim_regions(id),
    channel_id INT REFERENCES dist_perf_dw.dim_channels(id),
    firm_id INT REFERENCES dist_perf_dw.dim_firms(id),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT unique_advisor_firm UNIQUE (advisor_name, firm_id)
);
-----------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dist_perf_dw.dim_asset_classes (
    id SERIAL PRIMARY KEY,
    asset_class_name TEXT NOT NULL UNIQUE
);
-----------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dist_perf_dw.dim_vehicle_types (
    id SERIAL PRIMARY KEY,
    vehicle_type_name TEXT NOT NULL UNIQUE
);
-----------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dist_perf_dw.dim_products (
    id SERIAL PRIMARY KEY,
    product_name TEXT NOT NULL,
    asset_class_id INT REFERENCES dist_perf_dw.dim_asset_classes(id),
    vehicle_type_id INT REFERENCES dist_perf_dw.dim_vehicle_types(id),
    base_fee_rate NUMERIC,
    launch_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_product_name UNIQUE (product_name)
);
-----------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dist_perf_dw.dim_expense_categories (
    id SERIAL PRIMARY KEY,
    category_name TEXT NOT NULL UNIQUE
);
-----------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dist_perf_dw.dim_expense_types (
    id SERIAL PRIMARY KEY,
    expense_type_name TEXT NOT NULL,
    expense_type_category_id INT REFERENCES dist_perf_dw.dim_expense_categories(id),
    is_fixed BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_expense_type_name UNIQUE (expense_type_name)
);
-----------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dist_perf_dw.dim_transaction_types (
    id SERIAL PRIMARY KEY,
    transaction_type_name TEXT NOT NULL UNIQUE,
    is_inflow BOOLEAN NOT NULL,
    description TEXT
);
-----------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dist_perf_dw.fact_aum_flows (
    id SERIAL PRIMARY KEY,
    date_id INT NOT NULL REFERENCES dist_perf_dw.dim_dates(id),
    wholesaler_id INT NOT NULL REFERENCES dist_perf_dw.dim_wholesalers(id),
    advisor_id INT NOT NULL REFERENCES dist_perf_dw.dim_advisors(id),
    product_id INT NOT NULL REFERENCES dist_perf_dw.dim_products(id),
    channel_id INT NOT NULL REFERENCES dist_perf_dw.dim_channels(id),
    transaction_type_id INT NOT NULL REFERENCES dist_perf_dw.dim_transaction_types(id),
    flow_amount NUMERIC NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-----------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dist_perf_dw.fact_retention_snapshots (
    flow_id INT REFERENCES dist_perf_dw.fact_aum_flows(id),
    snapshot_date_id INT REFERENCES dist_perf_dw.dim_dates(id),
    retained_amount NUMERIC NOT NULL,
	retention_pct NUMERIC,
	days_since_flow INT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (flow_id, snapshot_date_id)
);
-----------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dist_perf_dw.fact_revenue (
    id SERIAL PRIMARY KEY,
    flow_id INT NOT NULL REFERENCES dist_perf_dw.fact_aum_flows(id),
    product_id INT NOT NULL REFERENCES dist_perf_dw.dim_products(id),
	advisor_id INT REFERENCES dist_perf_dw.dim_advisors(id),
    fee_rate NUMERIC NOT NULL,
	is_estimate BOOLEAN DEFAULT FALSE,
    revenue_date_id INT REFERENCES dist_perf_dw.dim_dates(id),
    revenue_amount NUMERIC NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-----------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dist_perf_dw.fact_distribution_expense (
    id SERIAL PRIMARY KEY,
    wholesaler_id INT NOT NULL REFERENCES dist_perf_dw.dim_wholesalers(id),
    date_id INT NOT NULL REFERENCES dist_perf_dw.dim_dates(id),
    expense_type_id INT NOT NULL REFERENCES dist_perf_dw.dim_expense_types(id),
	is_adjustment BOOLEAN DEFAULT FALSE,
    expense_notes TEXT,
	expense_amount NUMERIC NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	UNIQUE (wholesaler_id, date_id, expense_type_id)
);
-----------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dist_perf_dw.fact_wholesaler_comp (
    id SERIAL PRIMARY KEY,
    wholesaler_id INT NOT NULL REFERENCES dist_perf_dw.dim_wholesalers(id),
    date_id INT NOT NULL REFERENCES dist_perf_dw.dim_dates(id),
    base_salary NUMERIC,
    incentive_comp NUMERIC,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-----------------------------------------------------------------------------------------
CREATE INDEX idx_flows_date_id ON dist_perf_dw.fact_aum_flows(date_id);
CREATE INDEX idx_flows_wholesaler_id ON dist_perf_dw.fact_aum_flows(wholesaler_id);
CREATE INDEX idx_flows_advisor_id ON dist_perf_dw.fact_aum_flows(advisor_id);
CREATE INDEX idx_flows_product_id ON dist_perf_dw.fact_aum_flows(product_id);

CREATE INDEX idx_expense_date_id ON dist_perf_dw.fact_distribution_expense(date_id);
CREATE INDEX idx_expense_wholesaler_id ON dist_perf_dw.fact_distribution_expense(wholesaler_id);
CREATE INDEX idx_expense_type_id ON dist_perf_dw.fact_distribution_expense(expense_type_id);

CREATE INDEX idx_retention_snap_id ON dist_perf_dw.fact_retention_snapshots(snapshot_date_id);

CREATE INDEX idx_revenue_product_id ON dist_perf_dw.fact_revenue(product_id);
CREATE INDEX idx_revenue_date_id ON dist_perf_dw.fact_revenue(revenue_date_id);