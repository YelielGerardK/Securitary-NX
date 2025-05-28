from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QCheckBox, QLabel, QSpinBox, QFileDialog, QMessageBox, QSlider, QGroupBox, QFormLayout, QScrollArea, QFrame, QProgressBar
)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QIcon, QFont
from gui.models.password_model import PasswordModel
from utils.clipboard import copy_to_clipboard
from utils.export import export_passwords_txt, export_passwords_csv
from config.app_config import (
    DEFAULT_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH,
    DEFAULT_USE_UPPERCASE, DEFAULT_USE_LOWERCASE, DEFAULT_USE_DIGITS, DEFAULT_USE_SYMBOLS, DEFAULT_EXCLUDE_AMBIGUOUS
)
import os
import psutil
import time

ASSETS = os.path.join(os.path.dirname(__file__), '../../assets')

def icon_path(name):
    return os.path.abspath(os.path.join(ASSETS, name))

class PasswordGenWorker(QThread):
    finished = Signal(list)
    progress = Signal(int)
    resource = Signal(float, float)

    def __init__(self, count, options):
        super().__init__()
        self.count = count
        self.options = options
        self._running = True

    def run(self):
        from core.password_generator import generate_multiple_passwords
        process = psutil.Process(os.getpid())
        results = []
        batch = max(1, self.count // 100)  # Pour la progression
        for i in range(0, self.count, batch):
            if not self._running:
                break
            n = min(batch, self.count - i)
            results.extend(generate_multiple_passwords(count=n, **self.options))
            self.progress.emit(int((i + n) * 100 / self.count))
            # Retour CPU/mémoire
            cpu = process.cpu_percent(interval=0.05)
            mem = process.memory_info().rss / (1024 * 1024)
            self.resource.emit(cpu, mem)
        if self._running:
            self.finished.emit(results)

    def stop(self):
        self._running = False

class PasswordWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.model = PasswordModel()
        self.init_ui()
        self.passwords = []
        self.worker = None

    def init_ui(self):
        layout = QVBoxLayout()
        form_group = QGroupBox("Options de génération")
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(8)

        # Longueur
        self.length_spin = QSpinBox()
        self.length_spin.setRange(MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH)
        self.length_spin.setValue(DEFAULT_PASSWORD_LENGTH)
        form_layout.addRow("Longueur :", self.length_spin)

        # Types de caractères
        self.uppercase_cb = QCheckBox("Majuscules (A-Z)")
        self.uppercase_cb.setChecked(DEFAULT_USE_UPPERCASE)
        self.lowercase_cb = QCheckBox("Minuscules (a-z)")
        self.lowercase_cb.setChecked(DEFAULT_USE_LOWERCASE)
        self.digits_cb = QCheckBox("Chiffres (0-9)")
        self.digits_cb.setChecked(DEFAULT_USE_DIGITS)
        self.symbols_cb = QCheckBox("Symboles (!@#)")
        self.symbols_cb.setChecked(DEFAULT_USE_SYMBOLS)
        form_layout.addRow(self.uppercase_cb)
        form_layout.addRow(self.lowercase_cb)
        form_layout.addRow(self.digits_cb)
        form_layout.addRow(self.symbols_cb)

        # Exclusion des ambigus
        self.ambiguous_cb = QCheckBox("Exclure les caractères ambigus (l, 1, O, 0)")
        self.ambiguous_cb.setChecked(DEFAULT_EXCLUDE_AMBIGUOUS)
        form_layout.addRow(self.ambiguous_cb)

        # Nombre de mots de passe (pour version Pro)
        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 100)
        self.count_spin.setValue(1)
        form_layout.addRow("Nombre de mots de passe :", self.count_spin)

        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        # Zone scrollable pour les mots de passe
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.result_widget = QWidget()
        self.result_layout = QVBoxLayout()
        self.result_layout.setSpacing(6)
        self.result_widget.setLayout(self.result_layout)
        self.scroll_area.setWidget(self.result_widget)
        layout.addWidget(self.scroll_area, stretch=1)

        # Feedback visuel
        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.feedback_label)

        # Indicateur d'activité et ressources
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        self.resource_label = QLabel("")
        self.resource_label.setAlignment(Qt.AlignCenter)
        self.resource_label.setVisible(False)
        layout.addWidget(self.resource_label)

        # Boutons
        btn_layout = QHBoxLayout()
        self.generate_button = QPushButton("Générer")
        self.generate_button.setIcon(QIcon(icon_path('refresh.svg')) if os.path.exists(icon_path('refresh.svg')) else QIcon())
        self.generate_button.clicked.connect(self.generate_passwords)
        btn_layout.addWidget(self.generate_button)

        self.copy_button = QPushButton()
        self.copy_button.setIcon(QIcon(icon_path('copy.svg')) if os.path.exists(icon_path('copy.svg')) else QIcon())
        self.copy_button.setToolTip("Copier tout")
        self.copy_button.clicked.connect(self.copy_password)
        btn_layout.addWidget(self.copy_button)

        self.export_txt_button = QPushButton()
        self.export_txt_button.setIcon(QIcon(icon_path('txt.svg')) if os.path.exists(icon_path('txt.svg')) else QIcon())
        self.export_txt_button.setToolTip("Exporter TXT")
        self.export_txt_button.clicked.connect(self.export_txt)
        btn_layout.addWidget(self.export_txt_button)

        self.export_csv_button = QPushButton()
        self.export_csv_button.setIcon(QIcon(icon_path('csv.svg')) if os.path.exists(icon_path('csv.svg')) else QIcon())
        self.export_csv_button.setToolTip("Exporter CSV")
        self.export_csv_button.clicked.connect(self.export_csv)
        btn_layout.addWidget(self.export_csv_button)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def get_options(self):
        return {
            'length': self.length_spin.value(),
            'use_uppercase': self.uppercase_cb.isChecked(),
            'use_lowercase': self.lowercase_cb.isChecked(),
            'use_digits': self.digits_cb.isChecked(),
            'use_symbols': self.symbols_cb.isChecked(),
            'exclude_ambiguous': self.ambiguous_cb.isChecked(),
        }

    def clear_results(self):
        while self.result_layout.count():
            child = self.result_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def generate_passwords(self):
        options = self.get_options()
        count = self.count_spin.value()
        # Si beaucoup de mots de passe ou très long, lance en asynchrone
        if count > 1 or options['length'] > 100_000:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.resource_label.setVisible(True)
            self.feedback_label.setText("<i>Génération en cours...</i>")
            self.generate_button.setEnabled(False)
            self.worker = PasswordGenWorker(count, options)
            self.worker.finished.connect(self.on_gen_finished)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.resource.connect(self.update_resource)
            self.worker.start()
        else:
            try:
                if count > 1:
                    self.passwords = self.model.generate_multiple(count=count, **options)
                else:
                    pwd = self.model.generate_password(**options)
                    self.passwords = [pwd]
            except ValueError as e:
                self.clear_results()
                self.feedback_label.setText(f'<span style="color: #d32f2f; font-weight: bold;">{str(e)}</span>')
                QTimer.singleShot(4000, lambda: self.feedback_label.setText(""))
                return
            self.display_passwords()

    def on_gen_finished(self, results):
        self.passwords = results
        self.display_passwords()
        self.progress_bar.setVisible(False)
        self.resource_label.setVisible(False)
        self.generate_button.setEnabled(True)

    def update_resource(self, cpu, mem):
        self.resource_label.setText(f"CPU : {cpu:.1f}% | Mémoire : {mem:.1f} Mo")

    def display_passwords(self):
        self.clear_results()
        for pwd in self.passwords:
            row = QHBoxLayout()
            pwd_label = QLabel(pwd)
            pwd_label.setFont(QFont("Consolas", 12, QFont.Bold))
            pwd_label.setProperty('role', 'password')
            pwd_label.setStyleSheet("")
            row.addWidget(pwd_label)
            copy_btn = QPushButton()
            copy_btn.setIcon(QIcon(icon_path('copy.svg')) if os.path.exists(icon_path('copy.svg')) else QIcon())
            copy_btn.setToolTip("Copier ce mot de passe")
            copy_btn.setFixedSize(32, 32)
            copy_btn.setStyleSheet("border: none; padding: 0; outline: none;")
            copy_btn.setFocusPolicy(Qt.StrongFocus)
            copy_btn.clicked.connect(lambda _, p=pwd: self.copy_single_password(p))
            row.addWidget(copy_btn)
            row.addStretch()
            frame = QFrame()
            frame.setLayout(row)
            self.result_layout.addWidget(frame)
        self.feedback_label.setText('<span style="color: #43a047; font-weight: bold;">✔ Mots de passe générés !</span>')
        QTimer.singleShot(2000, lambda: self.feedback_label.setText(""))

    def copy_password(self):
        if self.passwords:
            copy_to_clipboard('\n'.join(self.passwords))
            self.feedback_label.setText('<span style="color: #43a047; font-weight: bold;">✔ Tous copiés !</span>')
            QTimer.singleShot(2000, lambda: self.feedback_label.setText(""))

    def copy_single_password(self, pwd):
        copy_to_clipboard(pwd)
        self.feedback_label.setText('<span style="color: #43a047; font-weight: bold;">✔ Copié !</span>')
        QTimer.singleShot(2000, lambda: self.feedback_label.setText(""))

    def export_txt(self):
        if not self.passwords:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Exporter en TXT", "passwords.txt", "Fichiers texte (*.txt)")
        if path:
            export_passwords_txt(self.passwords, path)
            QMessageBox.information(self, "Export", "Export TXT réussi !")

    def export_csv(self):
        if not self.passwords:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Exporter en CSV", "passwords.csv", "Fichiers CSV (*.csv)")
        if path:
            export_passwords_csv(self.passwords, path)
            QMessageBox.information(self, "Export", "Export CSV réussi !") 