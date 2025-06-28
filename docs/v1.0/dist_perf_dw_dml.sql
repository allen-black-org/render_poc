INSERT INTO dist_perf_dw.dim_dates (
    full_date,
    day_of_week_name,
    day_of_week_number,
    week_number,
    month_number,
    quarter_number,
    year_number,
    is_weekend,
    is_month_start,
    is_month_end,
    is_quarter_start,
    is_quarter_end,
    is_year_start,
is_year_end
)
SELECT
    d::DATE AS full_date,
    TO_CHAR(d, 'Day') AS day_of_week_name,
    EXTRACT(ISODOW FROM d)::INT AS day_of_week_number,
    EXTRACT(WEEK FROM d)::INT AS week_number,
    EXTRACT(MONTH FROM d)::INT AS month_number,
    EXTRACT(QUARTER FROM d)::INT AS quarter_number,
    EXTRACT(YEAR FROM d)::INT AS year_number,
    EXTRACT(ISODOW FROM d) IN (6,7) AS is_weekend,
    d = DATE_TRUNC('month', d)::DATE AS is_month_start,
    d = (DATE_TRUNC('month', d) + INTERVAL '1 MONTH - 1 day')::DATE AS is_month_end,
    d = DATE_TRUNC('quarter', d)::DATE AS is_quarter_start,
    d = (DATE_TRUNC('quarter', d) + INTERVAL '3 MONTH - 1 day')::DATE AS is_quarter_end,
    d = DATE_TRUNC('year', d)::DATE AS is_year_start,
    d = (DATE_TRUNC('year', d) + INTERVAL '1 YEAR - 1 day')::DATE AS is_year_end
FROM
    generate_series(DATE '2020-01-01', DATE '2030-12-31', INTERVAL '1 day') AS d;
-----------------------------------------------------------------------------------------	
INSERT INTO dist_perf_dw.dim_regions (region_name) VALUES
('Northeast'),
('Southeast'),
('Midwest'),
('Southwest'),
('West Coast'),
('Mountain'),
('Eastern Canada'),
('Western Canada'),
('Northern UK'),
('Southern UK');
-----------------------------------------------------------------------------------------	
INSERT INTO dist_perf_dw.dim_territories (territory_name, territory_code, region_id, country_name) VALUES
('Northeast Territory', 'NE01', 1, 'United States'),
('Southeast Territory', 'SE01', 2, 'United States'),
('Midwest Territory', 'MW01', 3, 'United States'),
('Southwest Territory', 'SW01', 4, 'United States'),
('West Coast Territory', 'WC01', 5, 'United States'),
('Mountain Territory', 'MT01', 6, 'United States'),
('Canada East', 'CA01', 7, 'Canada'),
('Canada West', 'CA02', 8, 'Canada'),
('United Kingdom - North', 'UK01', 9, 'United Kingdom'),
('United Kingdom - South', 'UK02', 10, 'United Kingdom');
-----------------------------------------------------------------------------------------
-- === Team Leads ===
INSERT INTO dist_perf_dw.dim_wholesalers (wholesaler_name, hire_date, territory_id)
VALUES
('Alice Thompson', '2015-06-15', 1),  -- NE01
('Brian Delgado', '2016-03-22', 2),  -- SE01
('Charlotte Lin', '2017-08-10', 3),  -- MW01
('David Osei', '2018-02-28', 4),     -- SW01
('Eva Morales', '2014-11-05', 5);    -- WC01

-- After inserting team leads, capture their IDs (assuming SERIAL starts at 1):
-- Alice → id 1
-- Brian → id 2
-- Charlotte → id 3
-- David → id 4
-- Eva → id 5

