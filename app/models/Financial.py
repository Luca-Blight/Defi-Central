from sqlmodel import SQLModel, Column, Integer, Float, DateTime, ForeignKey


class Financial(SQLModel, table=True):

    __tablename__ = "financial"
    # ensure id is foreign key
    id = Column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )  # Foreign key relationship
    tvl = Column(Float, nullable=True)
    fees = Column(Float, nullable=True)
    date = Column(DateTime, nullable=False)
    protocol_id = Column(Integer, ForeignKey("protocol.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
