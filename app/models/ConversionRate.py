from database.database import Base


from sqlmodel import Field, SQLModel, Column, DateTime, Float


class ConversionRate(SQLModel, table=True):
    __tablename__ = "conversion_rate"

    block_date = Column(DateTime, primary_key=True, nullable=False)
    eth_conversion_rate = Column(Float)
    matic_conversion_rate = Column(Float)
