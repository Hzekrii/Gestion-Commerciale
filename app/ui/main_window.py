from PySide6.QtWidgets import QMainWindow, QLabel, QMessageBox
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from app.ui.article_window import ArticleWindow
from app.ui.client_window import ClientWindow
from app.ui.fournisseur_window import FournisseurWindow
from app.ui.stock_dialog import StockDialog


class MainWindow(QMainWindow):
    def __init__(self, utilisateur):
        super().__init__()

        self.utilisateur = utilisateur

        self.setWindowTitle("Gestion Commerciale")
        self.resize(900, 600)

        self._build_ui()
        self._build_menu()

    def _build_ui(self):
        label = QLabel(
            f"Bienvenue {self.utilisateur.nom_utilisateur}",
            alignment=Qt.AlignCenter
        )
        self.setCentralWidget(label)

    def _build_menu(self):
        menubar = self.menuBar()

        # ===== FICHIER =====
        menu_fichier = menubar.addMenu("Fichier")
        action_quitter = QAction("Quitter", self)
        action_quitter.triggered.connect(self.close)
        menu_fichier.addAction(action_quitter)

        # ===== GESTION =====
        menu_gestion = menubar.addMenu("Gestion")

        action_articles = QAction("Articles", self)
        action_articles.triggered.connect(self._open_articles)
        menu_gestion.addAction(action_articles)

        action_clients = QAction("Clients", self)
        action_clients.triggered.connect(self._open_clients)
        menu_gestion.addAction(action_clients)

        action_fournisseurs = QAction("Fournisseurs", self)
        action_fournisseurs.triggered.connect(self._open_fournisseurs)
        menu_gestion.addAction(action_fournisseurs)

        # ===== STOCK =====
        menu_stock = menubar.addMenu("Stock")

        action_entree = QAction("Entrée stock", self)
        action_entree.triggered.connect(self._entree_stock)
        menu_stock.addAction(action_entree)

        action_sortie = QAction("Sortie stock", self)
        action_sortie.triggered.connect(self._sortie_stock)
        menu_stock.addAction(action_sortie)

        # ===== AIDE =====
        menu_aide = menubar.addMenu("Aide")

        action_apropos = QAction("À propos", self)
        action_apropos.triggered.connect(self._a_propos)
        menu_aide.addAction(action_apropos)

        # ===== DROITS (V1 simple) =====
        if self.utilisateur.role_id != 1:  # 1 = ADMIN
            action_fournisseurs.setEnabled(False)

    # ===== ACTIONS =====
    def _open_articles(self):
        self.article_window = ArticleWindow()
        self.article_window.show()

    def _open_clients(self):
        self.client_window = ClientWindow()
        self.client_window.show()

    def _open_fournisseurs(self):
        self.fournisseur_window = FournisseurWindow()
        self.fournisseur_window.show()

    def _entree_stock(self):
        dialog = StockDialog("ENTREE")
        dialog.exec()

    def _sortie_stock(self):
        dialog = StockDialog("SORTIE")
        dialog.exec()

    def _a_propos(self):
        QMessageBox.about(
            self,
            "À propos",
            "Gestion Commerciale\nVersion 1.0\nDéveloppé en Python + PySide6"
        )