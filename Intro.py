import sys
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer

from SlicerWindow import SlicerWindow


class test(QMainWindow):
    def __init__(self, ):
        super(test, self).__init__()
        self.mainWindow = None
        win = self.frameGeometry()
        self.setFixedSize(800, 500)
        center_coordinates = QDesktopWidget().availableGeometry().center()
        win.moveCenter(center_coordinates)
        self.move(win.topLeft())
        self.set_background_image("Resources/Images/NOVA.png")
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.step2)
        self.timer.start(30)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.show()

    def step2(self):
        self.set_background_image("Resources/Images/NOVA1.png")
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.step3)
        self.timer.start(50)
        self.setWindowFlag(Qt.FramelessWindowHint)

    def step3(self):
        self.set_background_image("Resources/Images/NOVA2.png")
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.main)
        self.timer.start(30)

    def main(self):
        self.close()
        self.mainWindow = SlicerWindow()
        self.mainWindow.showMaximized()
    def set_background_image(self, image_path):

        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        brush = QBrush(pixmap)
        palette = self.palette()
        palette.setBrush(QPalette.Background, brush)
        self.setPalette(palette)


app = QApplication(sys.argv)
window = test()
sys.exit(app.exec())
