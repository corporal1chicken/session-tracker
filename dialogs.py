from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QDialog, QLineEdit)
from PyQt5.QtCore import Qt

class AddItemDialog(QDialog):
    def __init__(self, parent=None, group=None):
        super().__init__(parent)
        self.setWindowTitle(f"Add to {group}")
        self.setFixedSize(240, 120)
        
        layout = QVBoxLayout(self)
        label = QLabel("Add an Item")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Search Bar
        self.input_item = QLineEdit()
        self.input_item.setPlaceholderText("Enter")
        self.input_item.setStyleSheet("padding: 8px; border-bottom: 1px;")
        self.input_item.textChanged.connect(self.update_add_btn)
        layout.addWidget(self.input_item)

        btn_layout = QHBoxLayout()
  
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.add_item)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

    def add_item(self):
        print(self.input_item.text())
        self.accept()

    def cancel(self):
        print("Export as .json")
        self.accept()

    def update_add_btn(self, text):
        self.add_btn.setText(f"Add {text}")