import PyQt5.QtWidgets as qtw
from PyQt5.QtWidgets import QApplication, QLabel , QWidget , QPushButton , QVBoxLayout ,QMessageBox ,QFileDialog,QSizePolicy ,QComboBox,QMainWindow
import pandas as pd
import pyqtgraph as pg



class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System engineering")
        self.setLayout(qtw.QVBoxLayout())
        self.MyUI()
        self.show()

    def MyUI(self):
        container = qtw.QWidget()
        container.setLayout(qtw.QGridLayout())

        # buttons
        self.btn_open_csv = qtw.QPushButton('click here to choose a csv file',clicked =self.QPushButton_clicked)
        self.Show_content = qtw.QPushButton('Show content', clicked=self.Choose_from_list)
        self.Csv_dropdown_menu = qtw.QComboBox()
        self.graphWidget = pg.PlotWidget() #plot

        # adding to container
        container.layout().addWidget(self.btn_open_csv,0,0,1,2)
        container.layout().addWidget(self.Csv_dropdown_menu,1,0,1,2)
        container.layout().addWidget(self.Show_content, 1, 2, 1, 2)
        container.layout().addWidget(self.graphWidget, 3, 1, 1, 1)
        self.layout().addWidget(container)

# opens csv file search box
    def QPushButton_clicked(self):
        # opens CSV and receive headers
        CSV_path = QFileDialog.getOpenFileNames()
        CSV_path_str = CSV_path[0][0]
        dff = pd.read_csv(CSV_path_str)
        headers = dff.columns.tolist()
        # print(headers)
        # add headers to drop down list
        for header in headers:
            self.Csv_dropdown_menu.addItem(header)

    def Choose_from_list(self):
        header = self.Csv_dropdown_menu.currentText()
        path =  "/home/michael/2022.07.11_at_13.30.52_camera-mi_804_35m_l_r_Bike_cross_without_vest_bike_ped.csv"
        # print(header)
        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,0]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45,0]
        self.get_pandas(path,header)
        self.plot(self.graphWidget,hour,temperature)

    def get_pandas(self , path,header):
        dff = pd.read_csv(path)
        dff.iloc[:,:1]




    def plot(self,widget,x_data,y_daya):
        widget.plot(x_data, y_daya) # plot the data



app = qtw.QApplication([])
mw = MainWindow()
app.setStyle(qtw.QStyleFactory.create('Fusion'))
app.exec_()
