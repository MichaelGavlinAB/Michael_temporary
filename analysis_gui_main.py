import PyQt5.QtWidgets as qtw
from PyQt5 import QtGui
from PyQt5.QtWidgets import   QApplication, QLabel , QWidget , QPushButton , QVBoxLayout ,QMessageBox ,QFileDialog,QSizePolicy ,QComboBox,QMainWindow
import pandas as pd
import pyqtgraph as pg
from PyQt5.QtGui import QPixmap , QKeySequence
import os
import numpy as np
import pyqtgraph.examples

# SIM Image Right.SimImagePorts.SIM Image Right.AbsoluteTimestamp
# 1606587429086254

# pyqtgraph.examples.run() #examples for plotting!!


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

        container1 = qtw.QWidget()
        container1.setLayout(qtw.QGridLayout())

        container2 = qtw.QWidget()
        container2.setLayout(qtw.QGridLayout())

        container3 = qtw.QWidget()
        container3.setLayout(qtw.QGridLayout())

        # buttons and widgets
        self.label = QLabel("1. Choose CSV file")
        self.label3 = QLabel("4. select a folder with images to show'")
        self.btn_open_csv = qtw.QPushButton('click here to choose a csv file',clicked =self.QPushButton_clicked)
        # self.Show_content = qtw.QPushButton('Show content', clicked=self.Choose_from_list)
        self.Csv_dropdown_menu = qtw.QComboBox()
        self.Csv_dropdown_menu1 = qtw.QComboBox()
        self.Csv_dropdown_menu2 = qtw.QComboBox()
        self.Csv_dropdown_menu3 = qtw.QComboBox()
        self.Csv_dropdown_menu4 = qtw.QComboBox()
        # adding action to combo box
        self.Csv_dropdown_menu.activated.connect(self.Csv_dropdown_menu_activated)
        self.Csv_dropdown_menu1.activated.connect(self.Csv_dropdown_menu_activated1)
        self.Csv_dropdown_menu2.activated.connect(self.Csv_dropdown_menu_activated2)
        self.Csv_dropdown_menu3.activated.connect(self.Csv_dropdown_menu_activated3)
        self.Csv_dropdown_menu4.activated.connect(self.Csv_dropdown_menu_activated4)

        self.storage =  qtw.QLineEdit() #store temporary path ones clicked to be passed between functions


        self.graphWidget = pg.PlotWidget() #plot
        self.graphWidget1 = pg.PlotWidget()
        self.graphWidget2 = pg.PlotWidget()
        self.graphWidget3 = pg.PlotWidget()
        self.graphWidget4 = pg.PlotWidget()

        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget1.showGrid(x=True, y=True)
        self.graphWidget2.showGrid(x=True, y=True)
        self.graphWidget3.showGrid(x=True, y=True)
        self.graphWidget4.showGrid(x=True, y=True)


        self.photo = QPixmap() #insert image path in this object
        self.label_image = QLabel() #insert image
        self.label_image.setPixmap(self.photo) #insert image
        self.btn_open_picture = qtw.QPushButton('open image', clicked=self.show_picture)

        self.dropdown_menu_storage_image_names = qtw.QComboBox()
        # adding action to combo box
        self.dropdown_menu_storage_image_names.activated.connect(self.Dropdown_image_activated)
        #slider
        self.slider = qtw.QSlider(1)
        self.slider.valueChanged.connect(self.slider_move)
        self.next_picture = qtw.QPushButton('-->', clicked=self.next_picture)
        self.previous_picture = qtw.QPushButton('<--', clicked=self.previous_picture)

        #first image to show
        picture_path = "/home/michael/Pictures/Wallpapers/autobrains_wallpaper.png"
        self.photo = QPixmap(picture_path).scaledToHeight(450)
        self.label_image.setPixmap(self.photo) #insert image

        # adding to container
        container.layout().addWidget(self.label, 0, 0, 1, 1)
        container.layout().addWidget(self.btn_open_csv,1,1,1,1)
        container.layout().addWidget(self.storage, 1, 0, 1, 1)  # place to hold the path of thr CSV

        # container.layout().addWidget(self.Show_content, 3, 1, 1, 1)
        container.layout().addWidget(self.label3, 5, 0, 1, 1)
        container.layout().addWidget(self.btn_open_picture, 6, 1, 1, 1)
        container.layout().addWidget(self.dropdown_menu_storage_image_names, 6, 0, 1, 1)


        container1.layout().addWidget(self.previous_picture, 0, 0, 0, 1)
        container1.layout().addWidget(self.label_image,0,1,1,1)
        container1.layout().addWidget(self.next_picture, 0, 2, 0, 1)


        container2.layout().addWidget(self.slider, 2, 0, 1, 0)


        container3.layout().addWidget(self.graphWidget, 1, 1, 1, 1)
        container3.layout().addWidget(self.graphWidget1, 1, 2, 1, 1)
        container3.layout().addWidget(self.graphWidget2, 1, 3, 1, 1)
        container3.layout().addWidget(self.graphWidget3, 1, 4, 1, 1)
        container3.layout().addWidget(self.graphWidget4, 1, 5, 1, 1)


        container3.layout().addWidget(self.Csv_dropdown_menu, 2, 1, 1, 1)
        container3.layout().addWidget(self.Csv_dropdown_menu1, 2, 2, 1, 1)
        container3.layout().addWidget(self.Csv_dropdown_menu2, 2, 3, 1, 1)
        container3.layout().addWidget(self.Csv_dropdown_menu3, 2, 4, 1, 1)
        container3.layout().addWidget(self.Csv_dropdown_menu4, 2, 5, 1, 1)

        self.layout().addWidget(container)
        self.layout().addWidget(container1)
        self.layout().addWidget(container2)
        self.layout().addWidget(container3)

