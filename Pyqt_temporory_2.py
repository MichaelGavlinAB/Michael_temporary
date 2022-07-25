import PyQt5.QtWidgets as qtw
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QLabel , QWidget , QPushButton , QVBoxLayout ,QMessageBox ,QFileDialog,QSizePolicy ,QComboBox,QMainWindow
import pandas as pd
import pyqtgraph as pg
from PyQt5.QtGui import QPixmap


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System engineering")
        self.setLayout(qtw.QVBoxLayout())
        self.MyUI()
        self.resize(1500, 1300)
        self.show()

    def MyUI(self):
        container = qtw.QWidget()
        container.setLayout(qtw.QGridLayout())

        # buttons and widgets
        self.btn_open_csv = qtw.QPushButton('click here to choose a csv file',clicked =self.QPushButton_clicked)
        self.Show_content = qtw.QPushButton('Show content', clicked=self.Choose_from_list)
        self.Csv_dropdown_menu = qtw.QComboBox()
        self.storage =  qtw.QLineEdit() #store temporary path ones clicked to be passed between functions
        self.graphWidget = pg.PlotWidget() #plot
        self.photo = QPixmap("/home/michael/Pictures/Wallpapers/autobrains_wallpaper.png").scaledToWidth(1000) #insert image
        self.label = QLabel() #insert image
        # pixmap = pixmap.scaledToWidth(250)
        self.label.setPixmap(self.photo) #insert image
        self.btn_open_picture = qtw.QPushButton('open picture', clicked=self.show_picture)


        # adding to container
        container.layout().addWidget(self.btn_open_csv,0,0,1,2)
        container.layout().addWidget(self.Csv_dropdown_menu,1,0,1,2)
        container.layout().addWidget(self.Show_content, 1, 2, 1, 2)
        container.layout().addWidget(self.graphWidget, 3, 1, 1, 1)
        container.layout().addWidget(self.storage, 4, 1, 1, 1)
        container.layout().addWidget(self.btn_open_picture, 5, 1, 1, 1)
        container.layout().addWidget(self.label,6,1,1,1)
        self.layout().addWidget(container)

# opens csv file search box
    def QPushButton_clicked(self):
        # opens CSV and receive headers
        CSV_path = QFileDialog.getOpenFileNames()
        CSV_path_str = CSV_path[0][0]
        self.storage.setText(CSV_path_str) #store path in temporary widget
        dff = pd.read_csv(CSV_path_str)
        headers = dff.columns.tolist()

        # add headers to drop down list
        for header in headers:
            self.Csv_dropdown_menu.addItem(header)

    def Choose_from_list(self):
        header = self.Csv_dropdown_menu.currentText()
        # path =  "/home/michael/2022.07.11_at_13.30.52_camera-mi_804_35m_l_r_Bike_cross_without_vest_bike_ped.csv" #remove this!!!!!!!!
        path = self.storage.text()
        print(path)

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,0]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45,0]
        time_stamp , data = self.get_data_from_file(path , header)
        print("click")
        print(header)
        self.plot_grapth(self.graphWidget,time_stamp,data)

    def get_data_from_file(self , path,header):
        dff = pd.read_csv(path)
        time_stamp = dff[dff.columns[0]].tolist()
        data = dff[header].tolist()
        return time_stamp , data

    def plot_grapth(self,widget,x_data,y_daya):
        widget.plot(x_data, y_daya, clear=True ) # plot the data

    def show_picture(self):
        print("show_picture clicked")
        # self.photo.setPixmap(QPixmap='self.photo.setPixmap(QPixmap=/home/michael/Desktop/Knowlage/image.png')

if __name__ == "__main__":
    app = qtw.QApplication([])
    mw = MainWindow()
    app.setStyle(qtw.QStyleFactory.create('Fusion'))
    app.exec_()
