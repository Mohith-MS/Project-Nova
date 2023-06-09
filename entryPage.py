from PyQt5 import QtCore, QtGui, QtWidgets
import sys

import Nova
import Resources.Static.Printers as printers
import main


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(800, 500))
        MainWindow.setMaximumSize(QtCore.QSize(800, 500))
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet("background-color: rgb(85, 87, 83);")
        MainWindow.setAnimated(False)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalFrame = QtWidgets.QFrame(self.centralwidget)
        self.verticalFrame.setGeometry(QtCore.QRect(240, 50, 371, 371))
        self.verticalFrame.setObjectName("verticalFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalFrame)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Title = QtWidgets.QLabel(self.verticalFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Title.sizePolicy().hasHeightForWidth())
        self.Title.setSizePolicy(sizePolicy)
        self.Title.setMaximumSize(QtCore.QSize(16777215, 100))
        self.Title.setSizeIncrement(QtCore.QSize(1, 1))
        self.Title.setStyleSheet("font: 75 33pt \"Ubuntu Condensed\";\n"
                                 "color: rgb(0, 0, 0);\n"
                                 "margin-top: 1ex;")
        self.Title.setScaledContents(True)
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.verticalLayout.addWidget(self.Title, 0, QtCore.Qt.AlignHCenter)
        self.printer = QtWidgets.QLabel(self.verticalFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.printer.sizePolicy().hasHeightForWidth())
        self.printer.setSizePolicy(sizePolicy)
        self.printer.setMinimumSize(QtCore.QSize(50, 50))
        self.printer.setMaximumSize(QtCore.QSize(200, 200))
        self.printer.setStyleSheet("")
        self.printer.setText("")
        self.printer.setPixmap(QtGui.QPixmap("Resources/Images/3dprinter.png"))
        self.printer.setScaledContents(True)
        self.printer.setAlignment(QtCore.Qt.AlignCenter)
        self.printer.setWordWrap(False)
        self.printer.setIndent(-1)
        self.printer.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.printer.setObjectName("printer")
        self.verticalLayout.addWidget(self.printer, 0, QtCore.Qt.AlignHCenter)
        self.listPrinters = QtWidgets.QComboBox(self.verticalFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listPrinters.sizePolicy().hasHeightForWidth())
        self.listPrinters.setSizePolicy(sizePolicy)
        self.listPrinters.setMinimumSize(QtCore.QSize(350, 0))
        self.listPrinters.setAutoFillBackground(False)
        self.listPrinters.setStyleSheet("margin-top: 5ex;\n"
                                        "background-color: rgb(136, 138, 133);")
        self.listPrinters.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.listPrinters.setObjectName("listPrinters")
        self.verticalLayout.addWidget(self.listPrinters, 0, QtCore.Qt.AlignHCenter)
        self.Select = QtWidgets.QPushButton(self.verticalFrame, clicked=lambda: self.click())
        self.Select.setObjectName("Select")
        self.verticalLayout.addWidget(self.Select, 0, QtCore.Qt.AlignHCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.listPrinters.addItems(printers.printers.keys())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.printVol = []

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Title.setText(_translate("MainWindow", "Nova Slicer"))
        self.Select.setText(_translate("MainWindow", "Select"))

    def click(self):
        self.printVol = printers.printers[self.listPrinters.currentText()]
        #print(self.printVol)
        Nova.Nova.selectFile(Nova, printers.printers[self.listPrinters.currentText()])


def display():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
