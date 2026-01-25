from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Fournisseur(Base):
    __tablename__ = "fournisseurs"

    id = Column(Integer, primary_key=True)
    nom = Column(String(255), nullable=False)
    contact = Column(String(255))