from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QLabel, QHBoxLayout, QSpinBox
)

from utils import encode_text, decode_text

class CryptoTab(QWidget):
    def __init__(self, crypto_class):
        super().__init__()
        self.crypto_class = crypto_class

        self.client1 = None
        self.client2 = None

        layout = QVBoxLayout()

        # --- битность ---
        bits_layout = QHBoxLayout()
        self.bits_input = QSpinBox()
        self.bits_input.setRange(8, 512)
        self.bits_input.setValue(32)

        gen_btn = QPushButton("Generate Keys")
        gen_btn.clicked.connect(self.generate_keys)

        bits_layout.addWidget(QLabel("Bits:"))
        bits_layout.addWidget(self.bits_input)
        bits_layout.addWidget(gen_btn)

        layout.addLayout(bits_layout)

        # --- сообщения ---
        self.input1 = QTextEdit()
        self.input2 = QTextEdit()

        self.input1.setPlaceholderText("Client A message")
        self.input2.setPlaceholderText("Client B message")

        send1 = QPushButton("A → B")
        send2 = QPushButton("B → A")

        send1.clicked.connect(self.send_a_to_b)
        send2.clicked.connect(self.send_b_to_a)

        layout.addWidget(self.input1)
        layout.addWidget(send1)
        layout.addWidget(self.input2)
        layout.addWidget(send2)

        # --- лог ---
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        layout.addWidget(QLabel("Logs:"))
        layout.addWidget(self.log)

        self.setLayout(layout)

    def log_msg(self, text):
        self.log.append(text)

    def generate_keys(self):
        bits = self.bits_input.value()

        self.client1 = self.crypto_class(bits)
        self.client2 = self.crypto_class(bits)

        self.crypto_class.exchange(self.client1, self.client2)

        self.log_msg("=== Keys generated ===")
        self.log_msg(f"A pub: {self.client1.public_key}")
        self.log_msg(f"B pub: {self.client2.public_key}")
        self.log_msg("")

    def send_a_to_b(self):
        if not self.client1:
            return

        text = self.input1.toPlainText()
        msg = encode_text(text, "eng")

        self.log_msg(f"[A] Plain: {text} ({msg})")

        ct = self.client1.send_message(msg)
        self.log_msg(f"[A] Cipher: {ct}")

        pt = self.client2.read_message(ct)
        decoded = decode_text(pt, "eng")

        self.log_msg(f"[B] Decrypted: {decoded} ({pt})")
        self.log_msg("")

    def send_b_to_a(self):
        if not self.client2:
            return

        text = self.input2.toPlainText()
        msg = encode_text(text, "eng")

        self.log_msg(f"[B] Plain: {text} ({msg})")

        ct = self.client2.send_message(msg)
        self.log_msg(f"[B] Cipher: {ct}")

        pt = self.client1.read_message(ct)
        decoded = decode_text(pt, "eng")

        self.log_msg(f"[A] Decrypted: {decoded} ({pt})")
        self.log_msg("")