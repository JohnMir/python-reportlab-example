import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget, QBoxLayout, QFormLayout, QGroupBox,
)

debug_background=True

styles = {
    'files': "QLabel {color: 'white';background: '#3A3B41';} QGroupBox {color: 'white';}",
    'dropzone': "QLabel {color: 'white';background: '#3A3B41';margin-top: '50px';}",
    'main': "QMainWindow {background: '#3A3B41';}",
    'generate': "",
}



# Subclass QMainWindow to customize your application's main window
# pixmap = QPixmap('image.png')
# label.setPixmap(pixmap)
class MainWindow(QMainWindow):

    # Take a string
    # Add a QLabel with the string as text to the vbox
    def addPhotoElement(self, filename):
        label = QLabel(filename)
        label.setStyleSheet(styles['files'])
        label.setFixedWidth(500)
        self.filebox.addWidget(label)

    # Add a QPushButton and QLabel to self.filebox
    # When the button is clicked, the label should be removed from the box
    def addRemoveButton(self, filename):
        label = QLabel(filename)
        label.setStyleSheet(styles['files'])
        label.setFixedWidth(200)
        button = QPushButton("Remove")
        button.setFixedWidth(60)
        button.clicked.connect(lambda: self.removePhotoElement(label))
        self.filebox.addWidget(button)
        self.filebox.addWidget(label)

        # Remove the given widget from self.filebox

    def removePhotoElement(self, widget):
        self.filebox.removeWidget(widget)
        widget.deleteLater()
        widget = None

    def __init__(self):
        super().__init__()

        self.filelist = []

        self.setWindowTitle("Portfoliolio")
        self.setAcceptDrops(True)
        self.setGeometry(0, 0, 400, 500)
        self.setStyleSheet(styles['main'])

        dropzone = QLabel('Drop here')
        dropzone.setStyleSheet(styles['dropzone'])
        dropzone.setAlignment(QtCore.Qt.AlignCenter)
        dropzone.setFixedWidth(120)
        dropzone.setFixedHeight(80)

        files = QGroupBox("Photos")
        files.setStyleSheet(styles['files'])
        vbox = QVBoxLayout()
        files.setLayout(vbox)
        self.filebox = vbox
        # vbox.addWidget(radiobutton)

        filelabel = QLabel(f'Photos ({len(self.filelist)})')
        self.filelabel = filelabel
        filelabel.setStyleSheet(styles['files'])
        filelabel.setFixedWidth(500)

        layout = QFormLayout()

        vbox.addWidget(filelabel)

        instantiated_widgets = [files, dropzone]

        widgets = [
            QCheckBox,
            QComboBox,
            QDateEdit,
            QDateTimeEdit,
            QDial,
            QDoubleSpinBox,
            QFontComboBox,
            QLCDNumber,
            QLabel,
            QLineEdit,
            QProgressBar,
            QPushButton,
            QRadioButton,
            QSlider,
            QSpinBox,
            QTimeEdit,
        ]

        for w in instantiated_widgets:
            layout.addWidget(w)

        # for w in widgets:
        #     layout.addWidget(w())

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    # def addPhotoElement(self):


    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print(f)
            # self.filelist.append(f)
            self.addRemoveButton(f)

        self.filelabel.setText(f'Photos ({len(self.filelist)})\n------\n' + "\n".join(self.filelist))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
