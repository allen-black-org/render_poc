import os
from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, Date, Text, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from connections import SnowflakeBase
"""-----------------------------------------------------------------------------------------------------------------"""
class DimAccountsSF(SnowflakeBase):
    __tablename__ = "dim_accounts"

    id = Column(Integer, primary_key=True)
    account_name = Column(String)
    account_code = Column(String)
    base_fee_rate = Column(Numeric)
    base_fee_amount = Column(Numeric)
"""-----------------------------------------------------------------------------------------------------------------"""
class DimAssetClassesSF(SnowflakeBase):
    __tablename__ = "dim_asset_classes"

    id = Column(Integer, primary_key=True)
    asset_class_name = Column(String)
"""-----------------------------------------------------------------------------------------------------------------"""
class DimDatesSF(SnowflakeBase):
    __tablename__ = "dim_dates"

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
"""-----------------------------------------------------------------------------------------------------------------"""
class DimExpenseCatsSF(SnowflakeBase):
    __tablename__ = "dim_expense_categories"

    id = Column(Integer, primary_key=True)
    category_name = Column(String)
"""-----------------------------------------------------------------------------------------------------------------"""
class DimExpenseTypesSF(SnowflakeBase):
    __tablename__ = "dim_expense_types"

    id = Column(Integer, primary_key=True)
    expense_type_name = Column(String)
    expense_type_category_id = Column(String,ForeignKey("dim_expense_categories.id"))
    is_fixed = Column(Boolean)

    expense_type_category = relationship("DimExpenseCatsSF", foreign_keys=[expense_type_category_id])
"""-----------------------------------------------------------------------------------------------------------------"""
class DimRegionsSF(SnowflakeBase):
    __tablename__ = "dim_regions"

    id = Column(Integer, primary_key=True)
    region_name = Column(String)
"""-----------------------------------------------------------------------------------------------------------------"""
class DimChannelsSF(SnowflakeBase):
    __tablename__ = "dim_channels"

    id = Column(Integer, primary_key=True)
    channel_name = Column(String)
"""-----------------------------------------------------------------------------------------------------------------"""
class DimFirmTypesSF(SnowflakeBase):
    __tablename__ = "dim_firm_types"

    id = Column(Integer, primary_key=True)
    firm_type_name = Column(String)
"""-----------------------------------------------------------------------------------------------------------------"""
class DimFirmsSF(SnowflakeBase):
    __tablename__ = "dim_firms"

    id = Column(Integer, primary_key=True)
    firm_name = Column(String)
    firm_type_id = Column(Integer, ForeignKey("dim_firm_types.id"))
    headquarters_city = Column(String)
    headquarters_country = Column(String)

    firmtype = relationship("DimFirmTypesSF", foreign_keys=[firm_type_id])
"""-----------------------------------------------------------------------------------------------------------------"""
class DimAdvisorsSF(SnowflakeBase):
    __tablename__ = "dim_advisors"

    id = Column(Integer, primary_key=True)
    advisor_name = Column(String)
    region_id = Column(Integer, ForeignKey("dim_regions.id"))
    channel_id = Column(Integer, ForeignKey("dim_channels.id"))
    firm_id = Column(Integer, ForeignKey("dim_firms.id"))

    region = relationship("DimRegionsSF", foreign_keys=[region_id])
    channel = relationship("DimChannelsSF", foreign_keys=[channel_id])
    firm = relationship("DimFirmsSF", foreign_keys=[firm_id])
"""-----------------------------------------------------------------------------------------------------------------"""
class DimProductsSF(SnowflakeBase):
    __tablename__ = "dim_products"

    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    asset_class_id = Column(Integer, ForeignKey("dim_asset_classes.id"))
    vehicle_type_id = Column(Integer, ForeignKey("dim_vehicle_types.id"))
    launch_date = Column(Date)
    is_active = Column(Boolean)

    asset_class = relationship("DimAssetClassesSF", foreign_keys=[asset_class_id])
    vehicle_type = relationship("DimVehiclesSF", foreign_keys=[vehicle_type_id])
"""-----------------------------------------------------------------------------------------------------------------"""
class DimTerritoriesSF(SnowflakeBase):
    __tablename__ = "dim_territories"

    id = Column(Integer, primary_key=True)
    territory_name = Column(String)
    territory_code = Column(String)
    region_id = Column(Integer, ForeignKey("dim_regions.id"))
    country_name = Column(String)

    terr_region = relationship("DimRegionsSF", foreign_keys=[region_id])
"""-----------------------------------------------------------------------------------------------------------------"""
class DimTransactionTypesSF(SnowflakeBase):
    __tablename__ = "dim_transaction_types"

    id = Column(Integer, primary_key=True)
    transaction_type_name = Column(String)
    is_inflow = Column(Boolean)
"""-----------------------------------------------------------------------------------------------------------------"""
class DimVehiclesSF(SnowflakeBase):
    __tablename__ = "dim_vehicle_types"
    
    id = Column(Integer, primary_key=True)
    vehicle_type_name = Column(String)
