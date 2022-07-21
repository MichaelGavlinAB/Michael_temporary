import PyQt5.QtWidgets as qtw
from PyQt5.QtWidgets import QApplication, QLabel , QWidget , QPushButton , QVBoxLayout ,QMessageBox ,QFileDialog ,QComboBox,QMainWindow
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System engineering")
        self.setLayout(qtw.QVBoxLayout())
        self.keypad()

        self.show()
    def keypad(self):
        container = qtw.QWidget()
        container.setLayout(qtw.QGridLayout())

        # buttons
        self.btn_open_csv = qtw.QPushButton('click here to choose a csv file',clicked =self.QPushButton_clicked)
        self.Show_content = qtw.QPushButton('Show content', clicked=self.Choose_from_list)
        self.Csv_dropdown_menu = qtw.QComboBox()

        # adding to container
        container.layout().addWidget(self.btn_open_csv,0,0,1,2)
        container.layout().addWidget(self.Csv_dropdown_menu,1,0,1,2)
        container.layout().addWidget(self.Show_content, 1, 2, 1, 2)
        self.layout().addWidget(container)

# opens csv file search box
    def QPushButton_clicked(self):
        # opens CSV and receive headers
        CSV_path = QFileDialog.getOpenFileNames()
        CSV_path_str = CSV_path[0][0]
        dff = pd.read_csv(CSV_path_str)
        headers = dff.columns.tolist()
        print(headers)
        # add headers to drop down list
        for header in headers:
            print(header)
            self.Csv_dropdown_menu.addItem(header)

    def Choose_from_list(self):
        print(self.Csv_dropdown_menu.currentText())







app = qtw.QApplication([])
mw = MainWindow()
app.setStyle(qtw.QStyleFactory.create('Fusion'))
app.exec_()
