from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.itemcount = 0
        self.files = []

        # set the title
        self.setWindowTitle("Label")
        self.setAcceptDrops(True)

        # setting the geometry of window
        self.setGeometry(0, 0, 400, 300)

        # creating a label widget
        # by default label will display at top left corner
        self.label = QLabel('This is label', self)
        self.label.setFixedWidth(500)
        # self.labels.append(label)

        self.button = QPushButton('PyQt5 button', self)
        self.button.setToolTip('This is an example button')
        self.button.move(100, 70)
        self.button.clicked.connect(self.on_click)

        # show all the widgets
        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print(f)
            self.files.append(f)

        self.label.setText("\n".join(self.files))


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())
