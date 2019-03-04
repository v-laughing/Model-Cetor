# -*- coding:utf-8 -*-
# __author__ = 'Shanks'

# this file is a entrance for running the editor
import sys
from PyQt5.QtWidgets import *
import editorWindow
from dialogbox import SpaceDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #dialog = SpaceDialog()
    dpath = 'D:\Project\python\Real\editor\\text.c'
    #if dialog.exec_():
     #   dpath = dialog.dir_path()
    if dpath:
        window = editorWindow.EditorWindow(dpath)
        window.show()

    app.exec_()
