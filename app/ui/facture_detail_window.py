from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt

from app.ui.header_widget import HeaderWidget
from app.services.facture_service import FactureService
from app.services.article_service import ArticleService


class FactureDetailWindow(QWidget):
    def __init__(self, facture_id):
        super().__init__()

        self.facture_id = facture_id
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        self.setWindowTitle("Détail Facture")
        self.resize(700, 400)

        self.layout = QVBoxLayout()

        self.header = HeaderWidget("Détail de la facture")
        self.layout.addWidget(self.header)

        self.lbl_info = QLabel("")
        self.layout.addWidget(self.lbl_info)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(
            ["Article", "Quantité", "Prix", "Total"]
        )
        self.layout.addWidget(self.table)

        self.lbl_totaux = QLabel("")
        self.lbl_totaux.setStyleSheet("font-weight: bold;")
        self.layout.addWidget(self.lbl_totaux)

        self.setLayout(self.layout)

    def _load_data(self):
        facture, client, lignes = FactureService.get_facture_detail(self.facture_id)
        articles = {a.id: a.designation for a in ArticleService.lister_articles()}

        self.lbl_info.setText(
            f"Facture n° {facture.id} | Client : {client.nom} | Statut : {facture.statut}"
        )

        self.table.setRowCount(len(lignes))
        for row, l in enumerate(lignes):
            self.table.setItem(row, 0, QTableWidgetItem(articles.get(l.article_id, "")))
            self.table.setItem(row, 1, QTableWidgetItem(str(l.quantite)))
            self.table.setItem(row, 2, QTableWidgetItem(str(l.prix_unitaire)))
            self.table.setItem(row, 3, QTableWidgetItem(str(l.total_ligne)))

        self.lbl_totaux.setText(
            f"Total HT : {facture.total_ht:.2f} | "
            f"TVA : {facture.total_tva:.2f} | "
            f"Total TTC : {facture.total_ttc:.2f}"
        )