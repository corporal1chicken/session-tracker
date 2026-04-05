from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QDialog, QLineEdit, QCheckBox)
from PyQt5.QtCore import Qt

class AddItemDialog(QDialog):
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
        #self.input_item.textChanged.connect(self.update_add_btn)
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
        self.parent().add_item(self.group, self.input_item.text())

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
        self.parent().add_group(self.input_item.text(), [], True, True)
        self.accept()

    def cancel(self):
        self.accept()

class RemoveItemDialog(QDialog):
    def __init__(self, parent=None, passed_name=None, passed_items=None):
        super().__init__(parent)
        self.group_name = passed_name
        self.group_items = passed_items
        self.setWindowTitle("Remove Item")
        self.setFixedSize(480, 240)

        layout = QVBoxLayout(self)
        self.message_label = QLabel(f"Select items to remove from {passed_name}")
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
        
        self.parent().remove_items(self.group_name, checked_items)
        self.accept()

class DeleteGroupDialog(QDialog):
    def __init__(self, parent=None, passed_name=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Group?")
        self.setFixedSize(240, 120)

        self.group_name = passed_name
        
        layout = QVBoxLayout(self)
        self.message_label = QLabel(f"Are you sure you want to delete {self.group_name}?")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)

        btn_layout = QHBoxLayout()
  
        self.continue_btn = QPushButton("Continue")
        self.continue_btn.clicked.connect(self.close_message)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.accept)

        btn_layout.addWidget(self.continue_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

    def close_message(self):
        self.parent().delete_group(self.group_name)
        self.accept()

class MessageDialog(QDialog):
    def __init__(self, parent=None, title=None, text=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(240, 120)
        
        layout = QVBoxLayout(self)
        self.message_label = QLabel(text)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)

        btn_layout = QHBoxLayout()
  
        btn = QPushButton("Continue")
        btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

class StartSessionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Start Session")
        self.setFixedSize(320, 220)

        self.time = 20
        
        layout = QVBoxLayout(self)
        
        self.time_label = QLabel(f"{self.time} Minutes")
        self.time_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.time_label)

        btn_layout = QHBoxLayout()
  
        self.increment_btn = QPushButton("+1 minute")
        self.increment_btn.clicked.connect(self.increment_minute)
        
        self.decrement_btn = QPushButton("-1 minute")
        self.decrement_btn.clicked.connect(self.decrement_minute)

        btn_layout.addWidget(self.increment_btn)
        btn_layout.addWidget(self.decrement_btn)
        layout.addLayout(btn_layout)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Enter Session Name")
        self.input_name.setStyleSheet("padding: 8px; border-bottom: 1px;")
        layout.addWidget(self.input_name)

        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.accept)

        layout.addWidget(self.start_btn)

    def increment_minute(self):
        self.time += 1
        self.time_label.setText(f"{self.time} Minutes")

    def decrement_minute(self):
        if self.time <= 1:
            print("Cannot be less than 2 minutes")
        else:
            self.time -= 1
            self.time_label.setText(f"{self.time} Minutes")

    def get_details(self):
        name = self.input_name.text() if not self.input_name.text() == "" else "New Session"
        return self.time, name
    
class SessionEnded(QDialog):
    def __init__(self, parent=None, text=None):
        super().__init__(parent)
        self.setWindowTitle("Session Complete")
        self.setFixedSize(240, 120)
        
        layout = QVBoxLayout(self)
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        btn_layout = QHBoxLayout()
  
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)
    
class RestartSessionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Restart Session?")
        self.setFixedSize(240, 120)

        self.option = "hard_reset"

        layout = QVBoxLayout(self)
        self.message_label = QLabel(f"How would you like to restart?")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)

        btn_layout = QHBoxLayout()
  
        self.hard_reset_btn = QPushButton("Pick new item")
        self.hard_reset_btn.clicked.connect(self.hard_reset)
        
        self.soft_reset_btn = QPushButton("Keep current item")
        self.soft_reset_btn.clicked.connect(self.soft_reset)

        btn_layout.addWidget(self.hard_reset_btn)
        btn_layout.addWidget(self.soft_reset_btn)
        layout.addLayout(btn_layout)

    def hard_reset(self):
        self.accept()
        self.option = "hard_reset"

    def soft_reset(self):
        self.accept()
        self.option = "soft_reset"

    def get_option(self):
        return self.option