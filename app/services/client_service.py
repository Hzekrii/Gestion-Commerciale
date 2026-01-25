from app.core.database import SessionLocal
from app.models.client import Client

class ClientService:

    @staticmethod
    def creer_client(nom, telephone=None, adresse=None):
        session = SessionLocal()

        client = Client(
            nom=nom,
            telephone=telephone,
            adresse=adresse
        )

        session.add(client)
        session.commit()
        session.refresh(client)
        session.close()

        return client

    @staticmethod
    def lister_clients():
        session = SessionLocal()
        clients = session.query(Client).all()
        session.close()
        return clients
    
    @staticmethod
    def get_client(client_id):
        session = SessionLocal()
        client = session.get(Client, client_id)
        session.close()
        return client

    @staticmethod
    def modifier_client(client_id, nom, telephone, adresse):
        session = SessionLocal()
        client = session.get(Client, client_id)

        if not client:
            session.close()
            raise ValueError("Client introuvable")

        client.nom = nom
        client.telephone = telephone
        client.adresse = adresse

        session.commit()
        session.close()

    @staticmethod
    def supprimer_client(client_id):
        session = SessionLocal()
        client = session.get(Client, client_id)

        if not client:
            session.close()
            raise ValueError("Client introuvable")

        session.delete(client)
        session.commit()
        session.close()