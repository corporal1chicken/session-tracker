from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QDialog, QLineEdit, QCheckBox, QWidget)
from PyQt5.QtCore import Qt, QTimer

class BaseDialog(QDialog):
    def __init__(self, parent=None, title="Dialog", width=250, height=180):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(width, height)

        self.main_layout = QVBoxLayout(self)

        self.error_label = QLabel("abcdef")
        self.error_label.setStyleSheet("color: red; font-size: 11px")
        self.error_label.hide()
        self.error_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.error_label)

        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 14px; padding: 2px")
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.main_layout.addWidget(self.content_widget)

        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)
        
    def set_header(self, text):
        self.title_label.setText(text)

    def create_button(self, text, callback):
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        self.button_layout.addWidget(btn)

        return btn
    
    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.show()

        QTimer.singleShot(4000, self.error_label.hide)
    
class NewGroupDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(parent, "Create New Group")
        self.set_header("Enter group name:")

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Name")
        self.input_name.setStyleSheet("padding: 4px; border-bottom: 1px;")
        self.content_layout.addWidget(self.input_name)

        self.create_btn = self.create_button("Create", self.on_create_clicked)
        self.cancel_btn = self.create_button("Cancel", self.reject)

    def on_create_clicked(self):
        name = self.input_name.text().strip()

        if name == "":
            self.show_error("Name cannot be blank")
            return
        elif len(name) > 12:
            self.show_error("Name cannot be more than 12 characters")
            return

        self.accept()

    def get_name(self):
        return self.input_name.text()
    
class DeleteGroupDialog(BaseDialog):
    def __init__(self, parent=None, passed_name=""):
        super().__init__(parent, "Delete Group")
        self.set_header(f"Are you sure you want to delete {passed_name}")

        self.continue_btn = self.create_button("Continue", self.accept)
        self.cancel_btn = self.create_button("Cancel", self.reject)

class AddItemDialog(BaseDialog):
    def __init__(self, parent=None, passed_group=""):
        super().__init__(parent, "Add Item")
        self.set_header(f"Enter the item name to add to {passed_group}")

        self.passed_group = passed_group

        self.input_item = QLineEdit()
        self.input_item.setPlaceholderText("Item Name")
        self.input_item.setStyleSheet("padding: 4px; border-bottom: 1px;")
        self.content_layout.addWidget(self.input_item)

        self.create_btn = self.create_button("Add", self.on_add_clicked)
        self.cancel_btn = self.create_button("Cancel", self.reject)

    def on_add_clicked(self):
        item = self.input_item.text().strip()

        if len(item) == 0:
            self.show_error("Item cannot be blank")
            return
        elif len(item) > 24:
            self.show_error("Item cannot be more than 24 characters")
            return
        
        self.accept()

    def get_item(self):
        return self.input_item.text()
          
class RemoveItemDialog(BaseDialog):
    def __init__(self, parent=None, passed_name=None, passed_items=None):
        super().__init__(parent, "Remove Items", 480, 240)
        self.group_name = passed_name
        self.group_items = passed_items
        self.checked_items = []

        self.set_header(f"Select items to remove from {passed_name}")

        self.checkbox_buttons = []
        
        for text in self.group_items:
            checkbox = QCheckBox(text)
            self.content_layout.addWidget(checkbox)
            self.checkbox_buttons.append(checkbox)

        self.remove_btn = self.create_button("Remove", self.on_remove_clicked)
        self.cancel_btn = self.create_button("Cancel", self.reject)

    def on_remove_clicked(self):
        for btn in self.checkbox_buttons:
            if btn.isChecked():
                self.checked_items.append(btn.text())

        self.accept()

    def get_checked_items(self):
        return self.checked_items

class StartSessionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Start Session")
        self.setFixedSize(320, 220)

        self.time = 20
        
        layout = QVBoxLayout(self)
        
        self.time_label = QLabel(f"{self.time} minutes")
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
        self.time_label.setText(f"{self.time} minutes")

    def decrement_minute(self):
        if self.time <= 1:
            pass
        else:
            self.time -= 1
            self.time_label.setText(f"{self.time} minutes")

    def get_details(self):
        name = self.input_name.text() if not self.input_name.text() == "" else "New Session"
        return self.time, name
    
class SessionEnded(BaseDialog):
    def __init__(self, parent=None, text=None):
        super().__init__(parent, "Session Complete")

        self.set_header(text)
        self.save_btn = self.create_button("Save", self.accept)
    
class RestartSessionDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(parent, "Restart Session")

        self.option = "hard_reset"

        self.set_header("How would you like to restart?")

        self.hard_reset_btn = self.create_button("Pick new item", self.hard_reset)        
        self.soft_reset_btn = self.create_button("Keep current item", (self.soft_reset))

    def hard_reset(self):
        self.option = "hard_reset"
        self.accept()

    def soft_reset(self):
        self.option = "soft_reset"
        self.accept()

    def get_option(self):
        return self.option