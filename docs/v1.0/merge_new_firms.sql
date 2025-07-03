MERGE INTO dist_perf_dw.dim_firms AS dest
USING (
select 1 AS ID, 'CASSA RAIFFEISEN BASSA ATESINA (IN LINGUA TEDESCA RAIFFEISENKASSE UNTERLAND)' AS firm_name, 4 AS firm_type_id, 'Saint Augustine' AS firm_city, 'United States' AS firm_country, current_timestamp AS created_at, current_timestamp AS updated_at UNION
select 2, 'BRANCH CapitalING & TRUST COMPANY', 5, 'New York City', 'United States', current_timestamp, current_timestamp UNION
select 3, 'Saldo Capital UAB', 3, 'New York City', 'United States', current_timestamp, current_timestamp UNION
select 4, 'FIRST SAVINGS Capital', 4, 'Tacoma', 'United States', current_timestamp, current_timestamp UNION
select 5, 'Caixa Geral de Depósitos, S.A.', 3, 'Harrisburg', 'United States', current_timestamp, current_timestamp UNION
select 6, 'VolksCapital Vechta eG', 1, 'Garland', 'United States', current_timestamp, current_timestamp UNION
select 7, 'SOCIETA PER AZIONI', 1, 'Houston', 'United States', current_timestamp, current_timestamp UNION
select 8, 'MCE Capital GmbH', 1, 'San Diego', 'United States', current_timestamp, current_timestamp UNION
select 9, 'CITIZENS Capital', 5, 'North Little Rock', 'United States', current_timestamp, current_timestamp UNION
select 10, 'CORNERSTONE Wealth', 1, 'Huntsville', 'United States', current_timestamp, current_timestamp UNION
select 11, 'FIRST MIDWEST Wealth', 1, 'Boise', 'United States', current_timestamp, current_timestamp UNION
select 12, 'FNZ Wealth SE', 1, 'San Diego', 'United States', current_timestamp, current_timestamp UNION
select 13, 'Compagnie générale de location équipements "C.G.L."', 2, 'Ocala', 'United States', current_timestamp, current_timestamp UNION
select 14, 'BMO HARRIS Wealth', 1, 'Las Cruces', 'United States', current_timestamp, current_timestamp UNION
select 15, 'Wealth OF AMERICA', 2, 'Amarillo', 'United States', current_timestamp, current_timestamp UNION
select 16, 'UNITED COMMUNITY Wealth', 1, 'Saint Louis', 'United States', current_timestamp, current_timestamp UNION
select 17, 'The Wealth of New York Mellon SA/NV, Amsterdam Branch', 4, 'Austin', 'United States', current_timestamp, current_timestamp UNION
select 18, 'CAPITAL CITY Wealth', 2, 'Jacksonville', 'United States', current_timestamp, current_timestamp UNION
select 19, 'COMMUNITY FIRST Partners', 6, 'Birmingham', 'United States', current_timestamp, current_timestamp UNION
select 20, 'TD Partners', 1, 'Cincinnati', 'United States', current_timestamp, current_timestamp UNION
select 21, 'North Advisory', 5, 'Denver', 'United States', current_timestamp, current_timestamp UNION
select 22, 'CITIZENS NATIONAL Partners', 4, 'Washington', 'United States', current_timestamp, current_timestamp UNION
select 23, 'FIRST COMMUNITY Partners', 4, 'Beaumont', 'United States', current_timestamp, current_timestamp UNION
select 24, 'Partners Spółdzielczy w Głownie', 7, 'Carlsbad', 'United States', current_timestamp, current_timestamp UNION
select 25, 'PNC Partners', 7, 'Louisville', 'United States', current_timestamp, current_timestamp UNION
select 26, 'BANCO BPM SOCIETA ', 7, 'Pasadena', 'United States', current_timestamp, current_timestamp UNION
select 27, 'BMO HARRIS Group', 3, 'Austin', 'United States', current_timestamp, current_timestamp UNION
select 28, 'CASSA RURALE DI LEDRO - BANCA DI CREDITO COOPERATIVO - SOCIETA COOPERATIVA', 4, 'Denver', 'United States', current_timestamp, current_timestamp UNION
select 29, 'BULGARIAN DEVELOPMENT Group', 7, 'Midland', 'United States', current_timestamp, current_timestamp UNION
select 30, 'FIRST STATE Group', 1, 'Dallas', 'United States', current_timestamp, current_timestamp) AS src

ON (src.id = dest.id)

WHEN MATCHED THEN 
	UPDATE
		SET firm_name = src.firm_name
			, firm_type_id = src.firm_type_id
			, headquarters_city = src.firm_city
			, headquarters_country = src.firm_country
			, updated_at = current_timestamp
			
WHEN NOT MATCHED THEN
	INSERT (firm_name
			,firm_type_id
			,headquarters_city
			,headquarters_country
			,created_at
			,updated_at)
	VALUES (src.firm_name
			, src.firm_type_id
			, src.firm_city
			, src.firm_country
			, current_timestamp
			, NULL
			);