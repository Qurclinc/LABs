import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QProgressBar
from PyQt6.QtCore import Qt

from UI.widgets.primary_button import PrimaryButton
from UI.widgets.app_label import AppLabel
from UI.widgets.panel_frame import PanelFrame
from UI.dialogs.success_dialog import SuccessDialog
from UI.dialogs.error_dialog import ErrorDialog
from Services.crypter import Crypter
from UI.worker import Worker


class CryptoTab(QWidget):
    def __init__(self, mode="encrypt", parent=None):
        super().__init__(parent)
        self.mode = mode
        self.crypter = Crypter()
        self.init_ui()

    def init_ui(self):
        
        self.loader = QProgressBar()
        self.loader.setRange(0, 0)
        self.loader.setVisible(False)
        self.loader.setFormat("PROCESSING...")
        self.loader.setTextVisible(True)

        
        layout = QVBoxLayout(self)
        
        upper_frame = PanelFrame()
        upper_layout = QVBoxLayout(upper_frame)
        upper_frame.setObjectName("MainLayout")

        title = AppLabel(
            f"{self.mode.upper()} FILE",
            size=12,
            bold=True,
            align=Qt.AlignmentFlag.AlignCenter
        )
        upper_layout.addWidget(title)

        # Source
        source_frame = PanelFrame()
        source_layout = QVBoxLayout(source_frame)
        
        source_file_label = AppLabel("SOURCE FILE:", align=Qt.AlignmentFlag.AlignCenter)
        source_layout.addWidget(source_file_label)
        self.source_btn = PrimaryButton("Select File")
        self.source_btn.clicked.connect(self.select_source_file)
        source_layout.addWidget(self.source_btn)

        self.source_label = AppLabel("No file selected", align=Qt.AlignmentFlag.AlignCenter)
        source_layout.addWidget(self.source_label)
        
        source_file_label.setObjectName("NoBorder")
        
        upper_layout.addWidget(source_frame)

        # Key
        key_frame = PanelFrame()
        key_layout = QVBoxLayout(key_frame)

        key_upper_label = AppLabel("ENCRYPTION KEY (PNG/JPG):", align=Qt.AlignmentFlag.AlignCenter)
        key_layout.addWidget(key_upper_label)
        self.key_btn = PrimaryButton("Select Key")
        self.key_btn.setEnabled(False)
        self.key_btn.clicked.connect(self.select_key_file)
        key_layout.addWidget(self.key_btn)

        self.key_label = AppLabel("No key selected", align=Qt.AlignmentFlag.AlignCenter)
        key_layout.addWidget(self.key_label)

        key_upper_label.setObjectName("NoBorder")
        
        upper_layout.addWidget(key_frame)
    
        layout.addWidget(upper_frame)

        self.action_btn = PrimaryButton(self.mode.upper())
        self.action_btn.setEnabled(False)
        self.action_btn.clicked.connect(self.perform_action)
        layout.addWidget(self.action_btn)
        
        layout.addWidget(self.loader)

    def select_source_file(self):
        file_filter = "Encrypted Files (*.pixcrypted)" if self.mode == "decrypt" else "All Files (*)"
        path, _ = QFileDialog.getOpenFileName(self, "Select Source File", "", file_filter)

        if path:
            self.source_file = path
            self.source_label.setText(os.path.basename(path))
            self.key_btn.setEnabled(True)
            self.update_action_button()

    def select_key_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Key Image", "", "Images (*.png *.jpg *.jpeg)"
        )

        if path:
            try:
                self.crypter.set_key(path)
                self.key_file = path
                self.key_label.setText(os.path.basename(path))
                self.update_action_button()
            except Exception as e:
                ErrorDialog(str(e)).exec()

    def update_action_button(self):
        self.action_btn.setEnabled(
            hasattr(self, "source_file") and hasattr(self, "key_file")
        )

    def perform_action(self):
        caption = "Save Encrypted File" if self.mode == "encrypt" else "Save Decrypted File"
        filter_ = "Encrypted Files (*.pixcrypted)" if self.mode == "encrypt" else "All Files (*)"

        output, _ = QFileDialog.getSaveFileName(
            self,
            caption,
            "",
            filter_
        )
        if not output:
            return

        self.action_btn.setEnabled(False)

        self.worker = Worker(
            self.crypter,
            self.mode,
            self.source_file,
            output
        )

        self.worker.finished.connect(self.on_done)
        self.worker.error.connect(self.on_error)
        
        self.action_btn.setEnabled(False)
        self.loader.setVisible(True)
        
        self.worker.start()

        
        
    def on_done(self, ok, message):
        self.loader.setVisible(False)
        self.action_btn.setEnabled(True)
        
        if ok:
            SuccessDialog(message).exec()
        else:
            ErrorDialog(message).exec()

    def on_error(self, msg):
        self.loader.setVisible(False)
        self.action_btn.setEnabled(True)
        
        self.action_btn.setEnabled(True)
        ErrorDialog(msg).exec()
