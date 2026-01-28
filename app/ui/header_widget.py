from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class HeaderWidget(QWidget):
    def __init__(self, title: str, subtitle: str = ""):
        super().__init__()

        title_label = QLabel(title)
        title_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #2c3e50;"
        )

        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet(
            "color: #7f8c8d;"
        )

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        if subtitle:
            layout.addWidget(subtitle_label)
        layout.addSpacing(10)

        self.setLayout(layout)