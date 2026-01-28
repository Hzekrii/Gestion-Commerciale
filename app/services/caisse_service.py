from datetime import date
from sqlalchemy import func
from app.core.database import SessionLocal
from app.models.paiement import Paiement


class CaisseService:

    @staticmethod
    def total_journalier(jour=None):
        """
        Retourne le total encaissé par mode pour une journée
        """
        if jour is None:
            jour = date.today()

        session = SessionLocal()

        resultats = (
            session.query(
                Paiement.mode_paiement,
                func.sum(Paiement.montant)
            )
            .filter(func.date(Paiement.date_paiement) == jour)
            .group_by(Paiement.mode_paiement)
            .all()
        )

        session.close()

        # Convertir en dict
        caisse = {mode: total for mode, total in resultats}
        total_general = sum(caisse.values())

        return caisse, total_general