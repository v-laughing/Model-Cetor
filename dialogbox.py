# -*- coding:utf-8 -*-
# __author__ = 'Shanks'

# this file include a class, which is a file dialog permitting you to choose a workspace
import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


class SpaceDialog(QDialog):
    def __init__(self, parent=None):
        super(SpaceDialog, self).__init__(parent)
        self.setWindowTitle('Work Space')

        self.path_Text = QLineEdit()
        self.browser_button = QPushButton("browser...")
        self.browser_button.clicked.connect(self.dir_browser)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.main_layout()

    def main_layout(self):

        layout = QVBoxLayout()
        layout.addWidget(QLabel("please a work apace"))

        edit_layout = QHBoxLayout()
        edit_layout.addWidget(QLabel("work space:"))
        edit_layout.addWidget(self.path_Text)
        edit_layout.addWidget(self.browser_button)
        layout.addLayout(edit_layout)

        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def dir_browser(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'choose a dir', options=QFileDialog.ShowDirsOnly)
        self.path_Text.setText(dir_path)
        if self.path_Text.text():
            self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)

    def dir_path(self):
        return self.path_Text.text()




class NewFileDialog(QDialog):
    def __init__(self, parent=None):
        super(NewFileDialog, self).__init__(parent)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('entry a file name:'))
        self.edit = QLineEdit()
        layout.addWidget(self.edit)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)
    
    def file_name(self):
        return self.edit.text()


class NewDirDialog(QDialog):
    def __init__(self, parent=None):
        super(NewDirDialog, self).__init__(parent)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('entry a dir name:'))
        self.edit = QLineEdit()
        layout.addWidget(self.edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def dir_name(self):
        return self.edit.text()




