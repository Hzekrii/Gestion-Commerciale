from app.core.database import SessionLocal
from app.models.paiement import Paiement
from app.models.facture import Facture

class PaiementService:

    @staticmethod
    def ajouter_paiement(facture_id, montant, mode):
        session = SessionLocal()

        facture = session.get(Facture, facture_id)
        if not facture:
            session.close()
            raise ValueError("Facture introuvable")

        paiement = Paiement(
            facture_id=facture_id,
            montant=montant,
            mode_paiement=mode
        )

        session.add(paiement)
        session.commit()
        session.close()

    @staticmethod
    def total_paye(facture_id):
        session = SessionLocal()
        paiements = session.query(Paiement).filter_by(
            facture_id=facture_id
        ).all()
        session.close()
        return sum(p.montant for p in paiements)