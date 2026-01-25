from sqlalchemy import Column, Integer, ForeignKey, Float
from app.core.database import Base

class LigneFacture(Base):
    __tablename__ = "lignes_facture"

    id = Column(Integer, primary_key=True)
    facture_id = Column(Integer, ForeignKey("factures.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)

    quantite = Column(Integer, nullable=False)
    prix_unitaire = Column(Float, nullable=False)
    total_ligne = Column(Float, nullable=False)