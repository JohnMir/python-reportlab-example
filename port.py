import sys
from datetime import datetime

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
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
from reportlab.graphics.shapes import Line, Drawing
from reportlab.lib.colors import Color
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import LETTER, inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)

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
        self.files.append(filename)

        buttonlabel_container = QHBoxLayout()

        label = QLabel(filename)
        label.setStyleSheet(styles['files'])
        label.setFixedWidth(200)

        button = QPushButton("Remove")
        button.setFixedWidth(60)
        button.clicked.connect(lambda: self.removePhotoElement(buttonlabel_container, filename))

        buttonlabel_container.addWidget(button)
        buttonlabel_container.addWidget(label)

        self.filebox.addLayout(buttonlabel_container)
        self.updateFileLabel()

    # TODO add post function annotation to refresh all widgets that have internal logic
    def removePhotoElement(self, widget, filename):
        try:
            self.filebox.removeItem(widget)
            widget.deleteLater()
            widget = None
            self.files.remove(filename)
            self.updateFileLabel()
        except Exception as e:
            print('error removing:', e)

    generated_pdfs = {}

    # Add a QHBoxLayout to the centralWidget's layout with a small QPushButton 'Open' that opens the filename and a QLabel of the filename
    def addGeneratedPdf(self, filename):
        layout = self.mainlayout

        buttonlabel_container = QHBoxLayout()

        label = QLabel(filename)
        label.setStyleSheet(styles['files'])
        label.setFixedWidth(200)

        button = QPushButton("Open")
        button.setFixedWidth(60)
        button.clicked.connect(lambda: self.openPdf(filename))

        buttonlabel_container.addWidget(button)
        buttonlabel_container.addWidget(label)

        self.centralWidget().layout().addItem(buttonlabel_container) # Added line for pyqt5 nuance (and I'm not sure if it's correct)
        layout.addChildLayout(buttonlabel_container)  # Refactored line for correct function

    # Open the pdf with the default system application
    @pyqtSlot() # Refactored line
    def openPdf(self, filename):
        print(f'Opening {filename}')
        import os
        os.system(f'open {filename}')

    @pyqtSlot()
    def on_click(self):
        timestamp = datetime.now()
        filename = f'{timestamp.strftime("%Y-%m-%d %H-%M-%S")}.pdf'
        print(f'Portfolio generating... {filename}')
        BasicPortfolio(filename, self.files)
        print(f'Portfolio done! {filename}')
        # Add a dict entry to generated_pdfs with the timestamp in ms as the key and object with the filename and files as fields
        self.generated_pdfs[timestamp] = {
            'filename': filename,
            'files': self.files,
        }
        self.addGeneratedPdf(filename)


    def __init__(self):
        super().__init__()

        self.files = []

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
        self.mainlayout = layout

        generate_button = QPushButton('Generate', self)
        generate_button.setToolTip('Generate a portfolio pdf')
        # generate_button.move(100, 70)
        generate_button.setFixedWidth(60)
        generate_button.setFixedHeight(60)
        generate_button.clicked.connect(self.on_click)

        instantiated_widgets = [files, generate_button]

        for w in instantiated_widgets:
            layout.addWidget(w)

        if debug_all:
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


class FooterCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        self.width, self.height = LETTER

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            if (self._pageNumber > 1):
                self.draw_canvas(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_canvas(self, page_count):
        page = "Page %s of %s" % (self._pageNumber, page_count)
        x = 128
        self.saveState()
        self.setStrokeColorRGB(0, 0, 0)
        self.setLineWidth(0.5)
        self.drawImage("static/lr.png", self.width - inch * 8 - 5, self.height - 50, width=100, height=20,
                       preserveAspectRatio=True)
        self.drawImage("static/ohka.png", self.width - inch * 2, self.height - 50, width=100, height=30,
                       preserveAspectRatio=True, mask='auto')
        self.line(30, 740, LETTER[0] - 50, 740)
        self.line(66, 78, LETTER[0] - 66, 78)
        self.setFont('Times-Roman', 10)
        self.drawString(LETTER[0] - x, 65, page)
        self.restoreState()


class BasicPortfolio:

    def __init__(self, path, photos):
        self.path = path
        self.styleSheet = getSampleStyleSheet()
        self.elements = []

        # colors - Azul turkeza 367AB3
        self.colorOhkaGreen0 = Color((45.0 / 255), (166.0 / 255), (153.0 / 255), 1)
        self.colorOhkaGreen1 = Color((182.0 / 255), (227.0 / 255), (166.0 / 255), 1)
        self.colorOhkaGreen2 = Color((140.0 / 255), (222.0 / 255), (192.0 / 255), 1)
        # self.colorOhkaGreen2 = Color((140.0/255), (222.0/255), (192.0/255), 1)
        self.colorOhkaBlue0 = Color((54.0 / 255), (122.0 / 255), (179.0 / 255), 1)
        self.colorOhkaBlue1 = Color((122.0 / 255), (180.0 / 255), (225.0 / 255), 1)
        self.colorOhkaGreenLineas = Color((50.0 / 255), (140.0 / 255), (140.0 / 255), 1)
        #
        for i in photos:
            self.photopage(i)
            self.nextPagesHeader(True)

        # Build
        self.doc = SimpleDocTemplate(path, pagesize=LETTER)
        self.doc.multiBuild(self.elements, canvasmaker=FooterCanvas)

    def firstPage(self):
        img = Image('static/lr.png', kind='proportional')
        img.drawHeight = 0.5 * inch
        img.drawWidth = 2.4 * inch
        img.hAlign = 'LEFT'
        self.elements.append(img)

        spacer = Spacer(30, 100)
        self.elements.append(spacer)

        img = Image('static/ohka.png')
        img.drawHeight = 2.5 * inch
        img.drawWidth = 5.5 * inch
        self.elements.append(img)

        spacer = Spacer(10, 250)
        self.elements.append(spacer)

        psDetalle = ParagraphStyle('Resumen', fontSize=9, leading=14, justifyBreaks=1, alignment=TA_LEFT,
                                   justifyLastLine=1)
        text = """REPORTE DE SERVICIOS PROFESIONALES<br/>
        Empresa: Nombre del Cliente<br/>
        Fecha de Inicio: 23-Oct-2019<br/>
        Fecha de actualización: 01-Abril-2020<br/>
        """
        paragraphReportSummary = Paragraph(text, psDetalle)
        self.elements.append(paragraphReportSummary)
        self.elements.append(PageBreak())

    def photopage(self, photourl):
        spacer = Spacer(30, 100)
        self.elements.append(spacer)

        img = Image(photourl)
        img.drawHeight = 2.5 * inch
        img.drawWidth = 5.5 * inch
        self.elements.append(img)

        spacer = Spacer(10, 250)
        self.elements.append(spacer)

        psDetalle = ParagraphStyle('Resumen', fontSize=9, leading=14, justifyBreaks=1, alignment=TA_LEFT,
                                   justifyLastLine=1)
        text = """Elizabeth Holmes<br/>
        Mobile: 313-717-2496<br/>
        Email: el.holmes@gmail.com<br/>
        Socials: inst/el.holmes<br/>
        """
        paragraphReportSummary = Paragraph(text, psDetalle)
        self.elements.append(paragraphReportSummary)
        self.elements.append(PageBreak())

    def nextPagesHeader(self, isSecondPage):
        if isSecondPage:
            psHeaderText = ParagraphStyle('Hed0', fontSize=16, alignment=TA_LEFT, borderWidth=3,
                                          textColor=self.colorOhkaGreen0)
            text = 'REPORTE DE SESIONES'
            paragraphReportHeader = Paragraph(text, psHeaderText)
            self.elements.append(paragraphReportHeader)

            spacer = Spacer(10, 10)
            self.elements.append(spacer)

            d = Drawing(500, 1)
            line = Line(-15, 0, 483, 0)
            line.strokeColor = self.colorOhkaGreenLineas
            line.strokeWidth = 2
            d.add(line)
            self.elements.append(d)

            spacer = Spacer(10, 1)
            self.elements.append(spacer)

            d = Drawing(500, 1)
            line = Line(-15, 0, 483, 0)
            line.strokeColor = self.colorOhkaGreenLineas
            line.strokeWidth = 0.5
            d.add(line)
            self.elements.append(d)

            spacer = Spacer(10, 22)
            self.elements.append(spacer)

    def remoteSessionTableMaker(self):
        psHeaderText = ParagraphStyle('Hed0', fontSize=12, alignment=TA_LEFT, borderWidth=3,
                                      textColor=self.colorOhkaBlue0)
        text = 'SESIONES REMOTAS'
        paragraphReportHeader = Paragraph(text, psHeaderText)
        self.elements.append(paragraphReportHeader)

        spacer = Spacer(10, 22)
        self.elements.append(spacer)
        """
        Create the line items
        """
        d = []
        textData = ["No.", "Fecha", "Hora Inicio", "Hora Fin", "Tiempo Total"]

        fontSize = 8
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
        for text in textData:
            ptext = "<font size='%s'><b>%s</b></font>" % (fontSize, text)
            titlesTable = Paragraph(ptext, centered)
            d.append(titlesTable)

        data = [d]
        lineNum = 1
        formattedLineData = []

        alignStyle = [ParagraphStyle(name="01", alignment=TA_CENTER),
                      ParagraphStyle(name="02", alignment=TA_LEFT),
                      ParagraphStyle(name="03", alignment=TA_CENTER),
                      ParagraphStyle(name="04", alignment=TA_CENTER),
                      ParagraphStyle(name="05", alignment=TA_CENTER)]

        for row in range(10):
            lineData = [str(lineNum), "Miércoles, 11 de diciembre de 2019",
                        "17:30", "19:24", "1:54"]
            # data.append(lineData)
            columnNumber = 0
            for item in lineData:
                ptext = "<font size='%s'>%s</font>" % (fontSize - 1, item)
                p = Paragraph(ptext, alignStyle[columnNumber])
                formattedLineData.append(p)
                columnNumber = columnNumber + 1
            data.append(formattedLineData)
            formattedLineData = []

        # Row for total
        totalRow = ["Total de Horas", "", "", "", "30:15"]
        for item in totalRow:
            ptext = "<font size='%s'>%s</font>" % (fontSize - 1, item)
            p = Paragraph(ptext, alignStyle[1])
            formattedLineData.append(p)
        data.append(formattedLineData)

        # print(data)
        table = Table(data, colWidths=[50, 200, 80, 80, 80])
        tStyle = TableStyle([  # ('GRID',(0, 0), (-1, -1), 0.5, grey),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            # ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ("ALIGN", (1, 0), (1, -1), 'RIGHT'),
            ('LINEABOVE', (0, 0), (-1, -1), 1, self.colorOhkaBlue1),
            ('BACKGROUND', (0, 0), (-1, 0), self.colorOhkaGreenLineas),
            ('BACKGROUND', (0, -1), (-1, -1), self.colorOhkaBlue1),
            ('SPAN', (0, -1), (-2, -1))
        ])
        table.setStyle(tStyle)
        self.elements.append(table)

    def inSiteSessionTableMaker(self):
        self.elements.append(PageBreak())
        psHeaderText = ParagraphStyle('Hed0', fontSize=12, alignment=TA_LEFT, borderWidth=3,
                                      textColor=self.colorOhkaBlue0)
        text = 'SESIONES EN SITIO'
        paragraphReportHeader = Paragraph(text, psHeaderText)
        self.elements.append(paragraphReportHeader)

        spacer = Spacer(10, 22)
        self.elements.append(spacer)
        """
        Create the line items
        """
        d = []
        textData = ["No.", "Fecha", "Hora Inicio", "Hora Fin", "Tiempo Total"]

        fontSize = 8
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
        for text in textData:
            ptext = "<font size='%s'><b>%s</b></font>" % (fontSize, text)
            titlesTable = Paragraph(ptext, centered)
            d.append(titlesTable)

        data = [d]
        lineNum = 1
        formattedLineData = []

        alignStyle = [ParagraphStyle(name="01", alignment=TA_CENTER),
                      ParagraphStyle(name="02", alignment=TA_LEFT),
                      ParagraphStyle(name="03", alignment=TA_CENTER),
                      ParagraphStyle(name="04", alignment=TA_CENTER),
                      ParagraphStyle(name="05", alignment=TA_CENTER)]

        for row in range(10):
            lineData = [str(lineNum), "Miércoles, 11 de diciembre de 2019",
                        "17:30", "19:24", "1:54"]
            # data.append(lineData)
            columnNumber = 0
            for item in lineData:
                ptext = "<font size='%s'>%s</font>" % (fontSize - 1, item)
                p = Paragraph(ptext, alignStyle[columnNumber])
                formattedLineData.append(p)
                columnNumber = columnNumber + 1
            data.append(formattedLineData)
            formattedLineData = []

        # Row for total
        totalRow = ["Total de Horas", "", "", "", "30:15"]
        for item in totalRow:
            ptext = "<font size='%s'>%s</font>" % (fontSize - 1, item)
            p = Paragraph(ptext, alignStyle[1])
            formattedLineData.append(p)
        data.append(formattedLineData)

        # print(data)
        table = Table(data, colWidths=[50, 200, 80, 80, 80])
        tStyle = TableStyle([  # ('GRID',(0, 0), (-1, -1), 0.5, grey),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            # ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ("ALIGN", (1, 0), (1, -1), 'RIGHT'),
            ('LINEABOVE', (0, 0), (-1, -1), 1, self.colorOhkaBlue1),
            ('BACKGROUND', (0, 0), (-1, 0), self.colorOhkaGreenLineas),
            ('BACKGROUND', (0, -1), (-1, -1), self.colorOhkaBlue1),
            ('SPAN', (0, -1), (-2, -1))
        ])
        table.setStyle(tStyle)
        self.elements.append(table)

    def extraActivitiesTableMaker(self):
        self.elements.append(PageBreak())
        psHeaderText = ParagraphStyle('Hed0', fontSize=12, alignment=TA_LEFT, borderWidth=3,
                                      textColor=self.colorOhkaBlue0)
        text = 'OTRAS ACTIVIDADES Y DOCUMENTACIÓN'
        paragraphReportHeader = Paragraph(text, psHeaderText)
        self.elements.append(paragraphReportHeader)

        spacer = Spacer(10, 22)
        self.elements.append(spacer)
        """
        Create the line items
        """
        d = []
        textData = ["No.", "Fecha", "Hora Inicio", "Hora Fin", "Tiempo Total"]

        fontSize = 8
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
        for text in textData:
            ptext = "<font size='%s'><b>%s</b></font>" % (fontSize, text)
            titlesTable = Paragraph(ptext, centered)
            d.append(titlesTable)

        data = [d]
        lineNum = 1
        formattedLineData = []

        alignStyle = [ParagraphStyle(name="01", alignment=TA_CENTER),
                      ParagraphStyle(name="02", alignment=TA_LEFT),
                      ParagraphStyle(name="03", alignment=TA_CENTER),
                      ParagraphStyle(name="04", alignment=TA_CENTER),
                      ParagraphStyle(name="05", alignment=TA_CENTER)]

        for row in range(10):
            lineData = [str(lineNum), "Miércoles, 11 de diciembre de 2019",
                        "17:30", "19:24", "1:54"]
            # data.append(lineData)
            columnNumber = 0
            for item in lineData:
                ptext = "<font size='%s'>%s</font>" % (fontSize - 1, item)
                p = Paragraph(ptext, alignStyle[columnNumber])
                formattedLineData.append(p)
                columnNumber = columnNumber + 1
            data.append(formattedLineData)
            formattedLineData = []

        # Row for total
        totalRow = ["Total de Horas", "", "", "", "30:15"]
        for item in totalRow:
            ptext = "<font size='%s'>%s</font>" % (fontSize - 1, item)
            p = Paragraph(ptext, alignStyle[1])
            formattedLineData.append(p)
        data.append(formattedLineData)

        # print(data)
        table = Table(data, colWidths=[50, 200, 80, 80, 80])
        tStyle = TableStyle([  # ('GRID',(0, 0), (-1, -1), 0.5, grey),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            # ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ("ALIGN", (1, 0), (1, -1), 'RIGHT'),
            ('LINEABOVE', (0, 0), (-1, -1), 1, self.colorOhkaBlue1),
            ('BACKGROUND', (0, 0), (-1, 0), self.colorOhkaGreenLineas),
            ('BACKGROUND', (0, -1), (-1, -1), self.colorOhkaBlue1),
            ('SPAN', (0, -1), (-2, -1))
        ])
        table.setStyle(tStyle)
        self.elements.append(table)

    def summaryTableMaker(self):
        self.elements.append(PageBreak())
        psHeaderText = ParagraphStyle('Hed0', fontSize=12, alignment=TA_LEFT, borderWidth=3,
                                      textColor=self.colorOhkaBlue0)
        text = 'REGISTRO TOTAL DE HORAS'
        paragraphReportHeader = Paragraph(text, psHeaderText)
        self.elements.append(paragraphReportHeader)

        spacer = Spacer(10, 22)
        self.elements.append(spacer)
        """
        Create the line items
        """

        tStyle = TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            # ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ("ALIGN", (1, 0), (1, -1), 'RIGHT'),
            ('LINEABOVE', (0, 0), (-1, -1), 1, self.colorOhkaBlue1),
            ('BACKGROUND', (-2, -1), (-1, -1), self.colorOhkaGreen2)
        ])

        fontSize = 8
        lineData = [["Sesiones remotas", "30:15"],
                    ["Sesiones en sitio", "00:00"],
                    ["Otras actividades", "00:00"],
                    ["Total de horas consumidas", "30:15"]]

        # for row in lineData:
        #     for item in row:
        #         ptext = "<font size='%s'>%s</font>" % (fontSize-1, item)
        #         p = Paragraph(ptext, centered)
        #         formattedLineData.append(p)
        #     data.append(formattedLineData)
        #     formattedLineData = []

        table = Table(lineData, colWidths=[400, 100])
        table.setStyle(tStyle)
        self.elements.append(table)

        # Total de horas contradas vs horas consumidas
        data = []
        formattedLineData = []

        lineData = [["Total de horas contratadas", "120:00"],
                    ["Horas restantes por consumir", "00:00"]]

        # for row in lineData:
        #     for item in row:
        #         ptext = "<b>{}</b>".format(item)
        #         p = Paragraph(ptext, self.styleSheet["BodyText"])
        #         formattedLineData.append(p)
        #     data.append(formattedLineData)
        #     formattedLineData = []

        table = Table(lineData, colWidths=[400, 100])
        tStyle = TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ("ALIGN", (1, 0), (1, -1), 'RIGHT'),
            ('BACKGROUND', (0, 0), (1, 0), self.colorOhkaBlue1),
            ('BACKGROUND', (0, 1), (1, 1), self.colorOhkaGreen1),
        ])
        table.setStyle(tStyle)

        spacer = Spacer(10, 50)
        self.elements.append(spacer)
        self.elements.append(table)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
