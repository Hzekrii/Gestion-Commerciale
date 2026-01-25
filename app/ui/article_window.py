from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from PySide6.QtCore import Qt

from app.services.article_service import ArticleService
from app.ui.article_dialog import ArticleDialog
from app.models.article import Article

class ArticleWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Articles")
        self.resize(700, 400)

        self._build_ui()
        self._load_articles()

    def _build_ui(self):
        main_layout = QVBoxLayout()

        # ===== TABLE =====
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Code", "Désignation", "Prix Achat", "Prix Vente"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # ===== BOUTONS =====
        btn_layout = QHBoxLayout()

        btn_add = QPushButton("Ajouter")
        btn_edit = QPushButton("Modifier")
        btn_delete = QPushButton("Supprimer")

        btn_add.clicked.connect(self._add_article)
        btn_edit.clicked.connect(self._edit_article)
        btn_delete.clicked.connect(self._delete_article)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addStretch()

        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def _load_articles(self):
        articles = ArticleService.lister_articles()
        self.table.setRowCount(len(articles))

        for row, article in enumerate(articles):
            self.table.setItem(row, 0, QTableWidgetItem(str(article.id)))
            self.table.setItem(row, 1, QTableWidgetItem(article.code))
            self.table.setItem(row, 2, QTableWidgetItem(article.designation))
            self.table.setItem(row, 3, QTableWidgetItem(str(article.prix_achat)))
            self.table.setItem(row, 4, QTableWidgetItem(str(article.prix_vente)))

    def _get_selected_article_id(self):
        row = self.table.currentRow()
        if row == -1:
            return None
        return int(self.table.item(row, 0).text())

    # ===== ACTIONS (PLACEHOLDERS) =====
    def _add_article(self):
        dialog = ArticleDialog()
        if dialog.exec():
            self._load_articles()

    def _edit_article(self):
        article_id = self._get_selected_article_id()
        if not article_id:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un article")
            return

        articles = ArticleService.lister_articles()
        article = next((a for a in articles if a.id == article_id), None)

        if article:
            dialog = ArticleDialog(article)
            if dialog.exec():
                self._load_articles()

    def _delete_article(self):
        article_id = self._get_selected_article_id()
        if not article_id:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un article")
            return

        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Voulez-vous vraiment supprimer cet article ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                ArticleService.supprimer_article(article_id)
                self._load_articles()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", str(e))