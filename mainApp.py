from PyQt5 import QtCore, QtGui, QtWidgets
import vtkplotlib as vpl
from stl.mesh import Mesh

class appUi(object):
    # def __init__(self):
    #     super().__init__()

    def setupUi(self, MainWindow, path):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(479, 412)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(100, 100))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(16777214, 16777214))
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(3710, 3850, 351, 211))
        self.groupBox.setObjectName("groupBox")
        self.figure = vpl.QtFigure()
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked= lambda : self.getFile())
        self.pushButton.setGeometry(QtCore.QRect(210, 180, 89, 25))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.path = path
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def getFile(self):
        self.figure = vpl.QtFigure(parent= self.centralwidget )
        mesh = Mesh.from_file(self.path) #"Resources/models/Test.stl")

        mesh = vpl.mesh_plot(mesh)
        vpl.reset_camera(self.figure)
        self.figure.update()
        self.figure.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiApp()
    ui.setupUi(MainWindow,"Resources/models/Test.stl")
    MainWindow.show()
    sys.exit(app.exec_())
