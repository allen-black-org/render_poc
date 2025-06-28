from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey
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

class Product(Base):
    __tablename__ = "dim_products"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    product_name = Column(String)


class TransactionType(Base):
    __tablename__ = "dim_transaction_types"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    transaction_type_name = Column(String)


class AUMFlow(Base):
    __tablename__ = "fact_aum_flows"
    __table_args__ = {"schema": "dist_perf_dw"}

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("dist_perf_dw.dim_products.id"))
    transaction_type_id = Column(Integer, ForeignKey("dist_perf_dw.dim_transaction_types.id"))
    flow_amount = Column(Numeric)

    product = relationship("Product")
    transaction_type = relationship("TransactionType")