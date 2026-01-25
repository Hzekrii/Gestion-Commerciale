from app.core.database import SessionLocal
from app.models.fournisseur import Fournisseur

class FournisseurService:

    @staticmethod
    def creer_fournisseur(nom, contact=None):
        session = SessionLocal()

        fournisseur = Fournisseur(
            nom=nom,
            contact=contact
        )

        session.add(fournisseur)
        session.commit()
        session.refresh(fournisseur)
        session.close()

        return fournisseur

    @staticmethod
    def lister_fournisseurs():
        session = SessionLocal()
        fournisseurs = session.query(Fournisseur).all()
        session.close()
        return fournisseurs
    
    @staticmethod
    def get_fournisseur(fid):
        session = SessionLocal()
        f = session.get(Fournisseur, fid)
        session.close()
        return f

    @staticmethod
    def modifier_fournisseur(fid, nom, contact):
        session = SessionLocal()
        f = session.get(Fournisseur, fid)
        if not f:
            session.close()
            raise ValueError("Fournisseur introuvable")

        f.nom = nom
        f.contact = contact
        session.commit()
        session.close()

    @staticmethod
    def supprimer_fournisseur(fid):
        session = SessionLocal()
        f = session.get(Fournisseur, fid)
        if not f:
            session.close()
            raise ValueError("Fournisseur introuvable")

        session.delete(f)
        session.commit()
        session.close()