from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt

from app.ui.header_widget import HeaderWidget
from app.services.facture_service import FactureService
from app.services.client_service import ClientService
from app.ui.facture_detail_window import FactureDetailWindow


class FactureListWindow(QWidget):
    def __init__(self):
        super().__init__()

        self._build_ui()
        self._load_factures()

    def _build_ui(self):
        layout = QVBoxLayout()

        header = HeaderWidget(
            "Historique des factures",
            "Liste des factures créées"
        )
        layout.addWidget(header)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["N°", "Client", "Date", "Total TTC", "Statut"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self._open_detail)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def _load_factures(self):
        factures = FactureService.lister_factures()
        clients = {c.id: c.nom for c in ClientService.lister_clients()}

        self.table.setRowCount(len(factures))

        for row, f in enumerate(factures):
            self.table.setItem(row, 0, QTableWidgetItem(str(f.id)))
            self.table.setItem(row, 1, QTableWidgetItem(clients.get(f.client_id, "")))
            self.table.setItem(row, 2, QTableWidgetItem(str(f.date_facture.date())))
            self.table.setItem(row, 3, QTableWidgetItem(f"{f.total_ttc:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f.statut))

    def _open_detail(self):
        row = self.table.currentRow()
        if row == -1:
            return

        facture_id = int(self.table.item(row, 0).text())
        self.detail = FactureDetailWindow(facture_id)
        self.detail.show()