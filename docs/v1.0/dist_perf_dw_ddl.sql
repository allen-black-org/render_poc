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
CREATE TABLE dist_perf_dw.dim_accounts (
	id serial4 NOT NULL,
	account_name text NOT NULL,
	account_code text NOT NULL,
	base_fee_rate numeric NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	wholesaler_id int4 NULL,
	CONSTRAINT dim_accounts_pkey PRIMARY KEY (id),
	CONSTRAINT unique_account UNIQUE (account_name, account_code)
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
CREATE TABLE dist_perf_dw.fact_aum_flows (
	id serial4 NOT NULL,
	date_id int4 NOT NULL,
	account_id int4 NULL,
	wholesaler_id int4 NOT NULL,
	advisor_id int4 NOT NULL,
	product_id int4 NOT NULL,
	channel_id int4 NOT NULL,
	transaction_type_id int4 NOT NULL,
	flow_amount numeric NOT NULL,
	account_aum_amount NUMERIC,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT fact_aum_flows_pkey PRIMARY KEY (id)
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
    PRIMARY KEY (flow_id, snapshot_date_id, days_since_flow)
);
-----------------------------------------------------------------------------------------
CREATE TABLE dist_perf_dw.fact_revenue (
	id serial4 NOT NULL,
	account_id int4 NOT NULL,
	product_id int4 NOT NULL,
	wholesaler_id int4 NOT NULL,
	revenue_date_id int4 NULL,
	fee_rate numeric NOT NULL,
	revenue_amount numeric NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT fact_revenue_pkey PRIMARY KEY (id)
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

ALTER TABLE dist_perf_dw.dim_accounts ADD CONSTRAINT dim_accounts_wholesaler_fkey FOREIGN KEY (wholesaler_id) REFERENCES dist_perf_dw.dim_wholesalers(id);

ALTER TABLE dist_perf_dw.dim_advisors ADD CONSTRAINT dim_advisors_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES dist_perf_dw.dim_channels(id);
ALTER TABLE dist_perf_dw.dim_advisors ADD CONSTRAINT dim_advisors_firm_id_fkey FOREIGN KEY (firm_id) REFERENCES dist_perf_dw.dim_firms(id);
ALTER TABLE dist_perf_dw.dim_advisors ADD CONSTRAINT dim_advisors_region_id_fkey FOREIGN KEY (region_id) REFERENCES dist_perf_dw.dim_regions(id);

ALTER TABLE dist_perf_dw.dim_expense_types ADD CONSTRAINT dim_expense_types_expense_type_category_id_fkey FOREIGN KEY (expense_type_category_id) REFERENCES dist_perf_dw.dim_expense_categories(id);

ALTER TABLE dist_perf_dw.dim_firms ADD CONSTRAINT dim_firms_firm_type_id_fkey FOREIGN KEY (firm_type_id) REFERENCES dist_perf_dw.dim_firm_types(id);

ALTER TABLE dist_perf_dw.dim_products ADD CONSTRAINT dim_products_asset_class_id_fkey FOREIGN KEY (asset_class_id) REFERENCES dist_perf_dw.dim_asset_classes(id);
ALTER TABLE dist_perf_dw.dim_products ADD CONSTRAINT dim_products_vehicle_type_id_fkey FOREIGN KEY (vehicle_type_id) REFERENCES dist_perf_dw.dim_vehicle_types(id);

ALTER TABLE dist_perf_dw.dim_territories ADD CONSTRAINT dim_territories_region_id_fkey FOREIGN KEY (region_id) REFERENCES dist_perf_dw.dim_regions(id);

ALTER TABLE dist_perf_dw.dim_wholesalers ADD CONSTRAINT dim_wholesalers_team_lead_id_fkey FOREIGN KEY (team_lead_id) REFERENCES dist_perf_dw.dim_wholesalers(id);
ALTER TABLE dist_perf_dw.dim_wholesalers ADD CONSTRAINT dim_wholesalers_territory_id_fkey FOREIGN KEY (territory_id) REFERENCES dist_perf_dw.dim_territories(id);

ALTER TABLE dist_perf_dw.fact_aum_flows ADD CONSTRAINT fact_aum_flows_account_id_fkey FOREIGN KEY (account_id) REFERENCES dist_perf_dw.dim_accounts(id);
ALTER TABLE dist_perf_dw.fact_aum_flows ADD CONSTRAINT fact_aum_flows_advisor_id_fkey FOREIGN KEY (advisor_id) REFERENCES dist_perf_dw.dim_advisors(id);
ALTER TABLE dist_perf_dw.fact_aum_flows ADD CONSTRAINT fact_aum_flows_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES dist_perf_dw.dim_channels(id);
ALTER TABLE dist_perf_dw.fact_aum_flows ADD CONSTRAINT fact_aum_flows_date_id_fkey FOREIGN KEY (date_id) REFERENCES dist_perf_dw.dim_dates(id);
ALTER TABLE dist_perf_dw.fact_aum_flows ADD CONSTRAINT fact_aum_flows_product_id_fkey FOREIGN KEY (product_id) REFERENCES dist_perf_dw.dim_products(id);
ALTER TABLE dist_perf_dw.fact_aum_flows ADD CONSTRAINT fact_aum_flows_transaction_type_id_fkey FOREIGN KEY (transaction_type_id) REFERENCES dist_perf_dw.dim_transaction_types(id);
ALTER TABLE dist_perf_dw.fact_aum_flows ADD CONSTRAINT fact_aum_flows_wholesaler_id_fkey FOREIGN KEY (wholesaler_id) REFERENCES dist_perf_dw.dim_wholesalers(id);

ALTER TABLE dist_perf_dw.fact_distribution_expense ADD CONSTRAINT fact_distribution_expense_date_id_fkey FOREIGN KEY (date_id) REFERENCES dist_perf_dw.dim_dates(id);
ALTER TABLE dist_perf_dw.fact_distribution_expense ADD CONSTRAINT fact_distribution_expense_expense_type_id_fkey FOREIGN KEY (expense_type_id) REFERENCES dist_perf_dw.dim_expense_types(id);
ALTER TABLE dist_perf_dw.fact_distribution_expense ADD CONSTRAINT fact_distribution_expense_wholesaler_id_fkey FOREIGN KEY (wholesaler_id) REFERENCES dist_perf_dw.dim_wholesalers(id);

ALTER TABLE dist_perf_dw.fact_retention_snapshots ADD CONSTRAINT fact_retention_snapshots_flow_id_fkey FOREIGN KEY (flow_id) REFERENCES dist_perf_dw.fact_aum_flows(id);
ALTER TABLE dist_perf_dw.fact_retention_snapshots ADD CONSTRAINT fact_retention_snapshots_snapshot_date_id_fkey FOREIGN KEY (snapshot_date_id) REFERENCES dist_perf_dw.dim_dates(id);

ALTER TABLE dist_perf_dw.fact_revenue ADD CONSTRAINT fact_revenue_account_id_fkey FOREIGN KEY (account_id) REFERENCES dist_perf_dw.dim_accounts(id);
ALTER TABLE dist_perf_dw.fact_revenue ADD CONSTRAINT fact_revenue_product_id_fkey FOREIGN KEY (product_id) REFERENCES dist_perf_dw.dim_products(id);
ALTER TABLE dist_perf_dw.fact_revenue ADD CONSTRAINT fact_revenue_revenue_date_id_fkey FOREIGN KEY (revenue_date_id) REFERENCES dist_perf_dw.dim_dates(id);
ALTER TABLE dist_perf_dw.fact_revenue ADD CONSTRAINT fact_revenue_wholesaler_id_fkey FOREIGN KEY (wholesaler_id) REFERENCES dist_perf_dw.dim_wholesalers(id);

ALTER TABLE dist_perf_dw.fact_wholesaler_comp ADD CONSTRAINT fact_wholesaler_comp_date_id_fkey FOREIGN KEY (date_id) REFERENCES dist_perf_dw.dim_dates(id);
ALTER TABLE dist_perf_dw.fact_wholesaler_comp ADD CONSTRAINT fact_wholesaler_comp_wholesaler_id_fkey FOREIGN KEY (wholesaler_id) REFERENCES dist_perf_dw.dim_wholesalers(id);