"""-----------------------------------------------------------------------------------------------------------------"""
class DimWholesalersSF(SnowflakeBase):
    __tablename__ = "dim_wholesalers"

    id = Column(Integer, primary_key=True)
    wholesaler_name = Column(String)
    team_lead_id = Column(Numeric)
    hire_date = Column(Date)
    territory_id = Column(Numeric, ForeignKey("dim_territories.id"))

    ws_territory = relationship("DimTerritoriesSF", foreign_keys=[territory_id])
"""-----------------------------------------------------------------------------------------------------------------"""
class FactAUMFlowSF(SnowflakeBase):
    __tablename__ = "fact_aum_flows"

    id = Column(Integer, primary_key=True)
    date_id = Column(Integer, ForeignKey("dim_dates.id"))
    product_id = Column(Integer, ForeignKey("dim_products.id"))
    transaction_type_id = Column(Integer, ForeignKey("dim_transaction_types.id"))
    wholesaler_id = Column(Integer, ForeignKey("dim_wholesalers.id"))
    account_id = Column(Integer, ForeignKey("dim_accounts.id"))
    flow_amount = Column(Numeric)
    account_aum_amount = Column(Numeric)

    year = relationship("DimDatesSF", foreign_keys=[date_id])
    product = relationship("DimProductsSF", foreign_keys=[product_id])
    wholesaler = relationship("DimWholesalersSF", foreign_keys=[wholesaler_id])
    transaction_type = relationship("DimTransactionTypesSF", foreign_keys=[transaction_type_id])
    account = relationship("DimAccountsSF", foreign_keys=[account_id])
"""-----------------------------------------------------------------------------------------------------------------"""
class FactRetentionSnapshotsSF(SnowflakeBase):
    __tablename__ = "fact_retention_snapshots"

    flow_id = Column(Integer, ForeignKey("fact_aum_flows.id"), primary_key=True)
    snapshot_date_id = Column(Integer, ForeignKey("dim_dates.id"), primary_key=True)
    retained_amount = Column(Numeric)
    retention_pct = Column(Numeric)
    days_since_flow = Column(Integer)
    created_at = Column(Date)
    updated_at = Column(Date)

    flow = relationship("FactAUMFlowSF", foreign_keys=[flow_id])
    snapshot_date = relationship("DimDatesSF", foreign_keys=[snapshot_date_id])
"""-----------------------------------------------------------------------------------------------------------------"""
class FactRevenueSF(SnowflakeBase):
    __tablename__ = "fact_revenue"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("dim_accounts.id"))
    product_id = Column(Integer, ForeignKey("dim_products.id"))
    wholesaler_id = Column(Integer, ForeignKey("dim_wholesalers.id"))
    revenue_date_id = Column(Integer, ForeignKey("dim_dates.id"))
    fee_rate = Column(Numeric)
    revenue_amount = Column(Numeric)
    created_at = Column(Date)
    updated_at = Column(Date)

    product = relationship("DimProductsSF", foreign_keys=[product_id])
    revenue_date = relationship("DimDatesSF", foreign_keys=[revenue_date_id])
    rev_account = relationship("DimAccountsSF", foreign_keys=[account_id])
    rev_wholesaler = relationship("DimWholesalersSF", foreign_keys=[wholesaler_id])
"""-----------------------------------------------------------------------------------------------------------------"""
class FactDistributionExpenseSF(SnowflakeBase):
    __tablename__ = "fact_distribution_expense"

    id = Column(Integer, primary_key=True)
    wholesaler_id = Column(Integer, ForeignKey("dim_wholesalers.id"))
    date_id = Column(Integer, ForeignKey("dim_dates.id"))
    expense_type_id = Column(Integer, ForeignKey("dim_expense_types.id"))
    is_adjustment = Column(Boolean, default=False)
    expense_notes = Column(Text)
    expense_amount = Column(Numeric)
    created_at = Column(Date)
    updated_at = Column(Date)

    wholesaler = relationship("DimWholesalersSF", foreign_keys=[wholesaler_id])
    date = relationship("DimDatesSF", foreign_keys=[date_id])
    expense_type = relationship("DimExpenseTypesSF", foreign_keys=[expense_type_id])
"""-----------------------------------------------------------------------------------------------------------------"""
class FactWholesalerCompSF(SnowflakeBase):
    __tablename__ = "fact_wholesaler_comp"

    id = Column(Integer, primary_key=True)
    wholesaler_id = Column(Integer, ForeignKey("dim_wholesalers.id"))
    date_id = Column(Integer, ForeignKey("dim_dates.id"))
    base_salary = Column(Numeric)
    incentive_comp = Column(Numeric)
    notes = Column(Text)
    created_at = Column(Date)
    updated_at = Column(Date)

    wholesaler = relationship("DimWholesalersSF", foreign_keys=[wholesaler_id])
    date = relationship("DimDatesSF", foreign_keys=[date_id])