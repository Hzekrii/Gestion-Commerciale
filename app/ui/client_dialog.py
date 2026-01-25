from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QMessageBox
)

from app.services.client_service import ClientService


class ClientDialog(QDialog):
    def __init__(self, client=None):
        super().__init__()

        self.client = client
        self.setWindowTitle(
            "Ajouter Client" if client is None else "Modifier Client"
        )
        self.setFixedSize(300, 220)

        self._build_ui()
        if client:
            self._load_client()

    def _build_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        self.nom_input = QLineEdit()
        self.tel_input = QLineEdit()
        self.adresse_input = QLineEdit()

        form.addRow("Nom :", self.nom_input)
        form.addRow("Téléphone :", self.tel_input)
        form.addRow("Adresse :", self.adresse_input)

        btn = QPushButton("Enregistrer")
        btn.clicked.connect(self._save)

        layout.addLayout(form)
        layout.addWidget(btn)
        self.setLayout(layout)

    def _load_client(self):
        self.nom_input.setText(self.client.nom)
        self.tel_input.setText(self.client.telephone or "")
        self.adresse_input.setText(self.client.adresse or "")

    def _save(self):
        try:
            nom = self.nom_input.text().strip()
            tel = self.tel_input.text().strip()
            adresse = self.adresse_input.text().strip()

            if not nom:
                raise ValueError("Le nom est obligatoire")

            if self.client is None:
                ClientService.creer_client(nom, tel, adresse)
            else:
                ClientService.modifier_client(
                    self.client.id, nom, tel, adresse
                )

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))