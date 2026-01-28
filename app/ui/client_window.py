from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt

from app.services.client_service import ClientService
from app.ui.client_dialog import ClientDialog
from app.ui.header_widget import HeaderWidget


class ClientWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Clients")
        self.resize(700, 400)

        self._build_ui()
        self._load_clients()

    def _build_ui(self):
        layout = QVBoxLayout()

        header = HeaderWidget("Clients", "Gestion des clients")
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Nom", "Téléphone", "Adresse"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        header_table = self.table.horizontalHeader()
        header_table.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header_table.setSectionResizeMode(1, QHeaderView.Stretch)
        header_table.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header_table.setSectionResizeMode(3, QHeaderView.Stretch)

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Ajouter")
        btn_edit = QPushButton("Modifier")
        btn_delete = QPushButton("Supprimer")

        btn_add.clicked.connect(self._add_client)
        btn_edit.clicked.connect(self._edit_client)
        btn_delete.clicked.connect(self._delete_client)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addStretch()

        layout.addWidget(header)
        layout.addLayout(btn_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def _load_clients(self):
        clients = ClientService.lister_clients()
        self.table.setRowCount(len(clients))

        for row, client in enumerate(clients):
            self.table.setItem(row, 0, QTableWidgetItem(str(client.id)))
            self.table.setItem(row, 1, QTableWidgetItem(client.nom))
            self.table.setItem(row, 2, QTableWidgetItem(client.telephone or ""))
            self.table.setItem(row, 3, QTableWidgetItem(client.adresse or ""))

    def _selected_client_id(self):
        row = self.table.currentRow()
        if row == -1:
            return None
        return int(self.table.item(row, 0).text())

    def _add_client(self):
        dialog = ClientDialog()
        if dialog.exec():
            self._load_clients()

    def _edit_client(self):
        client_id = self._selected_client_id()
        if not client_id:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un client")
            return

        client = ClientService.get_client(client_id)
        dialog = ClientDialog(client)
        if dialog.exec():
            self._load_clients()

    def _delete_client(self):
        client_id = self._selected_client_id()
        if not client_id:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un client")
            return

        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Supprimer ce client ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            ClientService.supprimer_client(client_id)
            self._load_clients()