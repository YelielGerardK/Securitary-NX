from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, QMenuBar, QMessageBox
from PySide6.QtGui import QAction
from gui.widgets.password_widget import PasswordWidget
from PySide6.QtCore import Qt

SOFTWARE_NAME = "Securitary-NX"
SOFTWARE_VERSION = "v1.0.0"
SOFTWARE_DESCRIPTION = "Un générateur de mots de passe sécurisé et personnalisable."
SOFTWARE_CREATOR = "Rabenandrasana Yeliel Gerard"
SOFTWARE_CONTACT = ""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(SOFTWARE_NAME)
        central_widget = QWidget()
        layout = QVBoxLayout()
        self.password_widget = PasswordWidget()
        layout.addWidget(self.password_widget)
        # Bouton de thème
        self.theme_button = QPushButton("🌙 Thème sombre")
        self.theme_button.setCheckable(True)
        self.theme_button.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_button, alignment=Qt.AlignRight)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.is_dark = False
        self.apply_light_theme()
        self.init_menu()

    def init_menu(self):
        menubar = QMenuBar(self)
        # Menu Fichier
        file_menu = menubar.addMenu("Fichier")
        quit_action = QAction("Quitter", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        file_menu.addAction(quit_action)
        # Menu Aide
        help_menu = menubar.addMenu("Aide")
        about_action = QAction("À propos", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        self.setMenuBar(menubar)

    def show_about(self):
        text = f"<b>{SOFTWARE_NAME}</b><br>"
        text += f"Version : {SOFTWARE_VERSION}<br>"
        text += f"Créateur : {SOFTWARE_CREATOR}<br>"
        text += f"<i>{SOFTWARE_DESCRIPTION}</i><br>"
        if SOFTWARE_CONTACT:
            text += f"Contact : {SOFTWARE_CONTACT}<br>"
        msg = QMessageBox(self)
        msg.setWindowTitle(f"À propos de {SOFTWARE_NAME}")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Close)
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("QLabel{min-width:320px; font-size:14px;} QMessageBox{background:#f6f8fa;}")
        msg.exec()

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        if self.is_dark:
            self.theme_button.setText("☀️ Thème clair")
            self.apply_dark_theme()
        else:
            self.theme_button.setText("🌙 Thème sombre")
            self.apply_light_theme()

    def apply_dark_theme(self):
        dark = """
        QWidget { background: #23272e; color: #f1f1f1; }
        QLineEdit, QSpinBox, QGroupBox, QCheckBox, QLabel { background: #23272e; color: #f1f1f1; }
        QGroupBox { border: 1px solid #444950; margin-top: 10px; }
        QCheckBox::indicator { border: 1px solid #888; background: #23272e; }
        QCheckBox::indicator:checked { background: #1976d2; border: 1px solid #1976d2; }
        QPushButton { background: #1976d2; color: #fff; border-radius: 6px; padding: 6px 12px; font-weight: 500; }
        QPushButton:pressed { background: #1565c0; }
        QPushButton:disabled { background: #444950; color: #888; }
        QPushButton:hover { background: #2196f3; }
        QScrollArea { background: #23272e; border: 1px solid #444950; }
        QFrame { background: transparent; }
        QLabel[role='password'] { color: #90caf9; font-weight: bold; background: transparent; }
        """
        QApplication.instance().setStyleSheet(dark)

    def apply_light_theme(self):
        light = """
        QWidget { background: #f6f8fa; color: #23272e; }
        QLineEdit, QSpinBox, QGroupBox, QCheckBox, QLabel { background: #f6f8fa; color: #23272e; }
        QGroupBox { border: 1px solid #b0b0b0; margin-top: 10px; }
        QCheckBox::indicator { border: 1px solid #1976d2; background: #fff; }
        QCheckBox::indicator:checked { background: #1976d2; border: 1px solid #1976d2; }
        QPushButton { background: #1976d2; color: #fff; border-radius: 6px; padding: 6px 12px; font-weight: 500; }
        QPushButton:pressed { background: #1565c0; }
        QPushButton:disabled { background: #b0b0b0; color: #fff; }
        QPushButton:hover { background: #2196f3; }
        QScrollArea { background: #f6f8fa; border: 1px solid #b0b0b0; }
        QFrame { background: transparent; }
        QLabel[role='password'] { color: #1976d2; font-weight: bold; background: transparent; }
        """
        QApplication.instance().setStyleSheet(light) 