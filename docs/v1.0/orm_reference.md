
# ORM Reference – dist_perf_dw (v1.0)

This document outlines the SQLAlchemy ORM layer that maps to the PostgreSQL data warehouse schema `dist_perf_dw`. It provides class-based access to all dimension and fact tables for use in Flask routes, analytics, and programmatic queries.

---

## 🧱 Overview

- **Database**: PostgreSQL
- **Schema**: `dist_perf_dw`
- **ORM Tool**: SQLAlchemy
- **Code Location**: `models.py`
- **Class Convention**: Dimensions are prefixed with `Dim`, facts with `Fact`

---

## 📦 ORM Class Index

### Dimension Models

- `DimDates`: Calendar date breakdowns
- `DimRegions`: Geographic regions
- `DimChannels`: Distribution channels
- `DimFirms`: Advisory firms
- `DimFirmTypes`: Classification of firm types
- `DimAdvisors`: Financial advisors
- `DimProducts`: Investment products
- `DimAssetClasses`: Product asset categories
- `DimVehicleTypes`: Product vehicle structures
- `DimWholesalers`: Sales reps and teams
- `DimTerritories`: Sales geographies
- `DimExpenseCategories`: Expense grouping
- `DimExpenseTypes`: Specific expense entries
- `DimTransactionTypes`: Inflow/outflow transaction labels

### Fact Models

- `FactAUMFlow`: Core asset movement events
- `FactRetentionSnapshots`: Flow-level retention snapshots over time
- `FactRevenue`: Revenue generated from flows
- `FactDistributionExpense`: Wholesaler operating expenses
- `FactWholesalerComp`: Wholesaler base + incentive compensation

---

## 🧾 Table to ORM Class Mapping

| Table Name                         | ORM Class                | Description                          |
|------------------------------------|--------------------------|--------------------------------------|
| `dim_dates`                        | `DimDates`               | Date attributes and calendar flags   |
| `dim_regions`                      | `DimRegions`             | Geographic regions                   |
| `dim_channels`                     | `DimChannels`            | Distribution channels                |
| `dim_firms`                        | `DimFirms`               | Advisory firms                       |
| `dim_firm_types`                  | `DimFirmTypes`           | Type of advisory firm                |
| `dim_advisors`                     | `DimAdvisors`            | Financial advisors                   |
| `dim_products`                     | `DimProducts`            | Investment products                  |
| `dim_asset_classes`               | `DimAssetClasses`        | Product asset categories             |
| `dim_vehicle_types`               | `DimVehicleTypes`        | Product structures (e.g., ETF)       |
| `dim_wholesalers`                 | `DimWholesalers`         | Sales representatives                |
| `dim_territories`                 | `DimTerritories`         | Sales territory areas                |
| `dim_expense_categories`         | `DimExpenseCategories`   | Expense categories                   |
| `dim_expense_types`              | `DimExpenseTypes`        | Specific types of expenses           |
| `dim_transaction_types`          | `DimTransactionTypes`    | Types of flows (inflow, outflow)     |
| `fact_aum_flows`                 | `FactAUMFlow`            | Asset flows between parties          |
| `fact_retention_snapshots`       | `FactRetentionSnapshots` | Retention and aging of flows         |
| `fact_revenue`                   | `FactRevenue`            | Fee-based revenue generated          |
| `fact_distribution_expense`     | `FactDistributionExpense`| Operating expenses by wholesaler     |
| `fact_wholesaler_comp`          | `FactWholesalerComp`     | Compensation (salary + incentive)    |

---

## 🔗 Relationship Notes

- All relationships are one-way for now (no `back_populates`)
- Class names are referenced as strings inside `relationship()` to allow flexible ordering
- All foreign keys are schema-qualified
- Column data types are aligned to schema (e.g., `Integer`, `Numeric`, `Boolean`, `Text`)

---

## 🧠 ORM Usage Tips

- Use `session.query(...)` with `.join()` to combine tables
- Filter using class properties, not raw column strings:
  ```python
  session.query(FactRevenue).filter(FactRevenue.is_estimate == False)
  ```
- Relationships allow attribute access like:
  ```python
  flow.product.product_name
  advisor.firm.firm_type.firm_type_name
  ```

---
