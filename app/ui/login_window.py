from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt

from app.services.auth_service import AuthService
from app.ui.main_window import MainWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Connexion")
        self.setFixedSize(300, 200)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Connexion")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Se connecter")
        login_button.clicked.connect(self._handle_login)

        layout.addWidget(title)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def _handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs")
            return

        try:
            utilisateur = AuthService.authentifier(username, password)
            self._open_main_window(utilisateur)
        except ValueError as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def _open_main_window(self, utilisateur):
        self.main_window = MainWindow(utilisateur)
        self.main_window.show()
        self.close()