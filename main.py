import sys
from PySide6.QtWidgets import QApplication
from app.ui.style import APP_STYLE
from app.ui.login_window import LoginWindow


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()