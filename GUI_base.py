#imports
import sys
from PyQt5 import uic, QtWidgets

#insert gui.ui file
qtCreatorFile = "gui.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        #main init
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #buttons within tab widgets
        self.info_close.clicked.connect(self.close_app)
        self.fs_run.clicked.connect(self.sum_)

        #menu buttons
            #file submenu
        self.menu_close.triggered.connect(self.close_app)
        self.menu_ipython.triggered.connect(self.ipython_app)
        self.menu_browser.triggered.connect(self.browser_app)
            #help submenu
        self.menu_docu.triggered.connect(self.docu_app)
        self.menu_browser.triggered.connect(self.contact_app)
        self.menu_about.triggered.connect(self.about_app)
            #toolbar submenu
        self.menu_info.triggered.connect(self.info_app)
        self.menu_fs.triggered.connect(self.fs_app)
        self.menu_ctm.triggered.connect(self.ctm_app)
        self.menu_route.triggered.connect(self.route_app)
        self.menu_plotting.triggered.connect(self.plotting_app)



    def contact_app(self):
        text = u"""
       If you have any questions or problems, please contact:\n
                    python_course@uni-freiburg.de
        """
        QtWidgets.QMessageBox.about(self, 'Contact', text)

    def sum_(self):
        var1 = (self.varOne.value())
        var2 = (self.varTwo.value())
        result = (str(round((var1 + var2), 3))).replace('.', ',')
        self.totalBox.setText(result)

    def close_app(self):
        choise = QtWidgets.QMessageBox.question(self,
                                                "Close",
                                                'You are closing the application. Are you sure?',
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choise == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())