-- === Team Members ===
INSERT INTO dist_perf_dw.dim_wholesalers (wholesaler_name, team_lead_id, hire_date, territory_id)
VALUES
('Frank Nguyen', 1, '2020-01-15', 1),
('Grace Kim', 1, '2021-04-10', 1),
('Hassan Patel', 2, '2019-09-23', 2),
('Isla Roberts', 2, '2022-01-03', 2),
('Jamal Singh', 3, '2020-06-12', 3),
('Kara Lopez', 3, '2021-11-19', 3),
('Liam Walker', 4, '2022-07-01', 4),
('Maya Davis', 5, '2021-03-27', 5);
-----------------------------------------------------------------------------------------
INSERT INTO dist_perf_dw.dim_firm_types (firm_type_name) VALUES
('RIA'),
('Broker/Dealer'),
('Bank'),
('Wirehouse'),
('Insurance'),
('Asset Manager'),
('Hybrid');
-----------------------------------------------------------------------------------------
INSERT INTO dist_perf_dw.dim_firms (firm_name, firm_type_id, headquarters_city, headquarters_country)
VALUES
('Summit Wealth Advisors', 1, 'Denver', 'United States'),            -- RIA
('First National Brokerage', 2, 'Atlanta', 'United States'),         -- Broker/Dealer
('Crescent Bank & Trust', 3, 'New Orleans', 'United States'),        -- Bank
('Horizon Wealth Group', 4, 'New York', 'United States'),            -- Wirehouse
('Guardian Insurance Co.', 5, 'Chicago', 'United States'),           -- Insurance
('Apex Asset Management', 6, 'Toronto', 'Canada'),                   -- Asset Manager
('NorthStar Financial Partners', 7, 'San Francisco', 'United States'), -- Hybrid
('TrueNorth Advisory', 1, 'Boston', 'United States'),                -- RIA
('WestPoint Investment Group', 2, 'Dallas', 'United States'),        -- Broker/Dealer
('SilverRock Capital', 6, 'London', 'United Kingdom');               -- Asset Manager
-----------------------------------------------------------------------------------------
INSERT INTO dist_perf_dw.dim_channels (channel_name) VALUES
('RIA'),
('Wirehouse'),
('Bank'),
('Independent Broker/Dealer'),
('Insurance'),
('Institutional'),
('Hybrid'),
('Family Office'),
('Private Bank');
-----------------------------------------------------------------------------------------
INSERT INTO dist_perf_dw.dim_advisors (advisor_name, region_id, channel_id, firm_id)
VALUES
('Alan Rivera', 1, 1, 1),  -- RIA in Northeast at Summit
('Bethany Carter', 1, 4, 2),  -- IBD in Northeast at First National
('Caleb Zhang', 2, 3, 3),  -- Bank in Southeast at Crescent
('Dana Moore', 2, 2, 4),  -- Wirehouse in Southeast at Horizon
('Eli Thompson', 3, 5, 5),  -- Insurance in Midwest at Guardian
('Farrah Patel', 3, 1, 1),  -- RIA in Midwest at Summit
('Gabe Hernandez', 4, 4, 2),  -- IBD in Southwest at First National
('Holly Chen', 4, 6, 6),  -- Institutional in Southwest at Apex
('Ivan Novak', 5, 7, 7),  -- Hybrid in West Coast at NorthStar
('Jasmine Lee', 5, 1, 8); -- RIA in West Coast at TrueNorth
-----------------------------------------------------------------------------------------
INSERT INTO dist_perf_dw.dim_asset_classes (asset_class_name) VALUES
('Equity'),
('Fixed Income'),
('Multi-Asset'),
('Alternative'),
('Real Estate'),
('Commodities'),
('Cash');
-----------------------------------------------------------------------------------------
INSERT INTO dist_perf_dw.dim_vehicle_types (vehicle_type_name) VALUES
('Mutual Fund'),
('ETF'),
('SMA'),  -- Separately Managed Account
('CIT'),  -- Collective Investment Trust
('Hedge Fund'),
('Private Equity'),
('Model Portfolio');
-----------------------------------------------------------------------------------------
INSERT INTO dist_perf_dw.dim_products (
    product_name,
    asset_class_id,
    vehicle_type_id,
    base_fee_rate,
    launch_date,
    is_active
)
VALUES
('Alpha Growth Fund', 1, 1, 0.0075, '2018-05-01', TRUE),
('Beta Income Strategy', 2, 3, 0.0050, '2016-11-15', TRUE),
('Gamma All Asset ETF', 3, 2, 0.0040, '2020-02-20', TRUE),
('Delta Real Estate Trust', 5, 4, 0.0065, '2014-07-10', TRUE),
('Omega Commodity Tracker', 6, 2, 0.0080, '2019-03-01', TRUE),
('Zeta Private Equity Fund', 4, 6, 0.0200, '2012-01-01', FALSE), -- inactive
('Sigma Model Portfolio', 3, 7, 0.0030, '2021-08-05', TRUE),
('Theta Cash Reserve', 7, 1, 0.0010, '2022-10-01', TRUE);
-----------------------------------------------------------------------------------------
INSERT INTO dist_perf_dw.dim_expense_categories (category_name) VALUES
('Sales'),
('Marketing'),
('Technology'),
('Operations'),
('Travel'),
('Administrative'),
('Consulting');
-----------------------------------------------------------------------------------------
INSERT INTO dist_perf_dw.dim_expense_types (expense_type_name, expense_type_category_id, is_fixed)
VALUES
('CRM Subscription', 3, TRUE),         -- Technology
('Airfare', 5, FALSE),                 -- Travel
('Hotel', 5, FALSE),                   -- Travel
('Meals & Entertainment', 1, FALSE),  -- Sales
('Web Advertising', 2, FALSE),        -- Marketing
('Lead List Purchase', 2, FALSE),     -- Marketing
('Internal Reporting Tools', 3, TRUE),-- Technology
('Consulting Fees', 7, FALSE),        -- Consulting
('Office Rent', 4, TRUE),             -- Operations
('Admin Support Contract', 6, TRUE);  -- Administrative
-----------------------------------------------------------------------------------------
INSERT INTO dist_perf_dw.dim_transaction_types (transaction_type_name, is_inflow, description) VALUES
('Inflow', TRUE, 'New contributions or purchases from investors'),
('Outflow', FALSE, 'Withdrawals, redemptions, or liquidations'),
('Transfer In', TRUE, 'Internal or external transfers into a product or account'),
('Transfer Out', FALSE, 'Internal or external transfers out of a product or account'),
('Reinvestment', TRUE, 'Automatic reinvestment of dividends or distributions'),
('Fee Withdrawal', FALSE, 'Assets deducted to pay management or service fees'),
('Adjustment', TRUE, 'Manual or data-driven correction of reported flows'),
('Chargeback', FALSE, 'Reversal of prior inflows or commissions due to clawbacks or cancellations');
-----------------------------------------------------------------------------------------
INSERT INTO dist_perf_dw.fact_aum_flows (
    date_id, wholesaler_id, advisor_id, product_id,
    channel_id, transaction_type_id, flow_amount
)
VALUES
(1, 1, 1, 1, 1, 1, 500000.00),   -- Inflow from Alan Rivera into Alpha Growth Fund
(1, 1, 1, 1, 1, 2, -100000.00),  -- Outflow same day (net +400k)
(2, 2, 2, 2, 2, 1, 250000.00),   -- Inflow into Beta Income Strategy via IBD
(2, 2, 2, 2, 2, 4, -50000.00),   -- Transfer out
(3, 1, 1, 1, 1, 3, 150000.00),   -- Transfer in to Alpha Growth Fund
(3, 1, 1, 1, 1, 5, 50000.00);    -- Reinvestment into Alpha Growth Fund
-----------------------------------------------------------------------------------------
-- flow_id 1: $500,000 inflow
INSERT INTO dist_perf_dw.fact_retention_snapshots (
    flow_id, snapshot_date_id, retained_amount, retention_pct, days_since_flow
) VALUES
(1, 1, 500000.00, 1.00, 0),
(1, 4, 450000.00, 0.90, 30),
(1, 5, 375000.00, 0.75, 60);

