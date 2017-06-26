import sys
from PyQt5.QtWidgets import QApplication, QWidget

class MyForm(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.helloworld)

    def helloworld(self):
        self.ui.textEdit.setText(“Hello world”)
        print (‘Hello world again’)

if __name__ == “__main__”:
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())