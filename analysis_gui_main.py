import PyQt5.QtWidgets as qtw
from PyQt5 import QtGui
from PyQt5.QtWidgets import   QApplication, QLabel , QWidget , QPushButton , QVBoxLayout ,QMessageBox ,QFileDialog,QSizePolicy ,QComboBox,QMainWindow , QCompleter
import pandas as pd
import pyqtgraph as pg
from PyQt5.QtGui import QPixmap , QKeySequence
from PyQt5 import QtCore
import os


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System engineering")
        # self.setLayout(qtw.QVBoxLayout())
        self.setLayout(qtw.QGridLayout())
        self.MyUI()
        self.resize(1500, 1300)
        self.show()

    def MyUI(self):

        #define layout containers
        container = qtw.QWidget()
        container.setLayout(qtw.QGridLayout())

        container1 = qtw.QWidget()
        container1.setLayout(qtw.QGridLayout())

        container2 = qtw.QWidget()
        container2.setLayout(qtw.QGridLayout())

        container3 = qtw.QWidget()
        container3.setLayout(qtw.QGridLayout())

        container_side_widgets = qtw.QWidget()
        container_side_widgets.setLayout(qtw.QGridLayout())

        container_side_by_side_layout = qtw.QWidget()
        container_side_by_side_layout.setLayout(qtw.QGridLayout())



        container4_debug = qtw.QWidget()
        container4_debug.setLayout(qtw.QGridLayout())

        # labels and display (Qlabel)
        self.label = QLabel("1. Choose CSV file")
        self.label3 = QLabel("4. select a folder with images to show'")
        self.Time_stamp_display = qtw.QLCDNumber(14)

        # push Buttons (QPushButton)
        self.btn_open_picture = qtw.QPushButton('open images folder from mapi', clicked=self.show_picture)
        self.btn_reset_scale = qtw.QPushButton('reset scale', clicked=self.btn_reset_scale)
        self.btn_open_csv = qtw.QPushButton('click here to choose a csv file',clicked =self.QPushButton_clicked)
        self.btn_open_picture2 = qtw.QPushButton('optional -  open images folder to compare', clicked=self.show_picture2)
        self.btn_open_picture2.setHidden(1)
        self.next_picture = qtw.QPushButton('-->', clicked=self.next_picture)
        self.previous_picture = qtw.QPushButton('<--', clicked=self.previous_picture)
        self.add_another_picture = qtw.QPushButton('hide / unhide second picture', clicked=self.hide_unhide_second_picture)

        # Drop down menu (Qcombo)
        self.Csv_dropdown_menu = qtw.QComboBox()
        self.Csv_dropdown_menu.activated.connect(self.Csv_dropdown_menu_activated)# adding action to combo box
        self.dropdown_menu_storage_image_names = qtw.QComboBox()
        self.dropdown_menu_storage_image_names.activated.connect(self.Dropdown_image_activated) # adding action to combo box
        self.dropdown_menu_storage_image_names2 = qtw.QComboBox()
        self.dropdown_menu_storage_image_names2.setHidden(1)
        self.dropdown_menu_storage_image_names2.activated.connect(self.Dropdown_image_activated2) # adding action to combo box

        # storage widgets , keep data
        self.storage =  qtw.QLineEdit() #store temporary path ones clicked to be passed between functions
        self.storage_picture_scale = qtw.QLineEdit()
        self.storage_CSV_data =  qtw.QTextEdit() #store temporary string of data
        self.storage_CSV_timestamps = qtw.QTextEdit()  # store temporary string of data
        self.storage_picture_scale.setText("450") # init scale
        self.search_bar = qtw.QLineEdit('search bar')  # search bar
        self.search_bar.textChanged.connect(self.search_bar_activated)


        #   plot widgets
        self.graphWidget = pg.PlotWidget() #plot
        self.graphWidget.showGrid(x=True, y=True)

        # image display
        # init first picture
        self.picture_frame_scene2 = qtw.QGraphicsScene(self)  # set 2nd picture frame scene
        self.photo2 = QPixmap()  # insert image path in this object
        self.picture_frame_scene = qtw.QGraphicsScene(self) #set picture frame scene
        self.picture_frame = qtw.QGraphicsView(self.picture_frame_scene) #final item add to display image
        self.picture_frame2 = qtw.QGraphicsView(self.picture_frame_scene2)  # final item add to display image
        self.picture_frame2.setHidden(1)
        self.picture_frame.setFixedSize(1700,500)
        self.label_image = QLabel() #insert image
        self.label_image2 = QLabel() #insert image


        # slider widget
        self.slider = qtw.QSlider(1) #slider
        self.slider.valueChanged.connect(self.slider_move)

        # completer
        # self.completer = QCompleter(widget_names)


        # dial widget
        self.scale_dial = qtw.QDial()
        self.scale_dial.setMaximum(800)
        self.scale_dial.setMinimum(200)
        self.scale_dial.setValue(450)
        self.scale_dial.setFixedSize(80,100)
        self.scale_dial.valueChanged.connect(self.scale_dial_activated)


        # adding widgets to main layout
        container.layout().addWidget(self.label, 0, 0, 1, 1)
        container.layout().addWidget(self.storage, 0, 1, 1, 1)  # place to hold the path of thr CSV
        container.layout().addWidget(self.btn_open_csv,0,2,1,1)
        container.layout().addWidget(self.label3, 1, 0, 1, 1)
        container.layout().addWidget(self.dropdown_menu_storage_image_names, 1, 1, 1, 1)
        container.layout().addWidget(self.btn_open_picture, 1, 2, 1, 1)
        container.layout().addWidget(self.add_another_picture, 1, 3, 1, 1)
        container.layout().addWidget(self.dropdown_menu_storage_image_names2, 2, 1, 1, 1)
        container.layout().addWidget(self.btn_open_picture2, 2, 2, 1, 1)

        container1.layout().addWidget(self.picture_frame,0,1,1,1)
        container1.layout().addWidget(self.picture_frame2, 1, 1, 1, 1)


        # container2.layout().addWidget(self.Time_stamp_display, 0, 0, 1, 1)
        container2.layout().addWidget(self.previous_picture, 0, 1, 1, 1)
        container2.layout().addWidget(self.slider, 0, 2, 1, 1)
        container2.layout().addWidget(self.next_picture, 0, 3, 1, 1)

        container_side_widgets.layout().addWidget(self.Time_stamp_display,0,0,1,1)
        container_side_widgets.layout().addWidget(self.scale_dial, 1, 0, 1, 1)
        container_side_widgets.layout().addWidget(self.storage_picture_scale, 2, 0, 1, 1)
        container_side_widgets.layout().addWidget(self.btn_reset_scale, 3, 0, 1, 1)

        container3.layout().addWidget(self.search_bar, 0, 1, 1, 1)
        container3.layout().addWidget(self.graphWidget, 1, 1, 1, 1)
        container3.layout().addWidget(self.Csv_dropdown_menu, 2, 1, 1, 1)


        #debug cstorage containers
        # container4_debug.layout().addWidget(self.storage_picture_scale, 1, 1, 1, 1)
        # container4_debug.layout().addWidget(self.scale_dial, 1, 1, 1, 1)
        # container4_debug.layout().addWidget(self.picture_frame, 1, 1, 1, 1)
        # container4_debug.layout().addWidget(self.storage_CSV_data, 3, 1, 1, 1) #store temporary string of data
        # container4_debug.layout().addWidget(self.storage_CSV_timestamps, 4, 1, 1, 1)  # store temporary string of data

        # adding containers to main layout
        self.layout().addWidget(container,0,1,1,1)
        self.layout().addWidget(container1,1,1,1,1)
        self.layout().addWidget(container_side_widgets, 1, 0, 1, 1)
        self.layout().addWidget(container2,2,1,1,1)
        self.layout().addWidget(container3,3,1,1,1)
        self.layout().addWidget(container4_debug,4,1,1,1)

