from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QMessageBox
)
from app.services.fournisseur_service import FournisseurService


class FournisseurDialog(QDialog):
    def __init__(self, fournisseur=None):
        super().__init__()

        self.fournisseur = fournisseur
        self.setWindowTitle(
            "Ajouter Fournisseur" if fournisseur is None else "Modifier Fournisseur"
        )
        self.setFixedSize(300, 180)

        self._build_ui()
        if fournisseur:
            self._load()

    def _build_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        self.nom_input = QLineEdit()
        self.contact_input = QLineEdit()

        form.addRow("Nom :", self.nom_input)
        form.addRow("Contact :", self.contact_input)

        btn = QPushButton("Enregistrer")
        btn.clicked.connect(self._save)

        layout.addLayout(form)
        layout.addWidget(btn)
        self.setLayout(layout)

    def _load(self):
        self.nom_input.setText(self.fournisseur.nom)
        self.contact_input.setText(self.fournisseur.contact or "")

    def _save(self):
        try:
            nom = self.nom_input.text().strip()
            contact = self.contact_input.text().strip()

            if not nom:
                raise ValueError("Nom obligatoire")

            if self.fournisseur is None:
                FournisseurService.creer_fournisseur(nom, contact)
            else:
                FournisseurService.modifier_fournisseur(
                    self.fournisseur.id, nom, contact
                )

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))