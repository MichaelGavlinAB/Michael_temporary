import PyQt5.QtWidgets as qtw
from PyQt5 import QtGui
from PyQt5.QtWidgets import   QApplication, QLabel , QWidget , QPushButton , QVBoxLayout ,QMessageBox ,QFileDialog,QSizePolicy ,QComboBox,QMainWindow
import pandas as pd
import pyqtgraph as pg
from PyQt5.QtGui import QPixmap , QKeySequence
import os
import json
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
        self.Csv_dropdown_menu = qtw.QComboBox()
        self.Csv_dropdown_menu.activated.connect(self.Csv_dropdown_menu_activated)# adding action to combo box
        self.storage =  qtw.QLineEdit() #store temporary path ones clicked to be passed between functions
        self.storage_CSV_data =  qtw.QTextEdit() #store temporary string of data
        self.Time_stamp_display = qtw.QLabel(" Time stamp: ")
        self.storage_CSV_timestamps = qtw.QTextEdit()  # store temporary string of data
        self.graphWidget = pg.PlotWidget() #plot
        self.graphWidget.showGrid(x=True, y=True)
        self.photo = QPixmap() #insert image path in this object
        self.label_image = QLabel() #insert image
        self.label_image.setPixmap(self.photo) #insert image
        self.btn_open_picture = qtw.QPushButton('open images folder from mapi', clicked=self.show_picture)
        self.dropdown_menu_storage_image_names = qtw.QComboBox()
        self.dropdown_menu_storage_image_names.activated.connect(self.Dropdown_image_activated) # adding action to combo box
        self.slider = qtw.QSlider(1) #slider
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
        container.layout().addWidget(self.Time_stamp_display, 7, 0, 1, 1)

        container1.layout().addWidget(self.previous_picture, 0, 0, 0, 1)
        container1.layout().addWidget(self.label_image,0,1,1,1)
        container1.layout().addWidget(self.next_picture, 0, 2, 0, 1)

        container2.layout().addWidget(self.slider, 2, 0, 1, 0)


        container3.layout().addWidget(self.graphWidget, 1, 1, 1, 1)
        container3.layout().addWidget(self.Csv_dropdown_menu, 2, 1, 1, 1)
        container3.layout().addWidget(self.storage_CSV_data, 3, 1, 1, 1) #store temporary string of data
        container3.layout().addWidget(self.storage_CSV_timestamps, 4, 1, 1, 1)  # store temporary string of data

        self.layout().addWidget(container)
        self.layout().addWidget(container1)
        self.layout().addWidget(container2)
        self.layout().addWidget(container3)

# opens csv file search box
    def QPushButton_clicked(self):

        CSV_path = QFileDialog().getOpenFileNames(parent=None, caption='select csv file', filter="csv(*.csv)")

        # dir_ = QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtGui.QFileDialog.ShowDirsOnly)

        CSV_path_str = CSV_path[0][0]
        self.storage.clear()
        self.storage.setText(CSV_path_str) #store path in temporary widget
        dff = pd.read_csv(CSV_path_str)
        headers = dff.columns.tolist()
        headers.pop(0)

        self.Csv_dropdown_menu.clear()

        # add headers to drop down list
        for header in headers:
            self.Csv_dropdown_menu.addItem(header)

    def Csv_dropdown_menu_activated(self):
        print("Csv_dropdown_menu_activated")
        header = self.Csv_dropdown_menu.currentText()
        path = self.storage.text()

        time_stamps , data = self.get_data_from_file(path , header)

        self.storage_CSV_timestamps.clear()
        self.storage_CSV_data.clear()

        #save to storage
        self.storage_CSV_data.setText(str(data))
        self.storage_CSV_timestamps.setText(str(time_stamps))

        #plot data
        clear = 1
        self.plot_grapth(self.graphWidget,time_stamps,data , clear)

    def Csv_dropdown_menu_activated_update(self):
        print("Csv_dropdown_menu_activated_update")
        current_time_string = self.dropdown_menu_storage_image_names.currentText()[-20:-4] # get time from dropdown list
        self.Time_stamp_display.setText(" Time stamp:" + current_time_string)
        if current_time_string.isnumeric():
            current_time = float(current_time_string)
        else:
            current_time = 0

        # current_time = int(self.dropdown_menu_storage_image_names.currentText()[-20:-4])
        time_stamps_from_storage = self.string_to_list(self.storage_CSV_timestamps.toPlainText())# get data from dropdown list
        data_from_storage = self.string_to_list(self.storage_CSV_data.toPlainText())

        if data_from_storage and time_stamps_from_storage:
            Xdata = [current_time, current_time]
            Ydata = [max(data_from_storage),min(data_from_storage)]
            clear = 0
            self.graphWidget.plot(Xdata, Ydata, pen=(255, 0, 0), name="Red curve",clear=True)  # add timestamp
            self.plot_grapth(self.graphWidget, time_stamps_from_storage,data_from_storage, clear)


    def get_data_from_file(self , path,header):
        dff = pd.read_csv(path)
        time_stamp = dff[dff.columns[0]].tolist()
        data = dff[header].tolist()
        return time_stamp , data

    def plot_grapth(self,widget,x_data,y_data,clear):
        #clear = 1 - clear graph
        # clear = 0 - do not clear
        print("plot_grapth")

        #add data to plot
        if clear:
            widget.plot(x_data, y_data , name="data" , clear=True) # plot the data
        else:
            widget.plot(x_data, y_data, name="data")  # plot the data
        # widget.plot(x_data, y_data, name="data", clear=True)  # plot the data
        # widget.enableAutoRange('xy', True)


    def show_picture(self):
        #selec folder with images
        print("show_picture clicked")
        picture_folder_path = QFileDialog.getExistingDirectory(None, 'Select a folder:')
        file_names = os.listdir(picture_folder_path)
        file_names.sort()
        print(file_names)

        #store image names in combo dropdown list
        self.dropdown_menu_storage_image_names.clear()
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
        self.Csv_dropdown_menu_activated_update()

    def slider_move(self):
        number_of_items = self.dropdown_menu_storage_image_names.count()
        self.dropdown_menu_storage_image_names.setCurrentIndex(round(self.slider.value() / 100 * number_of_items))
        self.Dropdown_image_activated()
        print(self.slider.value())

    def next_picture(self):
        # update image
        self.dropdown_menu_storage_image_names.setCurrentIndex(self.dropdown_menu_storage_image_names.currentIndex() + 1)
        self.Dropdown_image_activated()
        #update slider
        number_of_items = self.dropdown_menu_storage_image_names.count()
        current_item_index = self.dropdown_menu_storage_image_names.currentIndex()
        self.slider.setValue(current_item_index/number_of_items*100)

    def previous_picture(self):
        next_picture = self.dropdown_menu_storage_image_names.currentIndex() - 1
        if next_picture >= 0:
            self.dropdown_menu_storage_image_names.setCurrentIndex(next_picture)
            self.Dropdown_image_activated()

        #update slider
        number_of_items = self.dropdown_menu_storage_image_names.count()
        current_item_index = self.dropdown_menu_storage_image_names.currentIndex()
        self.slider.setValue(current_item_index/number_of_items*100)

    def string_to_list(self,string_data):
        #translate string data to list
        if string_data:
            time_stamps_from_storage = string_data[1:-1].split(',')
            data = [float(i) for i in time_stamps_from_storage]
            return data
        else:
            return []



if __name__ == "__main__":
    app = qtw.QApplication([])
    mw = MainWindow()
    app.setStyle(qtw.QStyleFactory.create('Fusion'))
    app.exec_()
