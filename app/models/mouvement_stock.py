from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone
from app.core.database import Base

class MouvementStock(Base):
    __tablename__ = "mouvements_stock"

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    quantite = Column(Integer, nullable=False)
    type_mouvement = Column(String(20), nullable=False)  # ENTREE / SORTIE
    date_mouvement = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    commentaire = Column(String(255))