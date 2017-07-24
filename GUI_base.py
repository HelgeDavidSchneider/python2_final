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
from scipy.spatial import Delaunay
from scipy.spatial.distance import pdist, squareform
from scipy.sparse.csgraph import dijkstra

#imports for subproject files
from projects.focal_stats import *
#from projects.routeplanner import *
from projects.plot import plotter

#insert gui.ui file
qtCreatorFile = "gui.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # main init
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #plot in route_planner
        self.qlayout = QtWidgets.QHBoxLayout(self.widget_route)
        self.widget_route.setLayout(self.qlayout)
        self.qfigWidget = QtWidgets.QWidget(self.widget_route)
        fig = Figure((4.0, 4.0), dpi=100)
        canvas = FigureCanvas(fig)
        canvas.setParent(self.qfigWidget)

        np.random.seed(42)
        nodes = np.random.gamma(10, 2, size=(20, 2))
        delaunay = Delaunay(nodes)
        segments = list()

        for simp in delaunay.simplices:
            segments.extend(
                [(simp[0], simp[1]), (simp[0], simp[2]), (simp[1], simp[2])])

        edges = list(set(segments))

        axes = fig.add_subplot(111)
        for edge in edges:
            axes.plot(nodes[edge,][:, 0], nodes[edge,][:, 1], linestyle='-',
                      color='gray')

        axes.plot(nodes[:, 0], nodes[:, 1], linestyle='', marker='o',
                  color='k')

        for i, node in enumerate(nodes):
            axes.text(node[0], node[1] * 1.01, '%d' % i, color='k')

        self.qlayout.addWidget(self.qfigWidget)
        self.widget_route.show()


        # plot in plotting
        qlayout2 = QtWidgets.QHBoxLayout(self.widget_plotting)
        self.widget_plotting.setLayout(qlayout2)
        qfigWidget2 = QtWidgets.QWidget(self.widget_plotting)
        fig2 = Figure((4.0, 4.0), dpi=100)
        canvas2 = FigureCanvas(fig2)
        canvas2.setParent(qfigWidget2)

        axes2 = fig2.add_subplot(111)
        x = np.arange(0.0, 5.0, 0.01)
        func1 = 1 * np.sin(x) ** 1
        func2 = 2* np.sin(x) ** 2

        axes2.plot(x, func1)
        axes2.plot(x, func2)

        plt.grid(True)
        qlayout2.addWidget(qfigWidget2)
        self.widget_plotting.show()


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
        distance_value = self.cb_dis.currentText()

        self.routeplanner(start_value, finish_value, distance_value)

        #self.qlayout.addWidget(self.qfigWidget)

        #self.widget_route.show()

    def route_map(self):

        np.random.seed(42)
        nodes = np.random.gamma(10, 2, size=(20, 2))
        delaunay = Delaunay(nodes)
        segments = list()

        for simp in delaunay.simplices:
            segments.extend(
                [(simp[0], simp[1]), (simp[0], simp[2]), (simp[1], simp[2])])

        edges = list(set(segments))

        axes = fig.add_subplot(111)
        for edge in edges:
            axes.plot(nodes[edge,][:, 0], nodes[edge,][:, 1], linestyle='-',
                      color='gray')

        axes.plot(nodes[:, 0], nodes[:, 1], linestyle='', marker='o',
                  color='k')

        for i, node in enumerate(nodes):
            axes.text(node[0], node[1] * 1.01, '%d' % i, color='k')

        return self.widget_route.show()

    def routeplanner(self, start, finish, distance):
        if start not in range(20) or finish not in range(20) \
                or distance not in ['eucledian', 'manhatten']:
            raise ValueError('Wrong Input. '
                             '\nstart and finish have to be int between 0 and 19. '
                             '\ndistance can only be eucledian or manhatten.')

        np.random.seed(42)
        nodes = np.random.gamma(10, 2, size=(20, 2))
        delaunay = Delaunay(nodes)
        segments = list()

        for simp in delaunay.simplices:
            segments.extend(
                [(simp[0], simp[1]), (simp[0], simp[2]), (simp[1], simp[2])])

        edges = list(set(segments))

        if distance == 'eucledian':
            dis = squareform(pdist(nodes, metric='euclidean'))  # pythagoras
        elif distance == 'manhatten':
            dis = squareform(pdist(nodes, metric='cityblock'))  # 90°

        ## creating the weight matrix

        cs = np.zeros(dis.shape)
        # each segment defines the indices of the edges
        for seg in segments:
            cs[seg] = dis[seg]
            cs[seg[::-1]] = dis[seg]
        cs[cs == 0.0] = np.NaN

        weights, pre = dijkstra(cs, return_predecessors=True)

        path = [finish]

        while True:
            next_segment = pre[start, path[-1]]
            if next_segment == -9999:
                # no connection: break
                break
            elif next_segment == start:
                # finished: break
                break
            else:
                # new segment, add to path
                path.append(next_segment)
        path.append(start)
        reversed(path)

        title = 'Path %s to %s: ' % (start, finish), ' - '.join(
            ['%d' % _ for _ in reversed(path)])

        figr = Figure((4.0, 4.0), dpi=100)
        canvasr = FigureCanvas(figr)
        canvasr.setParent(self.qfigWidget)

        # plot
        axesr = figr.add_subplot(111)

        # plot the vertices
        axesr.plot(nodes[:, 0], nodes[:, 1], linestyle='', marker='o',
                  color='gray')

        for i, node in enumerate(nodes):
            axesr.text(node[0], node[1] * 1.01, '%d' % i, color='gray')

        # plot the edges
        for edge in edges:
            axesr.plot(nodes[edge,][:, 0], nodes[edge,][:, 1], linestyle='-',
                      color='k')

        # plot the path
        for i in range(1, len(path)):
            axesr.plot(nodes[(path[i - 1], path[i]),][:, 0],
                      nodes[(path[i - 1], path[i]),][:, 1], '-g', lw=2)

        # plot start and end point
        axesr.plot(nodes[path[0]][0], nodes[path[0]][1], 'or', markersize=9)
        axesr.plot(nodes[path[-1]][0], nodes[path[-1]][1], 'og', markersize=9)

        #plt.suptitle(title[0] + title[1])

        self.qlayout.addWidget(self.qfigWidget)

        return self.widget_route.show()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.setWindowTitle("Incredible App")
    window.show()
    sys.exit(app.exec_())