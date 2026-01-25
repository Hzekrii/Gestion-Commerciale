from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QMessageBox
)

from app.services.article_service import ArticleService


class ArticleDialog(QDialog):
    def __init__(self, article=None):
        super().__init__()

        self.article = article  # None = ajout, sinon modification

        self.setWindowTitle(
            "Ajouter Article" if article is None else "Modifier Article"
        )
        self.setFixedSize(300, 250)

        self._build_ui()

        if self.article:
            self._load_article()

    def _build_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        self.code_input = QLineEdit()
        self.designation_input = QLineEdit()
        self.prix_achat_input = QLineEdit()
        self.prix_vente_input = QLineEdit()

        form.addRow("Code :", self.code_input)
        form.addRow("Désignation :", self.designation_input)
        form.addRow("Prix achat :", self.prix_achat_input)
        form.addRow("Prix vente :", self.prix_vente_input)

        btn_save = QPushButton("Enregistrer")
        btn_save.clicked.connect(self._save)

        layout.addLayout(form)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def _load_article(self):
        self.code_input.setText(self.article.code)
        self.designation_input.setText(self.article.designation)
        self.prix_achat_input.setText(str(self.article.prix_achat))
        self.prix_vente_input.setText(str(self.article.prix_vente))

    def _save(self):
        try:
            code = self.code_input.text().strip()
            designation = self.designation_input.text().strip()
            prix_achat = float(self.prix_achat_input.text())
            prix_vente = float(self.prix_vente_input.text())

            if not code or not designation:
                raise ValueError("Champs obligatoires manquants")

            if self.article is None:
                ArticleService.creer_article(
                    code=code,
                    designation=designation,
                    prix_achat=prix_achat,
                    prix_vente=prix_vente,
                    tva_id=1
                )
            else:
                self.article.code = code
                self.article.designation = designation
                self.article.prix_achat = prix_achat
                self.article.prix_vente = prix_vente

                ArticleService.modifier_article(self.article)

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))