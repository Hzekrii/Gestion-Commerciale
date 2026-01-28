from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt

from app.ui.header_widget import HeaderWidget
from app.services.facture_service import FactureService
from app.services.article_service import ArticleService
from app.services.paiement_service import PaiementService
from app.ui.paiement_dialog import PaiementDialog
from app.utils.pdf_facture import generer_facture_pdf
from app.utils.excel_facture import exporter_facture_excel


class FactureDetailWindow(QWidget):
    def __init__(self, facture_id):
        super().__init__()

        self.facture_id = facture_id
        self._build_ui()
        self._load_data()

    # =====================================================
    # UI
    # =====================================================
    def _build_ui(self):
        self.setWindowTitle("Détail Facture")
        self.resize(750, 500)

        layout = QVBoxLayout()

        # ===== HEADER =====
        header_widget = HeaderWidget(
            "Détail de la facture",
            "Informations, paiements et export"
        )
        layout.addWidget(header_widget)

        # ===== INFO FACTURE =====
        self.lbl_info = QLabel("")
        self.lbl_info.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.lbl_info)

        # ===== BOUTONS ACTIONS =====
        btn_layout = QHBoxLayout()

        self.btn_payer = QPushButton("Ajouter paiement")
        self.btn_pdf = QPushButton("Exporter PDF")
        self.btn_excel = QPushButton("Exporter Excel")

        self.btn_payer.clicked.connect(self._open_paiement)
        self.btn_pdf.clicked.connect(self._export_pdf)
        self.btn_excel.clicked.connect(self._export_excel)

        btn_layout.addWidget(self.btn_payer)
        btn_layout.addWidget(self.btn_pdf)
        btn_layout.addWidget(self.btn_excel)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        # ===== TABLE LIGNES =====
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(
            ["Article", "Quantité", "Prix unitaire", "Total"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # ===== RÉSUMÉ FINANCIER =====
        self.lbl_totaux = QLabel("")
        self.lbl_totaux.setWordWrap(True)
        self.lbl_totaux.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.lbl_totaux)

        self.setLayout(layout)

    # =====================================================
    # DATA
    # =====================================================
    def _load_data(self):
        facture, client, lignes = FactureService.get_facture_detail(self.facture_id)
        articles = {a.id: a.designation for a in ArticleService.lister_articles()}

        # ----- Calcul paiements -----
       
        total_paye = PaiementService.total_paye(facture.id)
        

        reste = facture.total_ttc - total_paye

        # ----- Statut paiement -----
        if total_paye <= 0:
            statut_paiement = "NON PAYÉE"
            color = "red"
        elif total_paye < facture.total_ttc:
            statut_paiement = "PARTIELLE"
            color = "orange"
        else:
            statut_paiement = "PAYÉE"
            color = "green"

        # ----- Header info -----
        self.lbl_info.setText(
            f"Facture n° {facture.id} | "
            f"Client : {client.nom} | "
            f"Statut facture : {facture.statut}"
        )

        # ----- Table lignes -----
        self.table.setRowCount(len(lignes))
        for row, l in enumerate(lignes):
            self.table.setItem(row, 0, QTableWidgetItem(articles.get(l.article_id, "")))
            self.table.setItem(row, 1, QTableWidgetItem(str(l.quantite)))
            self.table.setItem(row, 2, QTableWidgetItem(f"{l.prix_unitaire:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{l.total_ligne:.2f}"))

        # ----- Résumé financier -----
        self.lbl_totaux.setText(
            f"Total HT : {facture.total_ht:.2f}\n"
            f"TVA : {facture.total_tva:.2f}\n"
            f"Total TTC : {facture.total_ttc:.2f}\n\n"
            f"Payé : {total_paye:.2f}\n"
            f"Reste à payer : {reste:.2f}\n"
            f"Statut paiement : {statut_paiement}"
        )
        self.lbl_totaux.setStyleSheet(
            f"font-weight: bold; font-size: 14px; color: {color};"
        )

        # ----- Désactiver paiement si déjà payée -----
        self.btn_payer.setEnabled(statut_paiement != "PAYÉE")

    # =====================================================
    # ACTIONS
    # =====================================================
    def _open_paiement(self):
        dialog = PaiementDialog(self.facture_id)
        if dialog.exec():
            self._load_data()  # ✅ refresh après paiement

    def _export_pdf(self):
        facture, client, lignes = FactureService.get_facture_detail(self.facture_id)
        filename = generer_facture_pdf(facture, client, lignes)
        QMessageBox.information(self, "PDF", f"PDF généré : {filename}")

    def _export_excel(self):
        facture, client, lignes = FactureService.get_facture_detail(self.facture_id)
        filename = exporter_facture_excel(facture, client, lignes)
        QMessageBox.information(self, "Excel", f"Fichier Excel généré : {filename}")