# opens csv file search box
    def QPushButton_clicked(self):
        # opens CSV and receive headers
        CSV_path = QFileDialog.getOpenFileNames()
        # dir_ = QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        CSV_path_str = CSV_path[0][0]
        self.storage.setText(CSV_path_str) #store path in temporary widget
        dff = pd.read_csv(CSV_path_str)
        headers = dff.columns.tolist()
        headers.pop(0)

        # add headers to drop down list
        for header in headers:
            self.Csv_dropdown_menu.addItem(header)
        for header in headers:
            self.Csv_dropdown_menu1.addItem(header)
        for header in headers:
            self.Csv_dropdown_menu2.addItem(header)
        for header in headers:
            self.Csv_dropdown_menu3.addItem(header)
        for header in headers:
            self.Csv_dropdown_menu4.addItem(header)

    def Csv_dropdown_menu_activated(self):
        print("Csv_dropdown_menu_activated")
        header = self.Csv_dropdown_menu.currentText()
        path = self.storage.text()

        current_time = int(self.dropdown_menu_storage_image_names.currentText()[-20:-4]) #get time from dropdown list

        time_stamps , data = self.get_data_from_file(path , header)
        print("current time stamp" , current_time)
        self.plot_grapth(self.graphWidget,time_stamps,data,current_time)


    def Csv_dropdown_menu_activated1(self):
        print("Csv_dropdown_menu_activated1")
        header = self.Csv_dropdown_menu1.currentText()
        path = self.storage.text()

        current_time = int(self.dropdown_menu_storage_image_names.currentText()[-20:-4]) #get time from dropdown list

        time_stamp , data = self.get_data_from_file(path , header)
        self.plot_grapth(self.graphWidget1,time_stamp,data,current_time)

    def Csv_dropdown_menu_activated2(self):
        header = self.Csv_dropdown_menu2.currentText()
        path = self.storage.text()
        time_stamp , data = self.get_data_from_file(path , header)
        self.plot_grapth(self.graphWidget2,time_stamp,data,time_stamp[0])

    def Csv_dropdown_menu_activated3(self):
        header = self.Csv_dropdown_menu3.currentText()
        path = self.storage.text()
        time_stamp , data = self.get_data_from_file(path , header)
        self.plot_grapth(self.graphWidget3,time_stamp,data,time_stamp[0])

    def Csv_dropdown_menu_activated4(self):
        header = self.Csv_dropdown_menu4.currentText()
        path = self.storage.text()
        time_stamp, data = self.get_data_from_file(path, header)
        self.plot_grapth(self.graphWidget4, time_stamp, data,time_stamp[0])

    def get_data_from_file(self , path,header):
        dff = pd.read_csv(path)
        time_stamp = dff[dff.columns[0]].tolist()
        data = dff[header].tolist()
        return time_stamp , data

    def plot_grapth(self,widget,x_data,y_daya,current_time):
        # widget.plot(x_data, y_daya,clear=True) # plot the data

        # add time stamp to plot
        Xdata = [current_time, current_time]
        Ydata = [min(y_daya), max(y_daya)]
        widget.plot(Xdata, Ydata, pen=(255, 0, 0), name="Red curve", clear=True)  # add timestamp

        #add data to plot
        widget.plot(x_data, y_daya , pen=(0,0,255), name="Blue curve") # plot the data
        widget.enableAutoRange('xy', True)




    def show_picture(self):
        #selec folder with images
        print("show_picture clicked")
        picture_folder_path = QFileDialog.getExistingDirectory(None, 'Select a folder:')
        file_names = os.listdir(picture_folder_path)
        file_names.sort()
        print(file_names)

        #store image names in combo dropdown list
        for file_name in file_names:
            self.dropdown_menu_storage_image_names.addItem(os.path.join(picture_folder_path,file_name))

        #first image to show
        picture_path = os.path.join(picture_folder_path,file_names[0])
        self.photo = QPixmap(picture_path).scaledToHeight(450)
        self.label_image.setPixmap(self.photo) #insert image


    def Dropdown_image_activated(self):
        #update list
        self.photo = QPixmap(self.dropdown_menu_storage_image_names.currentText()).scaledToHeight(450)
        self.label_image.setPixmap(self.photo)#insert image
        print("Dropdown_image_activated")
        self.Csv_dropdown_menu_activated()
        self.Csv_dropdown_menu_activated1()
        self.Csv_dropdown_menu_activated2()
        self.Csv_dropdown_menu_activated3()
        self.Csv_dropdown_menu_activated4()

        # self.add_timestamp_to_plot()

    def slider_move(self):
        number_of_items = self.dropdown_menu_storage_image_names.count()
        self.dropdown_menu_storage_image_names.setCurrentIndex(round(self.slider.value() / 100 * number_of_items))
        self.Dropdown_image_activated()
        print(self.slider.value())

    def next_picture(self):
        self.dropdown_menu_storage_image_names.setCurrentIndex(self.dropdown_menu_storage_image_names.currentIndex() + 1)
        self.Dropdown_image_activated()

    def previous_picture(self):
        self.dropdown_menu_storage_image_names.setCurrentIndex(self.dropdown_menu_storage_image_names.currentIndex() - 1)
        self.Dropdown_image_activated()




if __name__ == "__main__":
    app = qtw.QApplication([])
    mw = MainWindow()
    app.setStyle(qtw.QStyleFactory.create('Fusion'))
    app.exec_()
