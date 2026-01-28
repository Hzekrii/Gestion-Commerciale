from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime, timezone
from app.core.database import Base

class Paiement(Base):
    __tablename__ = "paiements"

    id = Column(Integer, primary_key=True)
    facture_id = Column(Integer, ForeignKey("factures.id"), nullable=False)

    montant = Column(Float, nullable=False)
    mode_paiement = Column(String(20), nullable=False)  # ESPECES / CARTE / CHEQUE
    date_paiement = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )