from PySide6.QtWidgets import QMainWindow, QMessageBox, QStackedWidget
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

# Pages UI
from app.ui.article_window import ArticleWindow
from app.ui.client_window import ClientWindow
from app.ui.fournisseur_window import FournisseurWindow
from app.ui.facture_window import FactureWindow
from app.ui.stock_dialog import StockDialog
from app.ui.facture_list_window import FactureListWindow


class MainWindow(QMainWindow):
    def __init__(self, utilisateur):
        super().__init__()

        self.utilisateur = utilisateur

        self.setWindowTitle("Gestion Commerciale")
        self.resize(1100, 700)

        self._build_ui()
        self._build_menu()

    # ======================================================
    # UI PRINCIPALE
    # ======================================================
    def _build_ui(self):
        """
        Zone centrale avec navigation interne
        """
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Pages (une seule instance chacune)
        self.page_articles = ArticleWindow()
        self.page_clients = ClientWindow()
        self.page_fournisseurs = FournisseurWindow()
        self.page_factures = FactureWindow()
        self.page_facture_list = FactureListWindow()

        # Ajout au stack
        self.stack.addWidget(self.page_articles)
        self.stack.addWidget(self.page_clients)
        self.stack.addWidget(self.page_fournisseurs)
        self.stack.addWidget(self.page_factures)
        self.stack.addWidget(self.page_facture_list)
        

        # Page par défaut
        self.stack.setCurrentWidget(self.page_articles)

    # ======================================================
    # MENU BAR
    # ======================================================
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

        # ===== FACTURATION =====
        menu_facturation = menubar.addMenu("Facturation")

        action_factures = QAction("Factures", self)
        action_factures.triggered.connect(self._open_factures)
        menu_facturation.addAction(action_factures)

        # ===== Historique FACTURATION =====
        action_historique = QAction("Historique factures", self)
        action_historique.triggered.connect(self._open_historique_factures)
        menu_facturation.addAction(action_historique)

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

        # ===== GESTION DES DROITS (V2 simple) =====
        # Exemple : seul ADMIN peut gérer fournisseurs
        if self.utilisateur.role_id != 1:  # 1 = ADMIN
            action_fournisseurs.setEnabled(False)

    # ======================================================
    # NAVIGATION INTERNE
    # ======================================================
    def _open_articles(self):
        self.stack.setCurrentWidget(self.page_articles)

    def _open_clients(self):
        self.stack.setCurrentWidget(self.page_clients)

    def _open_fournisseurs(self):
        self.stack.setCurrentWidget(self.page_fournisseurs)

    def _open_factures(self):
        self.page_factures.refresh_data()
        self.stack.setCurrentWidget(self.page_factures)
        
    def _open_historique_factures(self):
        self.page_facture_list._load_factures()
        self.stack.setCurrentWidget(self.page_facture_list)
    # ======================================================
    # ACTIONS STOCK
    # ======================================================
    def _entree_stock(self):
        dialog = StockDialog("ENTREE")
        dialog.exec()

    def _sortie_stock(self):
        dialog = StockDialog("SORTIE")
        dialog.exec()

    # ======================================================
    # AIDE
    # ======================================================
    def _a_propos(self):
        QMessageBox.about(
            self,
            "À propos",
            "Gestion Commerciale\n"
            "Version 2.0\n"
            "Python • PySide6 • SQLite\n\n"
            "Application de gestion commerciale"
        )