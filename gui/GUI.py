# -*- coding: utf-8 -*-


from PyQt4 import QtCore, QtGui, uic

qtCreatorFile = "gui.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # custom stuff ini
        self.closeBtnINFO.clicked.connect(self.close_application)
        self.runBtnFS.clicked.connect(self.sum_)
        self.closeMenu.triggered.connect(self.close_application)
        self.contactMenu.triggered.connect(self.contact_tag)

    def close_application(self):
        '''
        function to be called by button closeBtnINFO
        '''
        choice = QtGui.QMessageBox.question(self, 'Close', 'You are \
        closing the application. Are you sure?',
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        # ask what to do if choices are made
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def sum_(self):
        '''
        function that sums up var1 and var2 spinbutton
        and puts it into totalbox
        '''
        var1 = (self.var1.value())
        var2 = (self.var2.value())
        result = (str(round((var1 + var2), 3))).replace('.', ',')
        self.totalbox.setText(result)

    def contact_tag(self):
        '''
        Function that opens the contact window
        '''
        text = u'''
        If you got problems, google it ffs
        '''
        QtGui.QMessageBox.about(self, 'Contact', text)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
