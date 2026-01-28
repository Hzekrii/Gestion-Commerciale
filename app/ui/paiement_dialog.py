from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QPushButton, QMessageBox
)
from app.services.paiement_service import PaiementService


class PaiementDialog(QDialog):
    def __init__(self, facture_id):
        super().__init__()

        self.facture_id = facture_id
        self.setWindowTitle("Paiement")
        self.setFixedSize(300, 200)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        self.montant_input = QLineEdit()
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["ESPECES", "CARTE", "CHEQUE"])

        form.addRow("Montant :", self.montant_input)
        form.addRow("Mode :", self.mode_combo)

        btn = QPushButton("Valider paiement")
        btn.clicked.connect(self._save)

        layout.addLayout(form)
        layout.addWidget(btn)
        self.setLayout(layout)

    def _save(self):
        try:
            montant = float(self.montant_input.text())
            mode = self.mode_combo.currentText()

            PaiementService.ajouter_paiement(
                self.facture_id, montant, mode
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))