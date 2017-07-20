#imports
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QFileDialog

from projects.focal_stats import *

#insert gui.ui file
qtCreatorFile = "gui.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # main init
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # buttons within tab widgets
        self.info_close.clicked.connect(self.close_app)

        # buttons in focal statistics tab
        self.fs_run.clicked.connect(self.fs_run_filter)
        self.fs_browse.clicked.connect(self.file_browser)
        self.fs_file_path = None


        """
        # menu buttons
            # file submenu
        self.menu_close.triggered.connect(self.close_app)
        self.menu_ipython.triggered.connect(self.ipython_app)
        self.menu_browser.triggered.connect(self.browser_app)
            # help submenu
        self.menu_docu.triggered.connect(self.docu_app)
        self.menu_browser.triggered.connect(self.contact_app)
        self.menu_about.triggered.connect(self.about_app)
            # toolbar submenu
        self.menu_info.triggered.connect(self.info_app)
        self.menu_fs.triggered.connect(self.fs_app)
        self.menu_ctm.triggered.connect(self.ctm_app)
        self.menu_route.triggered.connect(self.route_app)
        self.menu_plotting.triggered.connect(self.plotting_app)
        """

    def contact_app(self):
        text = u"""
        #If you have any questions or problems, please contact:\n
        #             python_course@uni-freiburg.de
        """
        QtWidgets.QMessageBox.about(self, 'Contact', text)


    def close_app(self):
        choise = QtWidgets.QMessageBox.question(self,
                                                "Close",
                                                'You are closing the application. Are you sure?',
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choise == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def fs_run_filter(self):
        '''
        function within focal Statistic tab
        calls filter_main from focal_stats.py
        with set parameters.
        :returns pop-up with original and filtered image
        '''
        #var def
        filter_type = self.fs_filter_type.currentText()
        function_type = self.fs_function_type.currentText()
        squarelength = None
        shape = None
        radius = None
        angle = None

        #swtich through filter types
        if filter_type.lower() == 'square':
            squarelength = self.fs_squarelength.value()
        elif filter_type.lower() == 'rectangular':
            shape = (self.fs_shape_1.value(), self.fs_shape_2.value())
        elif filter_type.lower() == 'circle':
            radius = self.fs_radius.value()
        elif filter_type.lower() == 'wedge':
            angle = (self.fs_radius.value(), self.fs_shape_1.value(), self.fs_shape_2.value())

        #format
        function_type=function_type.replace("Standard Deviation", "std").replace("Maximum", "max").replace("Minimum", "min").lower()
        img_path = (str(self.fs_file_path))

        #filter function call
        filter_main(img_path = img_path, filtertype=filter_type.lower(), functiontype=function_type, squarelength=squarelength, shape=shape, radius=radius,
                    angles=angle)

    def file_browser(self):
        '''
        General Filebrowse function
        :returns: chosen file's directory
        '''
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fs_file_path, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All files(*)", options=options)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())



