from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QLabel, QTableWidget,
    QTableWidgetItem, QMessageBox
)

from app.services.facture_service import FactureService
from app.services.client_service import ClientService
from app.services.article_service import ArticleService


class FactureWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nouvelle Facture")
        self.resize(800, 500)

        self.facture = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        self.client_combo = QComboBox()
        self.clients = ClientService.lister_clients()
        for c in self.clients:
            self.client_combo.addItem(c.nom, c.id)

        btn_create = QPushButton("Créer facture")
        btn_create.clicked.connect(self._create_facture)

        layout.addWidget(QLabel("Client"))
        layout.addWidget(self.client_combo)
        layout.addWidget(btn_create)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(
            ["Article", "Quantité", "Prix", "Total"]
        )
        layout.addWidget(self.table)

        btn_add = QPushButton("Ajouter ligne")
        btn_add.clicked.connect(self._add_ligne)

        btn_validate = QPushButton("Valider facture")
        btn_validate.clicked.connect(self._valider)

        btns = QHBoxLayout()
        btns.addWidget(btn_add)
        btns.addWidget(btn_validate)

        layout.addLayout(btns)
        self.setLayout(layout)

    def _create_facture(self):
        client_id = self.client_combo.currentData()
        self.facture = FactureService.creer_facture(client_id)
        QMessageBox.information(self, "OK", "Facture créée")

    def _add_ligne(self):
        if not self.facture:
            QMessageBox.warning(self, "Erreur", "Créer la facture d'abord")
            return

        article = ArticleService.lister_articles()[0]
        FactureService.ajouter_ligne(self.facture.id, article.id, 1)
        self._refresh()

    def _refresh(self):
        self.table.setRowCount(0)

    def _valider(self):
        FactureService.valider_facture(self.facture.id)
        QMessageBox.information(self, "OK", "Facture validée")