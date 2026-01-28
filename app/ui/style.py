APP_STYLE = """
QMainWindow {
    background-color: #f4f6f9;
}

QWidget {
    font-family: Segoe UI;
    font-size: 13px;
}

QMenuBar {
    background-color: #2c3e50;
    color: white;
}

QMenuBar::item {
    padding: 8px 15px;
    background: transparent;
}

QMenuBar::item:selected {
    background: #34495e;
}

QMenu {
    background-color: #2c3e50;
    color: white;
}

QMenu::item:selected {
    background-color: #34495e;
}

QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:disabled {
    background-color: #bdc3c7;
}

QTableWidget {
    background-color: white;
    border: 1px solid #dcdcdc;
}

QHeaderView::section {
    background-color: #ecf0f1;
    padding: 5px;
    border: none;
    font-weight: bold;
}

QLineEdit, QComboBox {
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 4px;
}
"""