-- flow_id 2: $100,000 outflow — nothing to retain
INSERT INTO dist_perf_dw.fact_retention_snapshots (
    flow_id, snapshot_date_id, retained_amount, retention_pct, days_since_flow
) VALUES
(2, 1, 0.00, 0.00, 0),
(2, 4, 0.00, 0.00, 30),
(2, 5, 0.00, 0.00, 60);

-- flow_id 3: $250,000 inflow
INSERT INTO dist_perf_dw.fact_retention_snapshots (
    flow_id, snapshot_date_id, retained_amount, retention_pct, days_since_flow
) VALUES
(3, 2, 250000.00, 1.00, 0),
(3, 4, 240000.00, 0.96, 15),
(3, 5, 210000.00, 0.84, 45);

-- flow_id 6: $50,000 reinvestment
INSERT INTO dist_perf_dw.fact_retention_snapshots (
    flow_id, snapshot_date_id, retained_amount, retention_pct, days_since_flow
) VALUES
(6, 3, 50000.00, 1.00, 0),
(6, 4, 49500.00, 0.99, 30),
(6, 5, 48000.00, 0.96, 60);
-----------------------------------------------------------------------------------------
INSERT INTO dist_perf_dw.fact_revenue (
    flow_id, product_id, revenue_date_id, fee_rate, revenue_amount
)
VALUES
-- Alpha Growth Fund: $500k @ 0.75%
(1, 1, 1, 0.0075, 3750.00),

