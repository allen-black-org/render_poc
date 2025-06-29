from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, Date, Text, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# SQLAlchemy ORM base class
Base = declarative_base()

# Replace with your connection string
DATABASE_URL = (
    "postgresql+psycopg2://pocdb_te73_user:TnlIBboc9mOqMrXWiYd1hiseRWpiCbPN"
    "@dpg-d1djjc3ipnbc73dbvi6g-a.virginia-postgres.render.com/pocdb_te73"
)

# Create the engine and session
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

class DimAdvisors(Base):
    __tablename__ = "dim_advisors"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    advisor_name = Column(String)
    region_id = Column(Integer, ForeignKey("dist_perf_dw.dim_regions.id"))
    channel_id = Column(Integer, ForeignKey("dist_perf_dw.dim_channels.id"))
    firm_id = Column(Integer, ForeignKey("dist_perf_dw.dim_firms.id"))

    region = relationship("DimRegions", foreign_keys=[region_id])
    channel = relationship("DimChannels", foreign_keys=[channel_id])
    firm = relationship("DimFirms", foreign_keys=[firm_id])


class DimAssetClasses(Base):
    __tablename__ = "dim_asset_classes"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    asset_class_name = Column(String)


class DimChannels(Base):
    __tablename__ = "dim_channels"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    channel_name = Column(String)


class DimDates(Base):
    __tablename__ = "dim_dates"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    full_date = Column(Date)
    day_of_week = Column(Text)
    day_of_week_number = Column(Integer)
    week_number = Column(Integer)
    month_number = Column(Integer)
    quarter_number = Column(Integer)
    year_number = Column(Integer)
    is_weekend = Column(Boolean)
    is_month_start = Column(Boolean)
    is_month_end = Column(Boolean)
    is_quarter_start = Column(Boolean)
    is_quarter_end = Column(Boolean)
    is_year_start = Column(Boolean)
    is_year_end = Column(Boolean)


class DimExpenseCats(Base):
    __tablename__ = "dim_expense_categories"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    category_name = Column(String)


class DimExpenseTypes(Base):
    __tablename__ = "dim_expense_types"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    expense_type_name = Column(String)
    expense_type_category_id = Column(String,ForeignKey("dist_perf_dw.dim_expense_categories.id"))
    is_fixed = Column(Boolean)

    expense_type_category = relationship("DimExpenseCats", foreign_keys=[expense_type_category_id])


class DimFirmTypes(Base):
    __tablename__ = "dim_firm_types"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    firm_type_name = Column(String)



class DimFirms(Base):
    __tablename__ = "dim_firms"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    firm_name = Column(String)
    firm_type_id = Column(Integer, ForeignKey("dist_perf_dw.dim_firm_types.id"))
    headquarters_city = Column(String)
    headquarters_country = Column(String)

    firmtype = relationship("DimFirmTypes", foreign_keys=[firm_type_id])


class DimProducts(Base):
    __tablename__ = "dim_products"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    asset_class_id = Column(Integer, ForeignKey("dist_perf_dw.dim_asset_classes.id"))
    vehicle_type_id = Column(Integer, ForeignKey("dist_perf_dw.dim_vehicle_types.id"))
    base_fee_rate = Column(Numeric)
    launch_date = Column(Date)
    is_active = Column(Boolean)

    asset_class = relationship("DimAssetClasses", foreign_keys=[asset_class_id])
    vehicle_type = relationship("DimVehicles", foreign_keys=[vehicle_type_id])


class DimRegions(Base):
    __tablename__ = "dim_regions"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    region_name = Column(String)


class DimTerritories(Base):
    __tablename__ = "dim_territories"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    territory_name = Column(String)
    territory_code = Column(String)
    region_id = Column(Integer, ForeignKey("dist_perf_dw.dim_regions.id"))
    country_name = Column(String)

    terr_region = relationship("DimRegions", foreign_keys=[region_id])


class DimTransactionTypes(Base):
    __tablename__ = "dim_transaction_types"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    transaction_type_name = Column(String)


class DimVehicles(Base):
    __tablename__ = "dim_vehicle_types"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    vehicle_type_name = Column(String)


