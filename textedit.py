# -*- coding:utf-8 -*-
# _author__ = 'Shanks'

# this file include a class, which construct a text edit widget using a file path
# when file path is none, it construct a new text edit widget
from PyQt5 import Qt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTextEdit, QMessageBox, QFileDialog


class TextEdit(QTextEdit):

    def __init__(self, file_path, parent=None):
        super(TextEdit, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.file_path = file_path
        self.file_name = QFileInfo(self.file_path).fileName()

        self.document().setModified(False)

    def save(self):
        exception = None
        file = None
        try:
            file = QFile(self.file_path)
            if not file.open(QIODevice.WriteOnly):
                raise IOError(file.errorString())
            steams = QTextStream(file)
            steams.setCodec('utf-8')
            steams << self.toPlainText()
            self.document().setModified(False)
        except EnvironmentError as e:
            exception = e
        finally:
            if file is not None:
                file.close()
            if exception is not None:
                raise exception

    def is_modified(self):
        return self.document().isModified()

    def load(self):

        exception = None
        file = None
        try:
            file = QFile(self.file_path)
            if not file.open(QIODevice.ReadOnly):
                raise IOError(file.errorString())
            steams = QTextStream(file)
            steams.setCodec('utf-8')
            self.setPlainText(steams.readAll())
            self.document().setModified(False)
        except EnvironmentError as e:
            exception = e
        finally:
            if file is not None:
                file.close()
            if exception is not None:
                raise exception















