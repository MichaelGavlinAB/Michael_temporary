import PyQt5.QtWidgets as qtw
from PyQt5 import QtGui
from PyQt5.QtWidgets import   QApplication, QLabel , QWidget , QPushButton , QVBoxLayout ,QMessageBox ,QFileDialog,QSizePolicy ,QComboBox,QMainWindow , QCompleter
from PyQt5.QtCore import Qt
import pandas as pd
import pyqtgraph as pg
from PyQt5.QtGui import QPixmap , QKeySequence
from PyQt5 import QtCore
import os
print(qtw.QStyleFactory.keys())

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MTS \ Mapi analysis tool")
        # self.setLayout(qtw.QVBoxLayout())
        self.setLayout(qtw.QGridLayout())
        self.MyUI()
        self.resize(1500, 1300)
        self.show()

        # List of names, widgets are stored in a dictionary by these keys.


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
        self.Time_stamp_display = qtw.QLCDNumber(15)
        self.display_search_results = qtw.QListWidget()
        self.display_search_results.itemDoubleClicked.connect(self.display_search_results_clicked)
        self.display_search_results.hide()


        # push Buttons (QPushButton)
        self.btn_open_picture = qtw.QPushButton('open images folder from mapi', clicked=self.show_picture)
        self.btn_reset_scale = qtw.QPushButton('reset scale', clicked=self.btn_reset_scale)
        self.btn_open_csv = qtw.QPushButton('click here to choose a csv file',clicked =self.QPushButton_clicked)
        self.btn_open_picture2 = qtw.QPushButton('open images folder to compare', clicked=self.show_picture2)
        self.btn_open_picture2.setHidden(1)
        self.next_picture = qtw.QPushButton('-->', clicked=self.next_picture)
        self.previous_picture = qtw.QPushButton('<--', clicked=self.previous_picture)
        self.add_another_picture = qtw.QPushButton('+', clicked=self.hide_unhide_second_picture)
        self.add_another_plot = qtw.QPushButton('add plot', clicked=self.add_another_plot)
        self.remove_plot = qtw.QPushButton('remove_plot', clicked=self.remove_plot)

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
        self.search_bar = qtw.QLineEdit()  # search bar
        self.search_bar.textChanged.connect(self.search_bar_activated)


        #   plot widgets
        self.graphWidget = pg.PlotWidget() #plot
        self.graphWidget.showGrid(x=True, y=True)

        # image display
        # init first picture
        self.picture_frame_scene = qtw.QGraphicsScene(self) #set picture frame scene
        self.picture_frame_scene2 = qtw.QGraphicsScene(self)  # set 2nd picture frame scene
        self.picture_frame = qtw.QGraphicsView(self.picture_frame_scene) #final item add to display image
        self.picture_frame2 = qtw.QGraphicsView(self.picture_frame_scene2)  # final item add to display image
        self.picture_frame.setFixedSize(1700,500)
        self.picture_frame2.setHidden(1)
        self.label_image = QLabel() #insert image
        self.label_image2 = QLabel() #insert image


        # slider widget
        self.slider = qtw.QSlider(1) #slider
        self.slider.valueChanged.connect(self.slider_move)

        # dial widget
        self.scale_dial = qtw.QDial()
        self.scale_dial.setMaximum(800)
        self.scale_dial.setMinimum(200)
        self.scale_dial.setValue(450)
        self.scale_dial.setFixedSize(80,100)
        self.scale_dial.valueChanged.connect(self.scale_dial_activated)

        # another plots 1 ##################################################################3
        self.search_bar1 = qtw.QLineEdit()  # search bar
        self.search_bar1.textChanged.connect(self.search_bar_activated1)
        self.display_search_results1 = qtw.QListWidget()
        self.display_search_results1.itemDoubleClicked.connect(self.display_search_results_clicked1)
        self.display_search_results1.hide()
        self.Csv_dropdown_menu1 = qtw.QComboBox()
        self.Csv_dropdown_menu1.activated.connect(self.Csv_dropdown_menu_activated1)# adding action to combo box
        self.graphWidget1 = pg.PlotWidget() #plot
        self.graphWidget1.showGrid(x=True, y=True)
        self.storage_CSV_data1 =  qtw.QTextEdit() #store temporary string of data
        self.search_bar1.hide()
        self.Csv_dropdown_menu1.hide()
        self.graphWidget1.hide()
        self.search_bar1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.Csv_dropdown_menu1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.graphWidget1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # another plots 2 ##################################################################3
        self.search_bar2 = qtw.QLineEdit()  # search bar
        self.search_bar2.textChanged.connect(self.search_bar_activated2)
        self.display_search_results2 = qtw.QListWidget()
        self.display_search_results2.itemDoubleClicked.connect(self.display_search_results_clicked2)
        self.display_search_results2.hide()
        self.Csv_dropdown_menu2 = qtw.QComboBox()
        self.Csv_dropdown_menu2.activated.connect(self.Csv_dropdown_menu_activated2)# adding action to combo box
        self.graphWidget2 = pg.PlotWidget() #plot
        self.graphWidget2.showGrid(x=True, y=True)
        self.storage_CSV_data2 =  qtw.QTextEdit() #store temporary string of data
        self.search_bar2.hide()
        self.Csv_dropdown_menu2.hide()
        self.graphWidget2.hide()

        # another plots 3 ##################################################################3
        self.search_bar3 = qtw.QLineEdit()  # search bar
        self.search_bar3.textChanged.connect(self.search_bar_activated3)
        self.display_search_results3 = qtw.QListWidget()
        self.display_search_results3.itemDoubleClicked.connect(self.display_search_results_clicked3)
        self.display_search_results3.hide()
        self.Csv_dropdown_menu3 = qtw.QComboBox()
        self.Csv_dropdown_menu3.activated.connect(self.Csv_dropdown_menu_activated3)# adding action to combo box
        self.graphWidget3 = pg.PlotWidget() #plot
        self.graphWidget3.showGrid(x=True, y=True)
        self.storage_CSV_data3 =  qtw.QTextEdit() #store temporary string of data
        self.search_bar3.hide()
        self.Csv_dropdown_menu3.hide()
        self.graphWidget3.hide()

        # another plots 4 ##################################################################3
        self.search_bar4 = qtw.QLineEdit()  # search bar
        self.search_bar4.textChanged.connect(self.search_bar_activated4)
        self.display_search_results4 = qtw.QListWidget()
        self.display_search_results4.itemDoubleClicked.connect(self.display_search_results_clicked4)
        self.display_search_results4.hide()
        self.Csv_dropdown_menu4 = qtw.QComboBox()
        self.Csv_dropdown_menu4.activated.connect(self.Csv_dropdown_menu_activated4)# adding action to combo box
        self.graphWidget4 = pg.PlotWidget() #plot
        self.graphWidget4.showGrid(x=True, y=True)
        self.storage_CSV_data4 =  qtw.QTextEdit() #store temporary string of data
        self.search_bar4.hide()
        self.Csv_dropdown_menu4.hide()
        self.graphWidget4.hide()

        # another plots 5 ##################################################################3
        self.search_bar5 = qtw.QLineEdit()  # search bar
        self.search_bar5.textChanged.connect(self.search_bar_activated5)
        self.display_search_results5 = qtw.QListWidget()
        self.display_search_results5.itemDoubleClicked.connect(self.display_search_results_clicked5)
        self.display_search_results5.hide()
        self.Csv_dropdown_menu5 = qtw.QComboBox()
        self.Csv_dropdown_menu5.activated.connect(self.Csv_dropdown_menu_activated5)# adding action to combo box
        self.graphWidget5 = pg.PlotWidget() #plot
        self.graphWidget5.showGrid(x=True, y=True)
        self.storage_CSV_data5 =  qtw.QTextEdit() #store temporary string of data
        self.search_bar5.hide()
        self.Csv_dropdown_menu5.hide()
        self.graphWidget5.hide()


        # # size policty
        # self.search_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.Csv_dropdown_menu.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.graphWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.search_bar5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.Csv_dropdown_menu5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.graphWidget5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.search_bar4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.Csv_dropdown_menu4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.graphWidget4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.search_bar3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.Csv_dropdown_menu3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.graphWidget3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.search_bar2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.Csv_dropdown_menu2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.graphWidget2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #






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

        container3.layout().addWidget(self.search_bar, 0, 0, 1, 1)
        container3.layout().addWidget(self.display_search_results, 1, 0, 1, 1)
        container3.layout().addWidget(self.Csv_dropdown_menu, 2, 0, 1, 1)
        container3.layout().addWidget(self.graphWidget, 3, 0, 1, 1)

        container3.layout().addWidget(self.search_bar1, 0, 1, 1, 1)
        container3.layout().addWidget(self.display_search_results1, 1, 1, 1, 1)
        container3.layout().addWidget(self.Csv_dropdown_menu1, 2, 1, 1, 1)
        container3.layout().addWidget(self.graphWidget1, 3,1, 1, 1)

        container3.layout().addWidget(self.search_bar2, 0, 2, 1, 1)
        container3.layout().addWidget(self.display_search_results2, 1, 2, 1, 1)
        container3.layout().addWidget(self.Csv_dropdown_menu2, 2, 2, 1, 1)
        container3.layout().addWidget(self.graphWidget2, 3, 2, 1, 1)

        container3.layout().addWidget(self.search_bar3, 0, 3, 1, 1)
        container3.layout().addWidget(self.display_search_results3, 1, 3, 1, 1)
        container3.layout().addWidget(self.Csv_dropdown_menu3, 2, 3, 1, 1)
        container3.layout().addWidget(self.graphWidget3, 3, 3, 1, 1)

        container3.layout().addWidget(self.search_bar4, 0, 4, 1, 1)
        container3.layout().addWidget(self.display_search_results4, 1, 4, 1, 1)
        container3.layout().addWidget(self.Csv_dropdown_menu4, 2, 4, 1, 1)
        container3.layout().addWidget(self.graphWidget4, 3, 4, 1, 1)

        container3.layout().addWidget(self.search_bar5, 0, 5, 1, 1)
        container3.layout().addWidget(self.display_search_results5, 1, 5, 1, 1)
        container3.layout().addWidget(self.Csv_dropdown_menu5, 2, 5, 1, 1)
        container3.layout().addWidget(self.graphWidget5, 3, 5, 1, 1)
        container3.layout().addWidget(self.add_another_plot, 0, 6, 1, 1)
        container3.layout().addWidget(self.remove_plot, 3, 6, 1, 1)


        #debug cstorage containers
        # container4_debug.layout().addWidget(self.storage_picture_scale, 1, 1, 1, 1)
        # container4_debug.layout().addWidget(self.scale_dial, 1, 1, 1, 1)
        # container4_debug.layout().addWidget(self.picture_frame, 1, 1, 1, 1)
        # container4_debug.layout().addWidget(self.storage_CSV_data, 3, 1, 1, 1) #store temporary string of data
        # container4_debug.layout().addWidget(self.storage_CSV_timestamps, 4, 1, 1, 1)  # store temporary string of data
        # container4_debug.layout().addWidget(self.display_search_results, 1, 1, 1, 1)


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
            self.Csv_dropdown_menu1.addItem(header)
            self.Csv_dropdown_menu2.addItem(header)
            self.Csv_dropdown_menu3.addItem(header)
            self.Csv_dropdown_menu4.addItem(header)
            self.Csv_dropdown_menu5.addItem(header)




    def Csv_dropdown_menu_activated(self):
        self.Csv_dropdown_menu_activated_function(self.Csv_dropdown_menu , self.storage , self.storage_CSV_timestamps , self.storage_CSV_data,self.graphWidget)

    def Csv_dropdown_menu_activated1(self):
        self.Csv_dropdown_menu_activated_function(self.Csv_dropdown_menu1 , self.storage , self.storage_CSV_timestamps , self.storage_CSV_data1 ,self.graphWidget1)

    def Csv_dropdown_menu_activated2(self):
        self.Csv_dropdown_menu_activated_function(self.Csv_dropdown_menu2 , self.storage , self.storage_CSV_timestamps , self.storage_CSV_data2 ,self.graphWidget2)

    def Csv_dropdown_menu_activated3(self):
        self.Csv_dropdown_menu_activated_function(self.Csv_dropdown_menu3 , self.storage , self.storage_CSV_timestamps , self.storage_CSV_data3  ,self.graphWidget3)

    def Csv_dropdown_menu_activated4(self):
        self.Csv_dropdown_menu_activated_function(self.Csv_dropdown_menu4 , self.storage , self.storage_CSV_timestamps , self.storage_CSV_data4 ,self.graphWidget4)

    def Csv_dropdown_menu_activated5(self):
        self.Csv_dropdown_menu_activated_function(self.Csv_dropdown_menu5 , self.storage , self.storage_CSV_timestamps , self.storage_CSV_data5 ,self.graphWidget5)


    def Csv_dropdown_menu_activated_function(self , Csv_dropdown_menu , storage ,storage_CSV_timestamps , storage_CSV_data ,graphWidget):
        #get current header and path from csv dropdown and storage
        print("Csv_dropdown_menu_activated")
        header = Csv_dropdown_menu.currentText()
        path = storage.text()

        # retrieve data of the desired data header from csv file
        time_stamps , data = self.get_data_from_file(path , header)

        #save to storage
        storage_CSV_timestamps.clear()
        storage_CSV_timestamps.setText(str(time_stamps))
        storage_CSV_data.clear()
        storage_CSV_data.setText(str(data))

        #plot data
        clear = 1 #choose if previous plot should be cleared
        self.plot_grapth(graphWidget,time_stamps,data , clear)

    def Csv_dropdown_menu_activated_update(self):
        self.Csv_dropdown_menu_activated_update_function(self.dropdown_menu_storage_image_names , self.Time_stamp_display,self.graphWidget,self.storage_CSV_data)

    def Csv_dropdown_menu_activated_update1(self):
        self.Csv_dropdown_menu_activated_update_function(self.dropdown_menu_storage_image_names , self.Time_stamp_display,self.graphWidget1 , self.storage_CSV_data1)

    def Csv_dropdown_menu_activated_update2(self):
        self.Csv_dropdown_menu_activated_update_function(self.dropdown_menu_storage_image_names , self.Time_stamp_display,self.graphWidget2 , self.storage_CSV_data2)

    def Csv_dropdown_menu_activated_update3(self):
        self.Csv_dropdown_menu_activated_update_function(self.dropdown_menu_storage_image_names , self.Time_stamp_display,self.graphWidget3 , self.storage_CSV_data3)

    def Csv_dropdown_menu_activated_update4(self):
        self.Csv_dropdown_menu_activated_update_function(self.dropdown_menu_storage_image_names , self.Time_stamp_display,self.graphWidget4 , self.storage_CSV_data4)

    def Csv_dropdown_menu_activated_update5(self):
        self.Csv_dropdown_menu_activated_update_function(self.dropdown_menu_storage_image_names , self.Time_stamp_display,self.graphWidget5 , self.storage_CSV_data5)

    def Csv_dropdown_menu_activated_update_function(self , dropdown_menu_storage_image_names,Time_stamp_display,graphWidget , storage_CSV_data):
        # get current timestamp from image file name
        current_time_string = dropdown_menu_storage_image_names.currentText()[-20:-4] # get time from dropdown list

        # convert timestamp to float
        if current_time_string.isnumeric():
            current_time = float(current_time_string)
        else:
            current_time = 0
        Time_stamp_display.display(current_time_string)
        print("current_time_string: \n", current_time_string)

        # get timestamps and data from storage widget and convert to numeric list
        time_stamps_from_storage = self.string_to_list(self.storage_CSV_timestamps.toPlainText())# get data from dropdown list
        data_from_storage = self.string_to_list(storage_CSV_data.toPlainText())

        # plot timestamp red marker + plot data again
        if data_from_storage and time_stamps_from_storage:
            Xdata = [current_time, current_time]
            Ydata = [max(data_from_storage),min(data_from_storage)]
            graphWidget.plot(Xdata, Ydata, pen=(255, 0, 0), name="Red curve",clear=True)  # add timestamp
            clear = 0
            self.plot_grapth(graphWidget, time_stamps_from_storage,data_from_storage, clear)

        #update second picture
        self.dropdown_menu_storage_image_names2.setCurrentIndex(dropdown_menu_storage_image_names.currentIndex())


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

        # display first image
        scale = int(self.storage_picture_scale.text())
        self.photo = QPixmap(picture_path).scaledToHeight(scale)
        self.picture_frame_scene.clear()
        self.picture_frame_scene.addPixmap(self.photo)



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


        # display  image
        picture_path = os.path.join(picture_folder_path, file_names[0])
        scale = int(self.storage_picture_scale.text())

        self.photo = QPixmap(picture_path).scaledToHeight(scale)
        self.picture_frame_scene2.clear()
        self.picture_frame_scene2.addPixmap(self.photo)


    def Dropdown_image_activated(self):
        #update list
        scale = int(self.storage_picture_scale.text())
        self.photo = QPixmap(self.dropdown_menu_storage_image_names.currentText()).scaledToHeight(scale)
        self.picture_frame_scene.clear()
        self.picture_frame_scene.addPixmap(self.photo)

        print("Dropdown_image_activated")

        self.Csv_dropdown_menu_activated_update()
        self.Csv_dropdown_menu_activated_update1()
        self.Csv_dropdown_menu_activated_update2()
        self.Csv_dropdown_menu_activated_update3()
        self.Csv_dropdown_menu_activated_update4()
        self.Csv_dropdown_menu_activated_update5()


    def Dropdown_image_activated2(self):
        #update list
        scale = int(self.storage_picture_scale.text())
        self.photo = QPixmap(self.dropdown_menu_storage_image_names2.currentText()).scaledToHeight(scale)
        self.picture_frame_scene2.clear()
        self.picture_frame_scene2.addPixmap(self.photo)

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
            self.add_another_picture.setText('-')
        else:
            #hide second image to compare widgets
            self.picture_frame2.setHidden(1)
            self.dropdown_menu_storage_image_names2.setHidden(1)
            self.btn_open_picture2.setHidden(1)
            self.picture_frame.setFixedSize(1700,500)
            self.add_another_picture.setText('+')

    def btn_reset_scale(self):
        self.storage_picture_scale.setText('450')
        self.Dropdown_image_activated()
        self.Dropdown_image_activated2()

    def search_bar_activated(self):
        self.search_bar_activated_function(self.search_bar,self.display_search_results,self.Csv_dropdown_menu)

    def search_bar_activated1(self):
        self.search_bar_activated_function(self.search_bar1,self.display_search_results1,self.Csv_dropdown_menu1)

    def search_bar_activated2(self):
        self.search_bar_activated_function(self.search_bar2,self.display_search_results2,self.Csv_dropdown_menu2)

    def search_bar_activated3(self):
        self.search_bar_activated_function(self.search_bar3,self.display_search_results3,self.Csv_dropdown_menu3)

    def search_bar_activated4(self):
        self.search_bar_activated_function(self.search_bar4,self.display_search_results4,self.Csv_dropdown_menu4)

    def search_bar_activated5(self):
        self.search_bar_activated_function(self.search_bar5,self.display_search_results5,self.Csv_dropdown_menu5)

    def search_bar_activated_function(self,search_bar,display_search_results,Csv_dropdown_menu):
        if search_bar.text():
            display_search_results.show()
            print("search_bar_activated")
            # get csv headers from dropdown list
            AllItems = [Csv_dropdown_menu.itemText(i) for i in range( Csv_dropdown_menu.count())]

            # lowercase all results for easy search
            def lower_case(items_to_lower :str):
                return items_to_lower.lower()
            AllItems_lowercase = list(map(lower_case,AllItems))

            # search for requested field in results
            matches = []
            i = 0
            for AllItem_lowercase in AllItems_lowercase:
                if search_bar.text().lower() in AllItem_lowercase:
                    matches.append(AllItem_lowercase)
            print('matches' , matches)

            # change matches to original state (not lower case)
            matches_to_original = []
            for AllItem in AllItems:
                for match in matches:
                    if match.lower() == AllItem.lower():
                        matches_to_original.append(AllItem)

            display_search_results.clear()
            display_search_results.addItems(matches_to_original)
        else:
            display_search_results.hide()

    def display_search_results_clicked(self , item):
        self.display_search_results_clicked_function(self.Csv_dropdown_menu,item,self.Csv_dropdown_menu_activated,self.display_search_results,self.search_bar)

    def display_search_results_clicked1(self , item):
        self.display_search_results_clicked_function(self.Csv_dropdown_menu1,item,self.Csv_dropdown_menu_activated1,self.display_search_results1,self.search_bar1)

    def display_search_results_clicked2(self , item):
        self.display_search_results_clicked_function(self.Csv_dropdown_menu2,item,self.Csv_dropdown_menu_activated2,self.display_search_results2,self.search_bar2)

    def display_search_results_clicked3(self , item):
        self.display_search_results_clicked_function(self.Csv_dropdown_menu3,item,self.Csv_dropdown_menu_activated3,self.display_search_results3,self.search_bar3)

    def display_search_results_clicked4(self , item):
        self.display_search_results_clicked_function(self.Csv_dropdown_menu4,item,self.Csv_dropdown_menu_activated4,self.display_search_results4,self.search_bar4)

    def display_search_results_clicked5(self , item):
        self.display_search_results_clicked_function(self.Csv_dropdown_menu5,item,self.Csv_dropdown_menu_activated5,self.display_search_results5,self.search_bar5)

    def display_search_results_clicked_function(self,Csv_dropdown_menu,item,Csv_dropdown_menu_activated,display_search_results,search_bar):
        #change plot so selected value
        print('item clicked:', item.text())
        for i in range (Csv_dropdown_menu.count()):
            if Csv_dropdown_menu.itemText(i) == item.text():
                Csv_dropdown_menu.setCurrentIndex(i)

        Csv_dropdown_menu_activated()
        display_search_results.hide()
        search_bar.clear()

    def add_another_plot(self):
        # show / unhide plot
        print('+')

        if self.search_bar1.isHidden():
            self.search_bar1.show()
            self.Csv_dropdown_menu1.show()
            self.graphWidget1.show()
            return
        if self.search_bar2.isHidden():
            self.search_bar2.show()
            self.Csv_dropdown_menu2.show()
            self.graphWidget2.show()
            return
        if self.search_bar3.isHidden():
            self.search_bar3.show()
            self.Csv_dropdown_menu3.show()
            self.graphWidget3.show()
            return
        if self.search_bar4.isHidden():
            self.search_bar4.show()
            self.Csv_dropdown_menu4.show()
            self.graphWidget4.show()
            return

    def remove_plot(self):
        # show / unhide plot
        print('+')
        if not self.search_bar4.isHidden():
            self.search_bar4.hide()
            self.Csv_dropdown_menu4.hide()
            self.graphWidget4.hide()
            return
        if not self.search_bar3.isHidden():
            self.search_bar3.hide()
            self.Csv_dropdown_menu3.hide()
            self.graphWidget3.hide()
            return
        if not self.search_bar2.isHidden():
            self.search_bar2.hide()
            self.Csv_dropdown_menu2.hide()
            self.graphWidget2.hide()
            return
        if not self.search_bar1.isHidden():
            self.search_bar1.hide()
            self.Csv_dropdown_menu1.hide()
            self.graphWidget1.hide()
            return










if __name__ == "__main__":
    app = qtw.QApplication([])
    mw = MainWindow()
    app.setStyle(qtw.QStyleFactory.create('Fusion'))
    app.exec_()
