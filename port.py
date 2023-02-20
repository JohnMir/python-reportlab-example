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
    QWidget, QFormLayout, QGroupBox, QHBoxLayout,
)

debug_background = True

styles = {
    'files': "QLabel {color: 'white';background: '#3A3B41';} QGroupBox {color: 'white';}",
    'dropzone': "QLabel {color: 'white';background: '#3A3B41';margin-top: '50px';}",
    'main': "QMainWindow {background: '#3A3B41';}",
    'generate': "",
}

debug_all = False
all_widgets = [
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


# Subclass QMainWindow to customize your application's main window
# pixmap = QPixmap('image.png')
# label.setPixmap(pixmap)
class MainWindow(QMainWindow):

    # Update filelabel text with number of buttonlabel_containers in filebox
    # Copilot is a godsend
    def updateFileLabel(self):
        self.filebox.parent().setTitle(f'Photos ({len(self.filebox.children())})')

    # Add a QPushButton and QLabel to self.filebox
    # When the button is clicked, the label should be removed from the box
    def addRemoveButton(self, filename):
        buttonlabel_container = QHBoxLayout()

        label = QLabel(filename)
        label.setStyleSheet(styles['files'])
        label.setFixedWidth(200)

        button = QPushButton("Remove")
        button.setFixedWidth(60)
        button.clicked.connect(lambda: self.removePhotoElement(buttonlabel_container))

        buttonlabel_container.addWidget(button)
        buttonlabel_container.addWidget(label)

        self.filebox.addLayout(buttonlabel_container)
        self.updateFileLabel()

    # TODO add post function annotation to refresh all widgets that have internal logic
    def removePhotoElement(self, widget):
        try:
            self.filebox.removeItem(widget)
            widget.deleteLater()
            widget = None
            self.updateFileLabel()
        except Exception as e:
            print('error removing:', e)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Portfoliolio")
        self.setAcceptDrops(True)
        self.setGeometry(0, 0, 400, 500)
        self.setStyleSheet(styles['main'])

        dropzone = QLabel('Drop here')
        dropzone.setStyleSheet(styles['dropzone'])
        dropzone.setAlignment(QtCore.Qt.AlignCenter)
        dropzone.setFixedWidth(120)
        dropzone.setFixedHeight(80)

        files = QGroupBox("Photos (0)")
        files.setStyleSheet(styles['files'])
        vbox = QVBoxLayout()
        files.setLayout(vbox)
        self.filebox = vbox
        files.setTitle(f'Photos ({len(self.filebox.children())})')

        layout = QFormLayout()

        instantiated_widgets = [files, dropzone]

        for w in instantiated_widgets:
            layout.addWidget(w)

        if (debug_all):
            for w in all_widgets:
                layout.addWidget(w())

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            self.addRemoveButton(f)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
