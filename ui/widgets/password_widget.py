from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit
from gui.models.password_model import PasswordModel

class PasswordWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.model = PasswordModel()
        self.layout = QVBoxLayout()
        self.password_field = QLineEdit()
        self.password_field.setReadOnly(True)
        self.generate_button = QPushButton("Générer un mot de passe")
        self.generate_button.clicked.connect(self.generate_password)
        self.layout.addWidget(self.password_field)
        self.layout.addWidget(self.generate_button)
        self.setLayout(self.layout)

    def generate_password(self):
        password = self.model.generate_password()
        self.password_field.setText(password) 