# opens csv file search box
    def QPushButton_clicked(self):

        # action after clicking search csv file button
        CSV_path = QFileDialog().getOpenFileNames(parent=None, caption='select csv file', filter="csv(*.csv)")
        CSV_path_str = CSV_path[0][0]
        self.storage.clear()

        # store csv path in storage widget
        self.storage.setText(CSV_path_str)
        dff = pd.read_csv(CSV_path_str)

        #get headers from csv file , taking first headers out (timestamp)
        headers = dff.columns.tolist()
        headers.pop(0)

        # add headers to drop down list
        self.Csv_dropdown_menu.clear()
        for header in headers:
            self.Csv_dropdown_menu.addItem(header)

    def Csv_dropdown_menu_activated(self):

        #get current header and path from csv dropdown and storage
        print("Csv_dropdown_menu_activated")
        header = self.Csv_dropdown_menu.currentText()
        path = self.storage.text()

        # retrieve data of the desired data header from csv file
        time_stamps , data = self.get_data_from_file(path , header)

        #save to storage
        self.storage_CSV_timestamps.clear()
        self.storage_CSV_timestamps.setText(str(time_stamps))
        self.storage_CSV_data.clear()
        self.storage_CSV_data.setText(str(data))

        #plot data
        clear = 1 #choose if previous plot should be cleared
        self.plot_grapth(self.graphWidget,time_stamps,data , clear)

    def Csv_dropdown_menu_activated_update(self):
        print("Csv_dropdown_menu_activated_update")

        # get current timestamp from image file name
        current_time_string = self.dropdown_menu_storage_image_names.currentText()[-20:-4] # get time from dropdown list

        # convert timestamp to float
        if current_time_string.isnumeric():
            current_time = float(current_time_string)
        else:
            current_time = 0

        self.Time_stamp_display.display(current_time_string)

        # get timestamps and data from storage widget and convert to numeric list
        time_stamps_from_storage = self.string_to_list(self.storage_CSV_timestamps.toPlainText())# get data from dropdown list
        data_from_storage = self.string_to_list(self.storage_CSV_data.toPlainText())

        # plot timestamp red marker + plot data again
        if data_from_storage and time_stamps_from_storage:
            Xdata = [current_time, current_time]
            Ydata = [max(data_from_storage),min(data_from_storage)]
            clear = 0
            self.graphWidget.plot(Xdata, Ydata, pen=(255, 0, 0), name="Red curve",clear=True)  # add timestamp
            self.plot_grapth(self.graphWidget, time_stamps_from_storage,data_from_storage, clear)

        #update second picture
        self.dropdown_menu_storage_image_names2.setCurrentIndex(self.dropdown_menu_storage_image_names.currentIndex())


    def get_data_from_file(self , path,header):

        # read from csv file and convert to list
        dff = pd.read_csv(path)
        time_stamp = dff[dff.columns[0]].tolist()
        data = dff[header].tolist()

        return time_stamp , data

    def plot_grapth(self,widget,x_data,y_data,clear):
        #clear = 1 - clear current plot , clear = 0 - do not clear current plot

        #add data to plot
        if clear:
            widget.plot(x_data, y_data , name="data" , clear=True) # plot the data
        else:
            widget.plot(x_data, y_data, name="data")  # plot the data
        # widget.plot(x_data, y_data, name="data", clear=True)  # plot the data
        # widget.enableAutoRange('xy', True)


    def show_picture(self):

        #user select path with images
        print("show_picture clicked")
        picture_folder_path = QFileDialog.getExistingDirectory(None, 'Select a folder:')
        file_names = os.listdir(picture_folder_path)
        file_names.sort()
        print(file_names)

        #store image names in combo dropdown list
        self.dropdown_menu_storage_image_names.clear()
        for file_name in file_names:
            self.dropdown_menu_storage_image_names.addItem(os.path.join(picture_folder_path,file_name))

        picture_path = os.path.join(picture_folder_path,file_names[0])
        scale = int(self.storage_picture_scale.text())

        # display first image
        self.photo = QPixmap(picture_path)
        item = qtw.QGraphicsPixmapItem(self.photo)
        self.picture_frame_scene.clear()
        self.picture_frame_scene.addItem(item)


    def show_picture2(self):
        #user select path with images
        print("show_picture clicked2")
        picture_folder_path = QFileDialog.getExistingDirectory(None, 'Select a folder:')
        file_names = os.listdir(picture_folder_path)
        file_names.sort()
        print(file_names)

        #store image names in combo dropdown list
        self.dropdown_menu_storage_image_names2.clear()
        for file_name in file_names:
            self.dropdown_menu_storage_image_names2.addItem(os.path.join(picture_folder_path,file_name))

        #display first image
        picture_path = os.path.join(picture_folder_path,file_names[0])
        scale = int(self.storage_picture_scale.text())
        # self.Dropdown_image_activated() #update scale of first image

        # display first image
        self.photo = QPixmap(picture_path)
        item = qtw.QGraphicsPixmapItem(self.photo)
        self.picture_frame_scene2.clear()
        self.picture_frame_scene2.addItem(item)

        # self.photo2 = QPixmap(picture_path).scaledToHeight(scale)
        # self.label_image2.setPixmap(self.photo2) #insert image





    def Dropdown_image_activated(self):
        #update list
        scale = int(self.storage_picture_scale.text())
        self.photo = QPixmap(self.dropdown_menu_storage_image_names.currentText()).scaledToHeight(scale)
        self.label_image.setPixmap(self.photo)#insert image

        item = qtw.QGraphicsPixmapItem(self.photo)
        # self.picture_frame_scene2 = qtw.QGraphicsScene(self)  # set 2nd picture frame scene
        self.picture_frame_scene.clear()
        self.picture_frame_scene.addItem(item)



        print("Dropdown_image_activated")
        self.Csv_dropdown_menu_activated_update()

    def Dropdown_image_activated2(self):
        #update list
        scale = int(self.storage_picture_scale.text())
        self.photo = QPixmap(self.dropdown_menu_storage_image_names2.currentText()).scaledToHeight(scale)
        self.label_image2.setPixmap(self.photo)#insert image

        item = qtw.QGraphicsPixmapItem(self.photo)
        self.picture_frame_scene2.clear()
        self.picture_frame_scene2.addItem(item)

        print("Dropdown_image_activated2")
        # self.Csv_dropdown_menu_activated_update()

    def slider_move(self):
        number_of_items = self.dropdown_menu_storage_image_names.count()
        self.dropdown_menu_storage_image_names.setCurrentIndex(round(self.slider.value() / 100 * number_of_items))
        self.Dropdown_image_activated()
        self.Dropdown_image_activated2()
        print(self.slider.value())

    def next_picture(self):
        # update image
        self.dropdown_menu_storage_image_names.setCurrentIndex(self.dropdown_menu_storage_image_names.currentIndex() + 1)
        self.Dropdown_image_activated()
        self.Dropdown_image_activated2()

        #update slider
        number_of_items = self.dropdown_menu_storage_image_names.count()
        current_item_index = self.dropdown_menu_storage_image_names.currentIndex()
        self.slider.setValue(current_item_index/number_of_items*100)

    def previous_picture(self):
        next_picture = self.dropdown_menu_storage_image_names.currentIndex() - 1
        if next_picture >= 0:
            self.dropdown_menu_storage_image_names.setCurrentIndex(next_picture)
            self.Dropdown_image_activated()
            self.Dropdown_image_activated2()

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

    def scale_dial_activated(self):
        # print(self.scale_dial.value())
        self.storage_picture_scale.setText(str(self.scale_dial.value()))
        self.Dropdown_image_activated()
        self.Dropdown_image_activated2()

    def hide_unhide_second_picture(self):
        #add new image
        if self.picture_frame2.isHidden():
            #unhide second image to compare widgets
            self.picture_frame2.setHidden(0)
            self.dropdown_menu_storage_image_names2.setHidden(0)
            self.btn_open_picture2.setHidden(0)
            self.picture_frame.setFixedSize(1500,260)
            self.picture_frame2.setFixedSize(1500,260)
        else:
            #hide second image to compare widgets
            self.picture_frame2.setHidden(1)
            self.dropdown_menu_storage_image_names2.setHidden(1)
            self.btn_open_picture2.setHidden(1)
            self.picture_frame.setFixedSize(1700,500)

    def btn_reset_scale(self):
        self.storage_picture_scale.setText('450')
        self.Dropdown_image_activated()
        self.Dropdown_image_activated2()

    def search_bar_activated(self):
        print("dsfsd")






if __name__ == "__main__":
    app = qtw.QApplication([])
    mw = MainWindow()
    app.setStyle(qtw.QStyleFactory.create('Fusion'))
    app.exec_()
