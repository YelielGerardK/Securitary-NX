from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from gui.widgets.password_widget import PasswordWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Générateur de mots de passe sécurisés")
        central_widget = QWidget()
        layout = QVBoxLayout()
        self.password_widget = PasswordWidget()
        layout.addWidget(self.password_widget)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget) 