class DimWholesalers(Base):
    __tablename__ = "dim_wholesalers"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    wholesaler_name = Column(String)
    team_lead_id = Column(Numeric)
    hire_date = Column(Date)
    territory_id = Column(Numeric, ForeignKey("dist_perf_dw.dim_territories.id"))

    ws_territory = relationship("DimTerritories", foreign_keys=[territory_id])


class FactAUMFlow(Base):
    __tablename__ = "fact_aum_flows"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    date_id = Column(Integer, ForeignKey("dist_perf_dw.dim_dates.id"))
    product_id = Column(Integer, ForeignKey("dist_perf_dw.dim_products.id"))
    transaction_type_id = Column(Integer, ForeignKey("dist_perf_dw.dim_transaction_types.id"))
    flow_amount = Column(Numeric)

    year = relationship("DimDates", foreign_keys=[date_id])
    product = relationship("DimProducts", foreign_keys=[product_id])
    transaction_type = relationship("DimTransactionTypes", foreign_keys=[transaction_type_id])

class FactRetentionSnapshots(Base):
    __tablename__ = "fact_retention_snapshots"
    __table_args__ = {"schema": "dist_perf_dw"}

    flow_id = Column(Integer, ForeignKey("dist_perf_dw.fact_aum_flows.id"), primary_key=True)
    snapshot_date_id = Column(Integer, ForeignKey("dist_perf_dw.dim_dates.id"), primary_key=True)
    retained_amount = Column(Numeric)
    retention_pct = Column(Numeric)
    days_since_flow = Column(Integer)
    created_at = Column(Date)
    updated_at = Column(Date)

    flow = relationship("FactAUMFlow", foreign_keys=[flow_id])
    snapshot_date = relationship("DimDates", foreign_keys=[snapshot_date_id])


class FactRevenue(Base):
    __tablename__ = "fact_revenue"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    flow_id = Column(Integer, ForeignKey("dist_perf_dw.fact_aum_flows.id"))
    product_id = Column(Integer, ForeignKey("dist_perf_dw.dim_products.id"))
    advisor_id = Column(Integer, ForeignKey("dist_perf_dw.dim_advisors.id"))
    fee_rate = Column(Numeric)
    is_estimate = Column(Boolean, default=False)
    revenue_date_id = Column(Integer, ForeignKey("dist_perf_dw.dim_dates.id"))
    revenue_amount = Column(Numeric)
    created_at = Column(Date)
    updated_at = Column(Date)

    flow = relationship("FactAUMFlow", foreign_keys=[flow_id])
    product = relationship("DimProducts", foreign_keys=[product_id])
    advisor = relationship("DimAdvisors", foreign_keys=[advisor_id])
    revenue_date = relationship("DimDates", foreign_keys=[revenue_date_id])


class FactDistributionExpense(Base):
    __tablename__ = "fact_distribution_expense"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    wholesaler_id = Column(Integer, ForeignKey("dist_perf_dw.dim_wholesalers.id"))
    date_id = Column(Integer, ForeignKey("dist_perf_dw.dim_dates.id"))
    expense_type_id = Column(Integer, ForeignKey("dist_perf_dw.dim_expense_types.id"))
    is_adjustment = Column(Boolean, default=False)
    expense_notes = Column(Text)
    expense_amount = Column(Numeric)
    created_at = Column(Date)
    updated_at = Column(Date)

    wholesaler = relationship("DimWholesalers", foreign_keys=[wholesaler_id])
    date = relationship("DimDates", foreign_keys=[date_id])
    expense_type = relationship("DimExpenseTypes", foreign_keys=[expense_type_id])


class FactWholesalerComp(Base):
    __tablename__ = "fact_wholesaler_comp"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    wholesaler_id = Column(Integer, ForeignKey("dist_perf_dw.dim_wholesalers.id"))
    date_id = Column(Integer, ForeignKey("dist_perf_dw.dim_dates.id"))
    base_salary = Column(Numeric)
    incentive_comp = Column(Numeric)
    notes = Column(Text)
    created_at = Column(Date)
    updated_at = Column(Date)

    wholesaler = relationship("DimWholesalers", foreign_keys=[wholesaler_id])
    date = relationship("DimDates", foreign_keys=[date_id])