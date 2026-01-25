from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    designation = Column(String(255), nullable=False)
    code_barre = Column(String(100), unique=True)

    prix_achat = Column(Float, nullable=False)
    prix_vente = Column(Float, nullable=False)

    tva_id = Column(Integer, ForeignKey("tva.id"))