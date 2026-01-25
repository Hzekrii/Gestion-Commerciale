from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QComboBox, QLineEdit, QPushButton, QMessageBox
)
from app.services.article_service import ArticleService
from app.services.stock_service import StockService


class StockDialog(QDialog):
    def __init__(self, mode="ENTREE"):
        super().__init__()

        self.mode = mode
        self.setWindowTitle("Entrée Stock" if mode == "ENTREE" else "Sortie Stock")
        self.setFixedSize(300, 220)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        self.article_combo = QComboBox()
        self.articles = ArticleService.lister_articles()
        for a in self.articles:
            self.article_combo.addItem(f"{a.code} - {a.designation}", a.id)

        self.qty_input = QLineEdit()
        self.comment_input = QLineEdit()

        form.addRow("Article :", self.article_combo)
        form.addRow("Quantité :", self.qty_input)
        form.addRow("Commentaire :", self.comment_input)

        btn = QPushButton("Valider")
        btn.clicked.connect(self._save)

        layout.addLayout(form)
        layout.addWidget(btn)
        self.setLayout(layout)

    def _save(self):
        try:
            article_id = self.article_combo.currentData()
            qty = int(self.qty_input.text())
            comment = self.comment_input.text()

            if self.mode == "ENTREE":
                StockService.entree_stock(article_id, qty, comment)
            else:
                StockService.sortie_stock(article_id, qty, comment)

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))