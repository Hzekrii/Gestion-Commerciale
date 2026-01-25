from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    nom = Column(String(255), nullable=False)
    telephone = Column(String(50))
    adresse = Column(String(255))