from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem,
    QPushButton
)
from PySide6.QtCore import Qt
from datetime import date

from app.ui.header_widget import HeaderWidget
from app.services.caisse_service import CaisseService


class CaisseWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Caisse Journalière")
        self.resize(600, 400)

        self._build_ui()
        self._load_data()

    def _build_ui(self):
        layout = QVBoxLayout()

        header = HeaderWidget(
            "Caisse journalière",
            "Encaissements du jour"
        )
        layout.addWidget(header)

        self.lbl_date = QLabel("")
        self.lbl_date.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_date)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(
            ["Mode de paiement", "Montant"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        self.lbl_total = QLabel("")
        self.lbl_total.setAlignment(Qt.AlignRight)
        self.lbl_total.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(self.lbl_total)

        btn_refresh = QPushButton("Actualiser")
        btn_refresh.clicked.connect(self._load_data)
        layout.addWidget(btn_refresh, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def _load_data(self):
        caisse, total = CaisseService.total_journalier()

        self.lbl_date.setText(f"Date : {date.today()}")

        self.table.setRowCount(len(caisse))
        for row, (mode, montant) in enumerate(caisse.items()):
            self.table.setItem(row, 0, QTableWidgetItem(mode))
            self.table.setItem(row, 1, QTableWidgetItem(f"{montant:.2f}"))

        self.lbl_total.setText(f"Total encaissé : {total:.2f}")