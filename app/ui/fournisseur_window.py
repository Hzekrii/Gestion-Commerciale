from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView
)
from app.services.fournisseur_service import FournisseurService
from app.ui.fournisseur_dialog import FournisseurDialog
from app.ui.header_widget import HeaderWidget

class FournisseurWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fournisseurs")
        self.resize(700, 400)

        self._build_ui()
        self._load_fournisseurs()

    def _build_ui(self):
        layout = QVBoxLayout()

        header = HeaderWidget("Fournisseurs", "Gestion des fournisseurs")
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Nom", "Contact"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        header_table = self.table.horizontalHeader()
        header_table.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header_table.setSectionResizeMode(1, QHeaderView.Stretch)
        header_table.setSectionResizeMode(2, QHeaderView.Stretch)

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Ajouter")
        btn_edit = QPushButton("Modifier")
        btn_delete = QPushButton("Supprimer")

        btn_add.clicked.connect(self._add)
        btn_edit.clicked.connect(self._edit)
        btn_delete.clicked.connect(self._delete)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addStretch()

        layout.addWidget(header)
        layout.addLayout(btn_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def _load_fournisseurs(self):
        fournisseurs = FournisseurService.lister_fournisseurs()
        self.table.setRowCount(len(fournisseurs))

        for row, f in enumerate(fournisseurs):
            self.table.setItem(row, 0, QTableWidgetItem(str(f.id)))
            self.table.setItem(row, 1, QTableWidgetItem(f.nom))
            self.table.setItem(row, 2, QTableWidgetItem(f.contact or ""))

    def _selected_id(self):
        row = self.table.currentRow()
        if row == -1:
            return None
        return int(self.table.item(row, 0).text())

    def _add(self):
        dialog = FournisseurDialog()
        if dialog.exec():
            self._load_fournisseurs()

    def _edit(self):
        fid = self._selected_id()
        if not fid:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un fournisseur")
            return

        fournisseur = FournisseurService.get_fournisseur(fid)
        dialog = FournisseurDialog(fournisseur)
        if dialog.exec():
            self._load_fournisseurs()

    def _delete(self):
        fid = self._selected_id()
        if not fid:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un fournisseur")
            return

        if QMessageBox.question(
            self, "Confirmation", "Supprimer ce fournisseur ?"
        ) == QMessageBox.Yes:
            FournisseurService.supprimer_fournisseur(fid)
            self._load_fournisseurs()