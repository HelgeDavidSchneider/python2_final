#imports
import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from html.parser import HTMLParser
import webbrowser as wb
import subprocess as sp
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from numpy import arange, sin, pi

#imports for subproject files
from projects.focal_stats import *
from projects.routeplanner import *
from projects.plot import plotter

#insert gui.ui file
qtCreatorFile = "gui.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        def compute_initial_figure(self):
            pass

class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        pass

class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        #self.pb_reset.clicked.connect(initial_figure)
        #self.pb_route.clicked.connect(update_figure)

    def initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # main init
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        l = QtWidgets.QVBoxLayout(self.widget_plotting)
        sc = MyStaticMplCanvas(self.widget_plotting)#, width=5, height=4, dpi=100)
        dc = MyDynamicMplCanvas(self.widget_plotting, width=5, height=4, dpi=100)
        l.addWidget(sc)
        l.addWidget(dc)


        # buttons within tab widgets
        self.info_close.clicked.connect(self.close_app)

        # buttons in focal statistics tab
        self.fs_run.clicked.connect(self.fs_run_filter)
        self.fs_browse.clicked.connect(self.file_browser)
        self.fs_file_path = None

        #buttons in route planner
        self.pb_route.clicked.connect(self.route_plot)

        #buttons in plotting tab
        self.plot_plot.clicked.connect(self.plot_app)

        #buttons in ct manager tab
        self.ctm_browse.clicked.connect(self.directory_browser)
        self.ctm_dir = None

        # menu buttons
            # file submenu
        self.menu_close.triggered.connect(self.close_app)
        self.menu_ipython.triggered.connect(self.ipython_app)
        self.menu_browser.triggered.connect(self.browser_app)
            # help submenu
        self.menu_docu.triggered.connect(self.docu_app)
        self.menu_contact.triggered.connect(self.contact_app)
        self.menu_about.triggered.connect(self.about_app)
            # toolbar submenu
        self.menu_info.triggered.connect(self.info_tab)
        self.menu_fs.triggered.connect(self.fs_tab)
        self.menu_ctm.triggered.connect(self.ctm_tab)
        self.menu_route.triggered.connect(self.route_tab)
        self.menu_plotting.triggered.connect(self.plotting_tab)

    def plot_app(self):
        '''
        calls plotter in plot.py
        '''

        a1 = self.plot_a1.value()
        a2 = self.plot_a2.value()
        n1 = self.plot_n1.value()
        n2 = self.plot_n2.value()

        plotter(a1,n1)
        plotter(a2,n2)

        fig.canvas.draw()

        mplwidget.show()

    #tab switch functions
    def info_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def fs_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def ctm_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def route_tab(self):
        self.tabWidget.setCurrentIndex(3)

    def plotting_tab(self):
        self.tabWidget.setCurrentIndex(4)

    def ipython_app(self):
        '''
        opens a new ipython/jupyter window as new tab
        in standard browser
        '''
        sp.call("ipython notebook")

    def browser_app(self):
        '''
        opens a new Uni Freiburg tab in standard browser
        '''
        wb.open_new('https://www.unr.uni-freiburg.de/')

    def contact_app(self):
        '''
        opens a message box with contact details
        '''
        html = HTMLParser()
        text = html.unescape('If you have any questions or problems, please contact us:<br>'
                             '<ul>'
                             '<li>Anna Tenberg <a href="mailto:tenberg.a@posteo.de">tenberg.a@posteo.de</a></li>'
                             '<li>Lukas Müller <a href="mailto:luggie@gmx.net">luggie@gmx.net</a></li>'
                             '<li>Helge Schneider <a href="mailto:info.helgeschneider@gmail.com">info.helgeschneider@gmail.com</a></li>'
                             '<li>Rafael. <a href="mailto:rafaelbr90@gmail.com">rafaelbr90@gmail.com</a></li>'
                             '</ul>')

        QtWidgets.QMessageBox.about(self, 'Contact', text)

    def docu_app(self):
        '''
        opens a new message box with information
        '''
        text = u"""
                See Info Tab for documentation
                """
        QtWidgets.QMessageBox.about(self, 'Documentation', text)

    def close_app(self):
        '''
        close application for the programm. called by close button and file->close
        '''
        choise = QtWidgets.QMessageBox.question(self,
                                                "Close",
                                                'You are closing the application. Are you sure?',
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choise == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def about_app(self):
        '''
        opens message box about the program
        '''
        html = HTMLParser()
        text = html.unescape('This App was programmed by:<br>'
                             '<ul>'
                             '<li>Anna Tenberg <a href="mailto:tenberg.a@posteo.de">tenberg.a@posteo.de</a></li>'
                             '<li>Lukas Müller <a href="mailto:luggie@gmx.net">luggie@gmx.net</a></li>'
                             '<li>Helge Schneider <a href="mailto:info.helgeschneider@gmail.com">info.helgeschneider@gmail.com</a></li>'
                             '<li>Rafael <a href="mailto:rafaelbr90@gmail.com">rafaelbr90@gmail.com</a></li>'
                             '</ul>'
                             'as part of Python II course at Albert-Ludwigs-Universität Freiburg'
                             '<br>'
                             'held by:'
                             '<ul>'
                             '<li>Mirko Mälicke <a href="mailto:mirko.maelicke@felis.uni-freiburg.de">mirko.maelicke@felis.uni-freiburg.de</a></li>'
                             '<li>Joao Paulo Pereira <a href="mailto:"joao.pereira@felis.uni-freiburg.de">joao.pereira@felis.uni-freiburg.de</a></li>'
                             '</ul>')


        QtWidgets.QMessageBox.about(self, 'About', text)

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
    def directory_browser(self):
        '''
        :returns: chosen folder as path string
        '''
        self.ctm_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

    def route_plot(self):
        start_value = self.sb_start.value()
        finish_value = self.sb_finish.value()
        distance_value = self.sb_dis.currentText()
        seed_value = self.sb_seed.value()

        output = routeplanner(start_value, finish_value, distance_value, seed_value)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.setWindowTitle("Incredible App")
    window.show()
    sys.exit(app.exec_())