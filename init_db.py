from app.core.database import Base, engine, SessionLocal

# IMPORT DE TOUS LES MODÈLES À CRÉER
import app.models

from app.models.role import Role
from app.models.utilisateur import Utilisateur
from app.models.tva import TVA

import bcrypt

def init_database():
    print("📦 Création des tables...")
    Base.metadata.create_all(engine)

    session = SessionLocal()

    # Rôles par défaut
    if session.query(Role).count() == 0:
        admin = Role(nom="ADMIN")
        caissier = Role(nom="CAISSIER")
        session.add_all([admin, caissier])
        session.commit()

    # TVA par défaut
    if session.query(TVA).count() == 0:
        session.add(TVA(taux=20.0))
        session.commit()

    # Utilisateur admin
    if session.query(Utilisateur).count() == 0:
        password = bcrypt.hashpw("admin".encode(), bcrypt.gensalt())
        admin_user = Utilisateur(
            nom_utilisateur="admin",
            mot_de_passe_hash=password.decode(),
            role_id=1
        )
        session.add(admin_user)
        session.commit()

    session.close()
    print("✅ Base de données initialisée")

if __name__ == "__main__":
    init_database()