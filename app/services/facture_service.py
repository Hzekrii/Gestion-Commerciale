from app.core.database import SessionLocal
from app.models.facture import Facture
from app.models.ligne_facture import LigneFacture
from app.models.article import Article
from app.models.client import Client
from app.services.stock_service import StockService

class FactureService:

    @staticmethod
    def creer_facture(client_id):
        session = SessionLocal()
        facture = Facture(client_id=client_id)
        session.add(facture)
        session.commit()
        session.refresh(facture)
        session.close()
        return facture

    @staticmethod
    def ajouter_ligne(facture_id, article_id, quantite):
        session = SessionLocal()

        article = session.get(Article, article_id)
        facture = session.get(Facture, facture_id)

        if not article or not facture:
            session.close()
            raise ValueError("Article ou facture introuvable")

        # Vérifier stock
        stock = StockService.calculer_stock(article_id)
        if stock < quantite:
            session.close()
            raise ValueError("Stock insuffisant")

        total_ligne = quantite * article.prix_vente

        ligne = LigneFacture(
            facture_id=facture_id,
            article_id=article_id,
            quantite=quantite,
            prix_unitaire=article.prix_vente,
            total_ligne=total_ligne
        )

        session.add(ligne)
        session.commit()

        FactureService._recalculer_totaux(facture_id, session)

        session.close()

    @staticmethod
    def _recalculer_totaux(facture_id, session):
        lignes = session.query(LigneFacture).filter_by(
            facture_id=facture_id
        ).all()

        total_ht = sum(l.total_ligne for l in lignes)
        total_tva = total_ht * 0.20
        total_ttc = total_ht + total_tva

        facture = session.get(Facture, facture_id)
        facture.total_ht = total_ht
        facture.total_tva = total_tva
        facture.total_ttc = total_ttc

        session.commit()

    @staticmethod
    def valider_facture(facture_id):
        session = SessionLocal()

        lignes = session.query(LigneFacture).filter_by(
            facture_id=facture_id
        ).all()

        if not lignes:
            session.close()
            raise ValueError("Facture vide")

        # Déduction du stock
        for ligne in lignes:
            StockService.sortie_stock(
                ligne.article_id,
                ligne.quantite,
                f"Facture {facture_id}"
            )

        facture = session.get(Facture, facture_id)
        facture.statut = "VALIDEE"

        session.commit()
        session.close()