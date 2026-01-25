from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.core.database import Base

class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True)
    nom_utilisateur = Column(String(50), unique=True, nullable=False)
    mot_de_passe_hash = Column(String(255), nullable=False)
    actif = Column(Boolean, default=True)

    role_id = Column(Integer, ForeignKey("roles.id"))