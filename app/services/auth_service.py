from app.core.database import SessionLocal
from app.models.utilisateur import Utilisateur
from app.models.role import Role
import bcrypt

class AuthService:

    @staticmethod
    def authentifier(nom_utilisateur: str, mot_de_passe: str):
        session = SessionLocal()

        utilisateur = (
            session.query(Utilisateur)
            .join(Role)
            .filter(Utilisateur.nom_utilisateur == nom_utilisateur)
            .first()
        )

        session.close()

        if not utilisateur:
            raise ValueError("Utilisateur inexistant")

        if not utilisateur.actif:
            raise ValueError("Utilisateur désactivé")

        if not bcrypt.checkpw(
            mot_de_passe.encode(),
            utilisateur.mot_de_passe_hash.encode()
        ):
            raise ValueError("Mot de passe incorrect")

        return utilisateur