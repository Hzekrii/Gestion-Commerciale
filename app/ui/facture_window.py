from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox,
    QSpinBox, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt

from app.ui.header_widget import HeaderWidget
from app.services.facture_service import FactureService
from app.services.client_service import ClientService
from app.services.article_service import ArticleService
from app.services.stock_service import StockService



class FactureWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.facture = None
        self.articles = ArticleService.lister_articles()

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        # ===== HEADER =====
        header = HeaderWidget(
            "Facturation",
            "Créer et valider des factures"
        )
        layout.addWidget(header)

        # ===== CLIENT =====
        client_layout = QHBoxLayout()
        client_layout.addWidget(QLabel("Client :"))

        self.client_combo = QComboBox()
        self.clients = ClientService.lister_clients()
        for c in self.clients:
            self.client_combo.addItem(c.nom, c.id)

        btn_create = QPushButton("Créer facture")
        btn_create.clicked.connect(self._creer_facture)

        client_layout.addWidget(self.client_combo)
        client_layout.addWidget(btn_create)
        client_layout.addStretch()

        layout.addLayout(client_layout)

        # ===== TABLE LIGNES =====
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(
            ["Article", "Quantité", "Prix unitaire", "Total"]
        )
        #  Redimensionnement automatique
        header_table = self.table.horizontalHeader()
        header_table.setSectionResizeMode(0, QHeaderView.Stretch)   # Article prend l’espace
        header_table.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header_table.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header_table.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        layout.addWidget(self.table)

        # ===== AJOUT LIGNE =====
        ligne_layout = QHBoxLayout()

        self.article_combo = QComboBox()
        for a in self.articles:
            self.article_combo.addItem(
                f"{a.code} - {a.designation}", a.id
            )
        self.article_combo.currentIndexChanged.connect(
            self._update_stock_label
        )

        self.qty_input = QSpinBox()
        self.qty_input.setMinimum(1)
        self.qty_input.setMaximum(100000)

        # ===== STOCK ACTUEL =====
        self.lbl_stock = QLabel("Stock actuel : -")
        self.lbl_stock.setStyleSheet("color: #c0392b; font-weight: bold;")

        btn_add = QPushButton("Ajouter ligne")
        btn_add.clicked.connect(self._ajouter_ligne)

        ligne_layout.addWidget(QLabel("Article :"))
        ligne_layout.addWidget(self.article_combo)
        ligne_layout.addWidget(QLabel("Qté :"))
        ligne_layout.addWidget(self.qty_input)
        ligne_layout.addWidget(self.lbl_stock)
        ligne_layout.addWidget(btn_add)
        ligne_layout.addStretch()

        layout.addLayout(ligne_layout)

        # ===== TOTAUX =====
        total_layout = QVBoxLayout()

        self.lbl_ht = QLabel("Total HT : 0.00")
        self.lbl_tva = QLabel("TVA (20%) : 0.00")
        self.lbl_ttc = QLabel("Total TTC : 0.00")

        self.lbl_ttc.setStyleSheet("font-weight: bold; font-size: 16px;")

        total_layout.addWidget(self.lbl_ht)
        total_layout.addWidget(self.lbl_tva)
        total_layout.addWidget(self.lbl_ttc)

        layout.addLayout(total_layout)

        # ===== VALIDER =====
        btn_validate = QPushButton("Valider facture")
        btn_validate.clicked.connect(self._valider_facture)

        layout.addWidget(btn_validate, alignment=Qt.AlignRight)

        #  Afficher le stock initial
        self._update_stock_label()

        self.setLayout(layout)

    # =====================================================
    # ACTIONS
    # =====================================================
    def _creer_facture(self):
        client_id = self.client_combo.currentData()
        self.facture = FactureService.creer_facture(client_id)
        QMessageBox.information(self, "OK", "Facture créée")

        self.table.setRowCount(0)
        self._refresh_totaux()

    def _ajouter_ligne(self):
        if not self.facture:
            QMessageBox.warning(self, "Erreur", "Créer la facture d'abord")
            return

        article_id = self.article_combo.currentData()
        quantite = self.qty_input.value()

        try:
            FactureService.ajouter_ligne(
                self.facture.id, article_id, quantite
            )
            self._refresh_table()
            self._refresh_totaux()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def _refresh_table(self):
        from app.models.ligne_facture import LigneFacture
        from app.core.database import SessionLocal

        session = SessionLocal()
        lignes = session.query(LigneFacture).filter_by(
            facture_id=self.facture.id
        ).all()
        session.close()

        self.table.setRowCount(len(lignes))

        for row, l in enumerate(lignes):
            article = next(
                a for a in self.articles if a.id == l.article_id
            )
            self.table.setItem(row, 0, QTableWidgetItem(article.designation))
            self.table.setItem(row, 1, QTableWidgetItem(str(l.quantite)))
            self.table.setItem(row, 2, QTableWidgetItem(str(l.prix_unitaire)))
            self.table.setItem(row, 3, QTableWidgetItem(str(l.total_ligne)))

    def _refresh_totaux(self):
        if not self.facture:
            return

        from app.core.database import SessionLocal
        from app.models.facture import Facture

        session = SessionLocal()
        f = session.get(Facture, self.facture.id)
        session.close()

        self.lbl_ht.setText(f"Total HT : {f.total_ht:.2f}")
        self.lbl_tva.setText(f"TVA (20%) : {f.total_tva:.2f}")
        self.lbl_ttc.setText(f"Total TTC : {f.total_ttc:.2f}")

    def _valider_facture(self):
        if not self.facture:
            return

        try:
            FactureService.valider_facture(self.facture.id)
            QMessageBox.information(self, "OK", "Facture validée")
            self.facture = None
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))


    def _update_stock_label(self):
        article_id = self.article_combo.currentData()
        if article_id:
            stock = StockService.calculer_stock(article_id)
            self.lbl_stock.setText(f"Stock actuel : {stock}")
        else:
            self.lbl_stock.setText("Stock actuel : -")


    def refresh_data(self):
        # Recharger clients
        self.client_combo.clear()
        self.clients = ClientService.lister_clients()
        for c in self.clients:
            self.client_combo.addItem(c.nom, c.id)

        # Recharger articles
        self.article_combo.clear()
        self.articles = ArticleService.lister_articles()
        for a in self.articles:
            self.article_combo.addItem(
                f"{a.code} - {a.designation}", a.id
            )
        self._update_stock_label()