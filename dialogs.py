from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QDialog, QLineEdit, QCheckBox)
from PyQt5.QtCore import Qt

class AddItemDialog(QDialog):
    group = None
    def __init__(self, parent=None, passed_group=None):
        super().__init__(parent)
        self.group = passed_group
        self.setWindowTitle(f"Add to {passed_group}")
        self.setFixedSize(240, 120)
        
        layout = QVBoxLayout(self)
        label = QLabel("Add Item")
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
        self.parent().add_item_to_group(self.group, self.input_item.text())

        self.accept()

    def cancel(self):
        self.accept()

    def update_add_btn(self, text):
        self.add_btn.setText(f"Add {text}")

class NewGroupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Group")
        self.setFixedSize(240, 120)
        
        layout = QVBoxLayout(self)
        label = QLabel("Enter Group Name")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Search Bar
        self.input_item = QLineEdit()
        self.input_item.setPlaceholderText("Enter")
        self.input_item.setStyleSheet("padding: 8px; border-bottom: 1px;")
        #self.input_item.textChanged.connect(self.update_add_btn)
        layout.addWidget(self.input_item)

        btn_layout = QHBoxLayout()
  
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.add)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

    def add(self):
        print(self.input_item.text())
        self.parent().add_group(self.input_item.text(), [])
        self.accept()

    def cancel(self):
        self.accept()

class RemoveItemDialog(QDialog):
    group_name = ""
    group_items = ""
    def __init__(self, parent=None, passed_name=None, passed_items=None):
        super().__init__(parent)
        self.group_name = passed_name
        self.group_items = passed_items
        self.setWindowTitle("Remove Item")
        self.setFixedSize(480, 240)

        layout = QVBoxLayout(self)
        self.message_label = QLabel("Remove Item:")
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)

        self.checkbox_buttons = []
        
        for text in self.group_items:
            checkbox = QCheckBox(text)
            layout.addWidget(checkbox)
            self.checkbox_buttons.append(checkbox)
          
        btn_layout = QHBoxLayout()
        self.continue_btn = QPushButton("Remove")
        self.continue_btn.clicked.connect(self.remove_items)
        btn_layout.addWidget(self.continue_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)

    def remove_items(self):
        checked_items = []

        for btn in self.checkbox_buttons:
            if btn.isChecked():
                checked_items.append(btn.text())
        
        self.parent().remove_items_from_group(self.group_name, checked_items)
        self.accept()