# -*- coding:utf-8 -*-
# __author__ = 'Shanks'
import re



'''0
class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)









        #file = QDir()
        #file.mkpath(r'D:\Project\python\Real\editor\text.c\hello2')
        #file.open(QIODevice.WriteOnly)
        #file.close()

    #    self.text.c(2)
        #self.setWindowTitle('IDE')
        self.resize(600, 600)

        #file_tree = tree.FileTreeWidget(r'D:\Project\python\Real\editor\text.c')
        #self.setCentralWidget(file_tree)
        #print(file_tree.selectedItem().text.c(0))

        #text.c = textedit.TextEdit()
        #self.setCentralWidget(text.c)


    def text.c(self, a):
        a = a + 1
        print(a)



app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()
'''





class Token(object):
    def __init__(self, row, value):
        self.row = row
        self.value = value



def is_digit_const(word):
    if re.match('\d+\.?\d+', word):
        return True
    return False




# 表达式-->TODO
i=0
while i<10:

    i +=1
else:
    print('hhh')




















