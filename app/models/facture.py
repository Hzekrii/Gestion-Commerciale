from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float, String
from datetime import datetime, timezone
from app.core.database import Base

class Facture(Base):
    __tablename__ = "factures"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    date_facture = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    total_ht = Column(Float, default=0.0)
    total_tva = Column(Float, default=0.0)
    total_ttc = Column(Float, default=0.0)

    statut = Column(String(20), default="BROUILLON")  # BROUILLON / VALIDEE