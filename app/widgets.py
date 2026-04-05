from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QPushButton, QScrollArea)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from constants import *
from dialogs import *
from helpers import *

import random

class GroupWidget(QWidget):
    def __init__(self, group_name, items, active, callback):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.items = items
        self.active = active
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
        btn_layout.setSpacing(1)

        btn_container = QWidget()
        btn_container.setFixedWidth(150)
        btn_layout_inner = QHBoxLayout(btn_container)
        btn_layout_inner.setContentsMargins(5, 0, 5, 0)
        
        for k, v in GROUP_BUTTONS.items():
            btn = QPushButton()
            btn.setIcon(QIcon(v['icon']))
            btn.setObjectName(k)
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

        self.active_btn = QPushButton()
        self.active_btn.setObjectName("active")
        self.active_btn.setFixedSize(32, 32)
        self.active_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #777; 
                border-radius: 6px; 
                background-color: #fcfcfc;
            }
        """)

        if active:
            self.active_btn.setIcon(QIcon("app/icons/tick.png"))
        else:
            self.active_btn.setIcon(QIcon("app/icons/cross.png"))

        self.active_btn.clicked.connect(lambda checked, gn=group_name, bi="active": callback(gn, bi))
        btn_layout_inner.addWidget(self.active_btn)

        self.layout.addWidget(self.container, alignment=Qt.AlignCenter)
        self.layout.addWidget(btn_container, alignment=Qt.AlignCenter)

    def change_active(self):
        self.active = not self.active

        if self.active:
            self.active_btn.setIcon(QIcon("app/icons/tick.png"))
        else:
            self.active_btn.setIcon(QIcon("app/icons/cross.png"))

        return self.active

class SessionTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.current_groups = {}
        self.group_widgets = {}

        self.saved_sessions = load_session_data()
        print(self.saved_sessions)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.current_session = {}

        #self.time_left = 0
        #self.session_duration = 0

        self.session_active = False
        self.session_paused = False

        #self.selected_group = None
        #self.selected_item = None

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

        self.load_groups()

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

        for k, v in BANNER_BUTTONS.items():
            btn = QPushButton()
            btn.setIcon(QIcon(v['icon']))
            btn.setToolTip(v['tooltip'])
            btn.setFixedSize(32, 32)
            btn.setStyleSheet("border: 1.5px solid black; border-radius: 6px; background: #f0f0f0;")
            btn.clicked.connect(lambda checked, b=k: self.banner_btn(b))
            control_btns_layout.addWidget(btn)

        self.pause_btn = QPushButton()
        self.pause_btn.setIcon(QIcon("app/icons/pause.png"))
        self.pause_btn.setToolTip("Pause Session")
        self.pause_btn.setFixedSize(32, 32)
        self.pause_btn.setStyleSheet("border: 1.5px solid black; border-radius: 6px; background: #f0f0f0;")
        self.pause_btn.clicked.connect(lambda checked, b="toggle_pause": self.banner_btn(b))
        control_btns_layout.addWidget(self.pause_btn)

        control_btns_layout.addStretch()

        timer_layout.addWidget(self.timer_label)
        timer_layout.addLayout(control_btns_layout)
        self.main_layout.addWidget(timer_container)

        # Current Session
        self.session_label = QLabel("No Session Active")
        self.session_label.setAlignment(Qt.AlignCenter)
        self.session_label.setStyleSheet("font-size: 20px; padding: 20px;")
        self.main_layout.addWidget(self.session_label)

    def load_groups(self):
        saved_groups = load_data()

        for name, data in saved_groups.items():
            self.add_group(name, data['items'], data['active'], False)

    def add_group(self, name, items, active, save):
        new_group = GroupWidget(name, items, active, self.group_btn)
        self.groups_layout.addWidget(new_group)
        self.current_groups[name] = {
            "items": items,
            "active": active
        }
        self.group_widgets[name] = new_group

        if save: save_data(self.current_groups)

    def add_item(self, group_name, item):
        group_data = self.current_groups[group_name]
        group_widget = self.group_widgets[group_name]

        group_data['items'].append(item)
        group_widget.items_label.setText("\n".join(group_data['items']))

        save_data(self.current_groups)

    def remove_items(self, group_name, items_to_remove):
        group_data = self.current_groups[group_name]
        group_widget = self.group_widgets[group_name]
        
        new_items = [item for item in group_data['items'] if item not in items_to_remove]
        group_data['items'] = new_items
        
        group_widget.items_label.setText("\n".join(group_data['items']))

        save_data(self.current_groups)

    def delete_group(self, group_name):
        widget = self.group_widgets[group_name]

        self.groups_layout.removeWidget(widget)
            
        widget.setParent(None)
        widget.deleteLater()

        self.current_groups.pop(group_name, None)
        self.group_widgets.pop(group_name, None)

        save_data(self.current_groups)

    def start_session(self):
        if self.session_active:
            print("session already active")
            return

        success, message, valid_groups = get_valid_groups(self.current_groups)
        print(message)
        if success:    
            dialog = StartSessionDialog(self)

            if dialog.exec_():
                chosen_group = random.choice(list(valid_groups.keys()))
                chosen_item = random.choice(valid_groups[chosen_group]['items'])

                total_duration, name = dialog.get_details()

                self.current_session = {
                    "name": name,
                    "duration": total_duration * 60,
                    "remaining": total_duration * 60,
                    "group": chosen_group,
                    "item": chosen_item,
                    "notes": "",
                }
                print(self.current_session)
                self.session_active = True
                self.session_paused = False

                self.session_label.setText(f"Session Active: (Group - {self.current_session['group']}) {self.current_session['item']}")

                self.update_timer()

                self.timer.start(1000)

    def update_timer(self):
        if self.current_session['remaining'] > 0:
            self.current_session['remaining'] -= 1
            self.update_timer_label()
        else:
            self.end_session(False)

    def update_timer_label(self):
        minutes = int(self.current_session['remaining'] // 60)
        seconds = int(self.current_session['remaining'] % 60)
        self.timer_label.setText(f"{minutes:02}:{seconds:02}")

    def resume_session(self):
        self.timer.start(1000)
        self.session_paused = False
        self.session_label.setText(f"Session Active: (Group - {self.current_session['group']}) {self.current_session['item']}")

    def pause_session(self):
        self.timer.stop()
        self.session_paused = True
        self.session_label.setText("Session Paused")

    def end_session(self, start_next):
        if not self.session_active:
            print("no session active")
            return
        
        self.timer.stop()
        self.session_active = False
        self.session_paused = False
        self.timer_label.setText("00:00")
        self.session_label.setText(f"Session Complete: {self.current_session['item']}")

        dialog = SessionEnded(self, f"Completed session")

        if dialog.exec_():
            save_session_data(self.current_session)
            self.current_session = {}
            
            if start_next:
                self.start_session()

    def restart_session(self):
        if not self.session_active:
            print("No session active")
            return
        
        dialog = RestartSessionDialog(self)
        self.pause_session()

        if dialog.exec_():
            option = dialog.get_option()
            self.resume_session()

            if option == "hard_reset":
                self.end_session(True)
            elif option == "soft_reset":
                self.timer.stop()

                self.current_session['remaining'] = self.current_session['duration']
                self.update_timer()

                self.timer.start(1000)

    def toggle_pause(self):
        if not self.session_active:
            print("No session active")
            return
        
        if self.session_paused:
            self.resume_session()
        else:
            self.pause_session()

    def group_btn(self, group_name, btn_key):
        group_data = self.current_groups[group_name]
        group_widget = self.group_widgets[group_name]

        if btn_key == "add":
            add_dialog = AddItemDialog(self, group_name)

            if add_dialog.exec_():
                self.add_item(group_name, add_dialog.get_item())

        elif btn_key == "remove":
            remove_dialog = RemoveItemDialog(self, group_name, group_data['items'])
            
            if remove_dialog.exec_():
                self.remove_items(group_name, remove_dialog.get_checked_items())
        elif btn_key == "delete":
            delete_dialog = DeleteGroupDialog(self, group_name)

            if delete_dialog.exec_():
                self.delete_group(group_name)

        elif btn_key == "active":
            new = group_widget.change_active()
            group_data['active'] = new 

    def banner_btn(self, btn_key):
        if btn_key == "new_group":
            new_dialog = NewGroupDialog(self)

            if new_dialog.exec_():
                self.add_group(new_dialog.get_name(), [], True, True)

        elif btn_key == "start_session":
            self.start_session()
        elif btn_key == "toggle_pause":
            self.toggle_pause()
        elif btn_key == "restart_timer":
            self.restart_session()