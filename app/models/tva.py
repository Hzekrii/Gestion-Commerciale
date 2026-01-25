from sqlalchemy import Column, Integer, Float
from app.core.database import Base

class TVA(Base):
    __tablename__ = "tva"

    id = Column(Integer, primary_key=True)
    taux = Column(Float, nullable=False)