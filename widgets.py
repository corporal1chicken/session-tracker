from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QPushButton, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from constants import GROUP_BUTTONS
from dialogs import AddItemDialog

class GroupWidget(QWidget):
    def __init__(self, group_name, items, callback):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.items = items
        self.layout.setContentsMargins(0, 5, 0, 15)
        self.layout.setSpacing(8)

        self.container = QFrame()
        self.container.setFixedWidth(300)
        self.container.setStyleSheet("""
            QFrame {
                border: 2px solid black; 
                border-radius: 12px; 
                background-color: white;
            }
        """)
        
        box_layout = QVBoxLayout(self.container)
        box_layout.setContentsMargins(0, 0, 0, 10)
        box_layout.setSpacing(0)

        # Title
        title = QLabel(group_name)
        title.setFixedHeight(45)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 16px; border: none")
        
        # Underline
        underline = QFrame()
        underline.setFrameShape(QFrame.HLine)
        underline.setFixedHeight(2)
        underline.setStyleSheet("background-color: black; margin-left: 10px; margin-right: 10px")
        
        # Items
        items_text = "\n".join(items)
        self.items_label = QLabel(items_text)
        self.items_label.setAlignment(Qt.AlignCenter)
        self.items_label.setStyleSheet("border: none; font-size: 13px; padding: 15px; line-height: 150%;")
        
        box_layout.addWidget(title)
        box_layout.addWidget(underline)
        box_layout.addWidget(self.items_label)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(2)

        btn_container = QWidget()
        btn_container.setFixedWidth(120)
        btn_layout_inner = QHBoxLayout(btn_container)
        btn_layout_inner.setContentsMargins(5, 0, 5, 0)
        
        for k, v in GROUP_BUTTONS.items():
            btn = QPushButton()
            btn.setIcon(QIcon(v['icon']))
            btn.setToolTip(v['tooltip'])
            btn.setFixedSize(32, 32)
            btn.setStyleSheet("""
                QPushButton {
                    border: 1px solid #777; 
                    border-radius: 6px; 
                    background-color: #fcfcfc;
                }
            """)
            btn.clicked.connect(lambda checked, gn=group_name, bi=k: callback(gn, bi))
            btn_layout_inner.addWidget(btn)
        
        self.layout.addWidget(self.container, alignment=Qt.AlignCenter)
        self.layout.addWidget(btn_container, alignment=Qt.AlignCenter)

class SessionTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Session Tracker')
        self.resize(500, 500)

        self.main_layout = QVBoxLayout(self)

        # Scrolling
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        
        self.scroll_content = QWidget()
        self.groups_layout = QVBoxLayout(self.scroll_content)
        self.groups_layout.setAlignment(Qt.AlignTop)
        
        # Test Groups
#        groups_data = [
#            ("GROUP #A", ["Minecraft", "GTA 6", "Roblox", "PAYDAY 2"]),
#            ("GROUP #B", ["Fortnite", "Valorant", "Apex Legends"]),
#            ("GROUP #C", ["Cyberpunk 2077", "The Witcher 3", "Elden Ring"]),
#            ("GROUP #D", ["League of Legends", "Dota 2", "Smite"])
#        ]
        
#        for name, items in groups_data:
#            self.add_group(name, items)

        self.scroll.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll)

        # Timer
        timer_container = QFrame()
        timer_container.setMinimumHeight(120)
        timer_container.setStyleSheet("border: 2px solid black; border-radius: 8px;")
        timer_layout = QVBoxLayout(timer_container)

        self.timer_label = QLabel("00:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 36px; font-weight: bold; border: none;")

        control_btns_layout = QHBoxLayout()
        control_btns_layout.setSpacing(5)
        control_btns_layout.addStretch()

        for i in range(5):
            btn = QPushButton()
            btn.setFixedSize(32, 32)
            btn.setStyleSheet("border: 1.5px solid black; border-radius: 6px; background: #f0f0f0;")
            btn.clicked.connect(lambda checked, b=i: self.banner_btn(b))
            control_btns_layout.addWidget(btn)

        control_btns_layout.addStretch()

        timer_layout.addWidget(self.timer_label)
        timer_layout.addLayout(control_btns_layout)
        self.main_layout.addWidget(timer_container)

        # Current Session
        self.session_label = QLabel("CURRENT SESSION: None")
        self.session_label.setAlignment(Qt.AlignCenter)
        self.session_label.setStyleSheet("font-size: 20px; padding: 20px;")
        self.main_layout.addWidget(self.session_label)

    def add_group(self, name, items):
        new_group = GroupWidget(name, items, self.group_btn)
        self.groups_layout.addWidget(new_group)

    def group_btn(self, group_name, btn_key):
        print(f"Group: {group_name} | Button: {btn_key}")

        if btn_key == "add":
            add_dialog = AddItemDialog(self, group_name)
            add_dialog.exec_()

    def banner_btn(self, index):
        print(f"Control Button: {index}")

        self.add_group("Group A", ["Minecraft", "GTA 6", "Roblox", "PAYDAY 2"])