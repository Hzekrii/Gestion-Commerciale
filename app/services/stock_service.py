from app.core.database import SessionLocal
from app.models.mouvement_stock import MouvementStock

class StockService:

    @staticmethod
    def entree_stock(article_id, quantite, commentaire=None):
        if quantite <= 0:
            raise ValueError("La quantité doit être positive")

        session = SessionLocal()

        mouvement = MouvementStock(
            article_id=article_id,
            quantite=quantite,
            type_mouvement="ENTREE",
            commentaire=commentaire
        )

        session.add(mouvement)
        session.commit()
        session.close()

    @staticmethod
    def sortie_stock(article_id, quantite, commentaire=None):
        if quantite <= 0:
            raise ValueError("La quantité doit être positive")

        stock_actuel = StockService.calculer_stock(article_id)
        if stock_actuel < quantite:
            raise ValueError("Stock insuffisant")

        session = SessionLocal()

        mouvement = MouvementStock(
            article_id=article_id,
            quantite=quantite,
            type_mouvement="SORTIE",
            commentaire=commentaire
        )

        session.add(mouvement)
        session.commit()
        session.close()

    @staticmethod
    def calculer_stock(article_id):
        session = SessionLocal()

        mouvements = session.query(MouvementStock).filter(
            MouvementStock.article_id == article_id
        ).all()

        session.close()

        stock = 0
        for m in mouvements:
            if m.type_mouvement == "ENTREE":
                stock += m.quantite
            elif m.type_mouvement == "SORTIE":
                stock -= m.quantite

        return stock