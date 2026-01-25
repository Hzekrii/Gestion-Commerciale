from app.core.database import SessionLocal
from app.models.article import Article

class ArticleService:

    @staticmethod
    def creer_article(code, designation, prix_achat, prix_vente, tva_id, code_barre=None):
        session = SessionLocal()

        article = Article(
            code=code,
            designation=designation,
            prix_achat=prix_achat,
            prix_vente=prix_vente,
            tva_id=tva_id,
            code_barre=code_barre
        )

        session.add(article)
        session.commit()
        session.refresh(article)
        session.close()

        return article

    @staticmethod
    def lister_articles():
        session = SessionLocal()
        articles = session.query(Article).all()
        session.close()
        return articles
    
    @staticmethod
    def modifier_article(article):
        session = SessionLocal()
        session.merge(article)
        session.commit()
        session.close()

    @staticmethod
    def supprimer_article(article_id: int):
        session = SessionLocal()

        article = session.get(Article, article_id)
        if not article:
            session.close()
            raise ValueError("Article introuvable")

        session.delete(article)
        session.commit()
        session.close()