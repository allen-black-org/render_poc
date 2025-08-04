**Distribution BI Project Summary**

**Project Overview** The Distribution Performance BI application is designed to evaluate wholesaler performance using key metrics such as net retained AUM, aging-based retention rates, revenue contribution, and fee efficiency. It leverages a modern Python-based analytics stack with a PostgreSQL data warehouse, an ORM layer (SQLAlchemy), and a Flask web application serving interactive dashboards via Plotly.js.

**Primary Goals**

- Track and visualize net AUM flows over time
- Calculate retention cohorts (30/60/90/120 days)
- Compute revenue contribution (AUM × fee rate) and effective fee rates
- Provide lightweight, embeddable dashboards for stakeholders

**Tech Stack**

- **Database**: PostgreSQL Data Warehouse ("dist\_perf\_dw") hosted on Supabase
- **ORM**: SQLAlchemy models (defined in `models.py`, based on `dist_perf_dw_ddl.sql` schema)
- **Web Framework**: Flask (routes in `app.py`)
- **Visualization**: Plotly.js embedded in HTML templates (`retention_chart.html`)
- **Hosting**: Flask app deployed on Render (environment vars set in Render dashboard)
- **Local Dev**: Mini PC at `C:\Users\Allen\Projects\Distribtuion_Performance`
- **Secrets**: Managed via `.env` (ignored by Git) and Render environment variables
- **Infrastructure as Code**: dbt+Airbyte Snowflake guide (for reference, though currently using Supabase/Postgres)

**Repository & Directory Structure**

```
C:\Users\Allen\Projects\Distribtuion_Performance
├── app.py                   # Flask application and route definitions
├── models.py                # SQLAlchemy ORM model definitions
├── dist_perf_dw_ddl.sql     # Data warehouse DDL (tables, constraints)
├── Distribution_Performance_ERD.png  # ERD diagram (reference)
├── retention_chart.html     # Plotly.js chart template
├── requirements.txt         # Python dependencies (Flask, SQLAlchemy, psycopg2, python-dotenv)
├── project_directory_outline.txt     # Outline of anticipated file structure
├── orm_reference.md         # Notes on model relationships and join logic
├── Use_Case_Wholesaler_Effectiveness.pdf  # Business use case description
└── .env (git-ignored)       # Local environment variables (keys, passwords)
```

**Database Schema Highlights**

- **Dimension Tables**: `dim_wholesalers`, `dim_assets`, `dim_time` (date hierarchy)
- **Fact Tables**: `fact_aum_flow` (daily AUM changes), `fact_revenue`, `fact_expenses`
- **Retention Logic**: Cohorts defined by account open/renewal dates, calculated via SQL window functions or Python

**ORM Model Structure**

- `DimWholesaler`: wholesaler metadata
- `DimAsset`: asset classifications
- `DimTime`: calendar table
- `FactAUMFlow`: daily net inflows/outflows with foreign keys to dimensions
- `FactRevenue`: computed revenue events
- Relationships defined in `orm_reference.md`

**Application Flow**

1. Client requests dashboard (e.g., `/retention`) in Flask
2. Flask route queries the warehouse via SQLAlchemy, returns JSON
3. Frontend (HTML+JS) fetches JSON and renders Plotly chart
4. Users interact with cohorts and date filters in-browser

**Secrets & Deployment**

- **Local**: `.env` managed with `python-dotenv`, loaded in `config.py`
- **Render**: environment variables set in dashboard (SNOWFLAKE\_\*, SUPABASE\_URL, etc.)
- **Rotation**: Credentials rotated periodically; old secrets purged from Git history.

**Next Steps & Roadmap**

- Migrate ETL to dbt for transformation and testing
- Add user authentication & RBAC for dashboard access
- Integrate real-time alerts for KPI thresholds
- Expand to multi-warehouse support (e.g., Snowflake alongside Supabase)
- Containerize with Docker for reproducible dev environments

**Local Development**

1. Clone repo to `C:\Users\Allen\Projects\Distribtuion_Performance`
2. Create and activate virtualenv:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. Copy `.env.sample` → `.env`, fill in variables
4. Run Flask app:
   ```bash
   flask run
   # or
   python app.py
   ```
5. Open `http://localhost:5000/retention_chart.html` in browser

**Contact & References**

- ERD Diagram: `Distribution_Performance_ERD.png`
- Schema DDL: `dist_perf_dw_ddl.sql`
- ORM details: `orm_reference.md`
- Use Case: `Use_Case_Wholesaler_Effectiveness.pdf`

---

*Generated to serve as an at-a-glance reference for the Distribution BI stack and project structure.*