-- Beta Income Strategy: $250k @ 0.50%
(3, 2, 2, 0.0050, 1250.00),

-- Reinvestment into Alpha Growth: $50k @ 0.75%
(6, 1, 3, 0.0075, 375.00);
-----------------------------------------------------------------------------------------
-- Alice Thompson's travel and tech costs
INSERT INTO dist_perf_dw.fact_distribution_expense (
    wholesaler_id, date_id, expense_type_id, expense_amount, is_adjustment, expense_notes
) VALUES
(1, 1, 1, 425.00, FALSE, 'Flight to New York for client meeting'),
(1, 1, 2, 145.25, FALSE, 'Dinner with advisors post-meeting'),
(1, 2, 3, 89.99, FALSE, 'Monthly CRM subscription'),
(1, 3, 4, 320.00, FALSE, '2-night stay at Marriott Chicago');

-- Brian Delgado's expense, including adjustment
INSERT INTO dist_perf_dw.fact_distribution_expense (
    wholesaler_id, date_id, expense_type_id, expense_amount, is_adjustment, expense_notes
) VALUES
(2, 1, 5, 1000.00, FALSE, 'Consulting for pitch material redesign'),
(2, 2, 5, -250.00, TRUE, 'Partial refund due to scope change');
-----------------------------------------------------------------------------------------
-- Alice: consistent salary, moderate incentive growth
INSERT INTO dist_perf_dw.fact_wholesaler_comp (wholesaler_id, date_id, base_salary, incentive_comp, notes) VALUES
(1, 1, 10000.00, 2000.00, 'January base + incentive based on Q4 flows'),
(1, 4, 10000.00, 2500.00, 'February incentive bump after large new account'),
(1, 7, 10000.00, 3000.00, 'March payout includes early Q1 bonus');

-- Brian: same base, incentive spike in February
INSERT INTO dist_perf_dw.fact_wholesaler_comp (wholesaler_id, date_id, base_salary, incentive_comp, notes) VALUES
(2, 1, 9500.00, 1800.00, 'Baseline month'),
(2, 4, 9500.00, 4000.00, 'High incentive from territory-wide conversion effort'),
(2, 7, 9500.00, 2200.00, 'Returned to normal performance');
-----------------------------------------------------------------------------------------