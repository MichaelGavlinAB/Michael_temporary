from automotive.POCs_Scripts.inference_results_visualisation import inference_results_visualisation
from cartica_services.data_center.data_center import DataCenter
from PyQt5.QtWidgets import  QLabel , QFileDialog,QSizePolicy
from PyQt5.QtGui import QPixmap
import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import pandas as pd
import datetime
import json
import os


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MTS & Mapi analysis platform")
        self.setLayout(qtw.QGridLayout())
        self.myui()
        # self.resize(1500, 1300)
        self.show()
        # List of names, widgets are stored in a dictionary by these keys.
        # print(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))


    def myui(self):

        #define layout containers
        # container = qtw.QWidget()
        tab_container = qtw.QTabWidget()

        container_main = qtw.QWidget()
        container_main.setLayout(qtw.QGridLayout())

        container = qtw.QWidget()
        container.setLayout(qtw.QGridLayout())

        container1 = qtw.QGroupBox()
        container1.setLayout(qtw.QGridLayout())

        container2 = qtw.QGroupBox()
        container2.setLayout(qtw.QGridLayout())

        container3 = qtw.QGroupBox()
        container3.setLayout(qtw.QGridLayout())

        container_side_widgets = qtw.QGroupBox()
        container_side_widgets.setLayout(qtw.QGridLayout())

        container_side_by_side_layout = qtw.QGroupBox()
        container_side_by_side_layout.setLayout(qtw.QGridLayout())

        container4 = qtw.QGroupBox()
        container4.setLayout(qtw.QGridLayout())

        container5 = qtw.QGroupBox()
        container5.setLayout(qtw.QGridLayout())

        container_mapi = qtw.QGroupBox()
        container_mapi.setLayout(qtw.QGridLayout())

        info_tab = qtw.QWidget()
        info_tab.setLayout(qtw.QGridLayout())

        Mapi_tab = qtw.QWidget()
        Mapi_tab.setLayout(qtw.QGridLayout())

        # load preset
        f = open('preset.json')
        preset = json.load(f)



        # labels and display (Qlabel)
        self.label =  QLabel(r"1. Choose CSV file                    ")
        self.label3 = QLabel(r"2. select a folder with images to show")
        self.label4 = QLabel("use this tab to download images from DC and run inference visualisation script\n \n"
                             "  - default values stored in 'preset.json'. \n"
                             "  - delete downloaded sessions when finish to free space. \n"
                             "  - change 'inference_results_visualisation_CFG.json' file to change drawing settings")
        self.label4.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.label5 = QLabel(r"User email                            ")
        self.label6 = QLabel(r"Mapi session name                     ")
        self.label7 = QLabel(r"Download path                         ")
        self.label8 = QLabel(r"Inference results visualisation CFG   ")
        self.label9 = QLabel(r"!! program will be idle while downloading and drawing results, be patient !!")
        self.label9.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.mail = qtw.QLineEdit(preset['user_email'])
        self.download_images_path = qtw.QLineEdit(preset['download_dir'])
        self.mapi_session_name = qtw.QLineEdit()
        self.inference_json_path = qtw.QLineEdit(preset['inference_json_path'])


        self.Time_stamp_display = qtw.QLineEdit()
        self.Time_stamp_display.returnPressed.connect(self.Time_stamp_display_pressed)
        self.Time_stamp_display.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.Time_stamp_display_real_time = qtw.QLabel()
        self.display_search_results = qtw.QListWidget()
        self.display_search_results.itemDoubleClicked.connect(self.display_search_results_clicked)
        self.display_search_results.hide()


        #logo
        self.logo = QPixmap(logo_path)
        self.logo_label = qtw.QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setPixmap(self.logo)


        #text box second tab
        self.info_text_box = qtw.QLabel(text) #dext defined as global in main
        self.info_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.info_text_box_scroll_area = qtw.QScrollArea()
        self.info_text_box_scroll_area.setWidget(self.info_text_box)


        # push Buttons (QPushButton)
        self.btn_open_picture = qtw.QPushButton('open existing images folder', clicked=self.show_picture)
        self.btn_reset_scale = qtw.QPushButton('reset scale', clicked=self.btn_reset_scale)
        self.btn_open_csv = qtw.QPushButton('click here to choose a csv file',clicked =self.QPushButton_clicked)
        self.btn_open_picture2 = qtw.QPushButton('open images folder to compare', clicked=self.show_picture2)
        self.btn_open_picture2.setHidden(1)
        self.next_picture = qtw.QPushButton('-->', clicked=self.next_picture)
        self.previous_picture = qtw.QPushButton('<--', clicked=self.previous_picture)
        self.add_another_picture = qtw.QPushButton('+', clicked=self.hide_unhide_second_picture)
        self.add_another_plot = qtw.QPushButton('add plot', clicked=self.add_another_plot)
        self.add_another_plot.setFixedSize(100,30)
        self.remove_plot = qtw.QPushButton('remove plot', clicked=self.remove_plot)
        self.remove_plot.setFixedSize(100,30)
        self.btn_download_picture = qtw.QPushButton('run', clicked=self.download_images_from_mapi)
        self.btn_download_picture.setStyleSheet("background-color : green")
        self.add_mapi_inference_to_main = qtw.QPushButton('add session to main window', clicked=self.add_mapi_inference_to_main)
        self.add_mapi_inference_to_main.setStyleSheet("background-color : green")
        self.add_mapi_inference_to_main.hide()
        self.btn_download_picture.setMaximumWidth(100)


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
        self.storage_picture_scale.returnPressed.connect(self.storage_picture_scale_pressed)

        # self.Time_stamp_display.returnPressed.connect(self.Time_stamp_display_pressed)
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
        self.picture_frame.setFixedSize(1650,450)
        self.picture_frame2.setHidden(1)
        self.label_image = QLabel() #insert image
        self.label_image2 = QLabel() #insert image

        # slider widget
        self.slider = qtw.QSlider(1) #slider
        self.slider.valueChanged.connect(self.slider_move)


        # dial widget
        self.scale_dial = qtw.QDial()
        self.scale_dial.setMaximum(1200)
        self.scale_dial.setMinimum(200)
        self.scale_dial.setValue(450)
        self.scale_dial.setFixedSize(100,100)
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


        #  size policty
        policy_a = QSizePolicy.Ignored
        policy_b = QSizePolicy.Preferred
        policy_C = QSizePolicy.Expanding

        self.search_bar.setSizePolicy(policy_a,policy_b)
        self.Csv_dropdown_menu.setSizePolicy(policy_a,policy_b)
        self.graphWidget.setSizePolicy(policy_a,policy_C)
        self.search_bar1.setSizePolicy(policy_a,policy_b)
        self.Csv_dropdown_menu1.setSizePolicy(policy_a,policy_b)
        self.graphWidget1.setSizePolicy(policy_a,policy_C)
        self.search_bar2.setSizePolicy(policy_a, policy_b)
        self.Csv_dropdown_menu2.setSizePolicy(policy_a, policy_b)
        self.graphWidget2.setSizePolicy(policy_a, policy_C)
        self.search_bar3.setSizePolicy(policy_a,policy_b)
        self.Csv_dropdown_menu3.setSizePolicy(policy_a,policy_b)
        self.graphWidget3.setSizePolicy(policy_a,policy_C)
        self.search_bar4.setSizePolicy(policy_a,policy_b)
        self.Csv_dropdown_menu4.setSizePolicy(policy_a,policy_b)
        self.graphWidget4.setSizePolicy(policy_a,policy_C)
        self.search_bar5.setSizePolicy(policy_a,policy_b)
        self.Csv_dropdown_menu5.setSizePolicy(policy_a,policy_b)
        self.graphWidget5.setSizePolicy(policy_a,policy_C)


        # adding widgets to main and tab layout
        # container.layout().addWidget(self.logo_label, 0, 0, 1, 1)
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

        container2.layout().addWidget(self.previous_picture, 0, 1, 1, 1)
        container2.layout().addWidget(self.slider, 0, 2, 1, 1)
        container2.layout().addWidget(self.next_picture, 0, 3, 1, 1)

        container_side_widgets.layout().setAlignment(Qt.AlignTop)
        container_side_widgets.layout().addWidget(self.scale_dial, 1, 0, 1, 1)
        container_side_widgets.layout().addWidget(self.storage_picture_scale, 2, 0, 1, 1)
        container_side_widgets.layout().addWidget(self.btn_reset_scale, 3, 0, 1, 1)
        container_side_widgets.layout().addWidget(self.Time_stamp_display_real_time, 4, 0, 1, 1)

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

        container4.layout().addWidget(self.add_another_plot, 0, 6, 1, 1)
        container4.layout().addWidget(self.remove_plot, 3, 6, 1, 1)
        container4.layout().setAlignment(Qt.AlignHCenter)

        container5.layout().addWidget(self.Time_stamp_display_real_time)
        container5.layout().addWidget(self.Time_stamp_display)
        container5.layout().setAlignment(Qt.AlignHCenter)

        # mapi tab layout
        container_mapi.layout().setAlignment(Qt.AlignTop)
        container_mapi.layout().addWidget(self.mail,1,1,1,1)
        container_mapi.layout().addWidget(self.label5 , 1, 0, 1, 1)

        container_mapi.layout().addWidget(self.inference_json_path, 2, 1, 1, 1)
        container_mapi.layout().addWidget(self.label8,2, 0, 1, 1)
        container_mapi.layout().addWidget(self.download_images_path, 3, 1, 1, 1)
        container_mapi.layout().addWidget(self.label7, 3, 0, 1, 1)
        container_mapi.layout().addWidget(self.mapi_session_name, 4, 1, 1, 1)
        container_mapi.layout().addWidget(self.label6, 4, 0, 1, 1)
        container_mapi.layout().addWidget(self.btn_download_picture, 5, 0, 1, 1)
        container_mapi.layout().addWidget(self.label9, 5, 1, 1, 1)
        container_mapi.layout().addWidget(self.add_mapi_inference_to_main, 6, 1, 1, 1)

        # adding containers to tab main layout
        container_main.layout().setAlignment(Qt.AlignTop)
        container_main.layout().addWidget(self.logo_label, 0, 0, 1, 1)
        container_main.layout().addWidget(container,0,1,1,1)
        container_main.layout().addWidget(container1,1,1,1,1)
        container_main.layout().addWidget(container_side_widgets, 1, 0, 1, 1)
        container_main.layout().addWidget(container2,2,1,1,1)
        container_main.layout().addWidget(container3,3,1,1,1)
        container_main.layout().addWidget(container4, 3, 0, 1, 1)
        container_main.layout().addWidget(container5, 2, 0, 1, 1)


        # add widgets to tubs  layouts

        #add to info tab layout
        info_tab.layout().addWidget(self.info_text_box_scroll_area,0,0,1,1)

        #add to mapi tab layout
        Mapi_tab.layout().addWidget(self.label4, 0, 0, 1, 1)
        Mapi_tab.layout().addWidget(container_mapi, 1, 0, 1, 1)


        #adding tab to tab container
        tab_container.addTab(container_main , 'Main')
        tab_container.addTab(Mapi_tab, 'multi API')
        tab_container.addTab(info_tab, 'Info')


        #main layout
        '''
        add to main display -----------------------------------------------------------------------------------
        add to main display -----------------------------------------------------------------------------------
        add to main display -----------------------------------------------------------------------------------
        '''
        self.layout().addWidget(tab_container,0,0,0,0) # <<<


# opens csv file search box
    def QPushButton_clicked(self) :
        '''
        function activated by QPushButton.
        * select csv file
        * add headers to csv dropdown menu
        * store csv path in storage widget
        '''

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

        '''
        get data from csv file and store in a storage widget and plot data + time stamp
        :param Csv_dropdown_menu: qtw.QComboBox
        :param storage: qtw.QLineEdit
        :param storage_CSV_timestamps: qtw.QTextEdit
        :param storage_CSV_data: qtw.QTextEdit
        :param graphWidget: pg.PlotWidget
        '''

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
        print('Csv_dropdown_menu_activated_update_function')
        '''
        get current time stamp , plot it and update image.
        :param dropdown_menu_storage_image_names: self.dropdown_menu_storage_image_names
        :param Time_stamp_display: QLineEdit
        :param graphWidget: self.graphWidget
        :param storage_CSV_data: self.storage_CSV_data
        :return:
        '''

        # get current timestamp from image file name
        current_time_string = dropdown_menu_storage_image_names.currentText()[-20:-4] # get time from dropdown list

        # convert timestamp to float and display time stamp
        if current_time_string.isnumeric():
            current_time = float(current_time_string)
        else:
            current_time = 0
        Time_stamp_display.setText(current_time_string)


        #display time stamps as real time
        first_time_string = self.dropdown_menu_storage_image_names.itemText(0)[-20:-4]
        real_time = (int(current_time_string)-int(first_time_string))/1000000
        self.Time_stamp_display_real_time.setText(str(real_time) + ' [sec]')


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
        print('get_data_from_file')
        '''
        :param path: path to csv file
        :param header: name of the desired contentout of csv file
        :return:
        '''

        # read from csv file and convert to list
        dff = pd.read_csv(path)
        time_stamp = dff[dff.columns[0]].tolist()
        data = dff[header].tolist()
        return time_stamp , data


    def plot_grapth(self,widget,x_data,y_data,clear):
        print('plot_grapth')
        '''
        :param widget: self.graphWidget
        :param x_data: time stamps
        :param y_data: data
        :param clear: clear previous plot ro not. clear = 1 , do not clear =0.
        :return:
        '''

        if clear:
            widget.plot(x_data, y_data , name="data" , clear=True) # plot the data
        else:
            widget.plot(x_data, y_data, name="data")  # plot the data

    def show_picture(self):
        # pop_window = 1 , take path from pop window
        # pop_window = 0 , take path from given path
        pop_window = 1
        path = []
        self.show_picture_function(pop_window,path)

    def show_picture_function(self,pop_window, path):

        print('show_picture')
        '''
        pop window to select folder containing images, store image names in combo list and display first image.
        '''
        #user select path with images
        if pop_window == 1:
            picture_folder_path = QFileDialog.getExistingDirectory(None, 'Select a folder:')
        else:
            picture_folder_path = path

        file_names = os.listdir(picture_folder_path)
        print(file_names)



        file_names.sort()


        #store image names in combo dropdown list
        self.dropdown_menu_storage_image_names.clear()
        for file_name in file_names:
            self.dropdown_menu_storage_image_names.addItem(os.path.join(picture_folder_path,file_name))

        # display first image
        picture_path = os.path.join(picture_folder_path,file_names[0])
        scale = int(self.storage_picture_scale.text())
        self.photo = QPixmap(picture_path).scaledToHeight(scale)
        self.picture_frame_scene.clear()
        self.picture_frame_scene.addPixmap(self.photo)


    def show_picture2(self):
        print('show_picture2')
        '''
        pop window to select folder containing images, store image names in combo list and display second image.
        '''

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
        print('Dropdown_image_activated')
        '''
        update images after dropdown images list activated
        '''

        #update list
        scale = int(self.storage_picture_scale.text())
        self.photo = QPixmap(self.dropdown_menu_storage_image_names.currentText()).scaledToHeight(scale)
        self.picture_frame_scene.clear()
        self.picture_frame_scene.addPixmap(self.photo)

        # update all plots
        self.Csv_dropdown_menu_activated_update()
        self.Csv_dropdown_menu_activated_update1()
        self.Csv_dropdown_menu_activated_update2()
        self.Csv_dropdown_menu_activated_update3()
        self.Csv_dropdown_menu_activated_update4()
        self.Csv_dropdown_menu_activated_update5()


    def Dropdown_image_activated2(self):
        print('Dropdown_image_activated2')
        '''
        update second picture after dropdown image activated
        '''

        #update list
        scale = int(self.storage_picture_scale.text())
        self.photo = QPixmap(self.dropdown_menu_storage_image_names2.currentText()).scaledToHeight(scale)
        self.picture_frame_scene2.clear()
        self.picture_frame_scene2.addPixmap(self.photo)


    def slider_move(self):
        print('slider_move')
        '''
        update images and timestamps after slider moves
        '''

        number_of_items = self.dropdown_menu_storage_image_names.count()
        self.dropdown_menu_storage_image_names.setCurrentIndex(round(self.slider.value() / 100 * number_of_items))
        self.Dropdown_image_activated()
        self.Dropdown_image_activated2()
        print(self.slider.value())


    def next_picture(self):
        print('next_picture')
        '''
        update dropdown image index to next image
        '''

        # update image
        self.dropdown_menu_storage_image_names.setCurrentIndex(self.dropdown_menu_storage_image_names.currentIndex() + 1)
        self.Dropdown_image_activated()
        self.Dropdown_image_activated2()

        self.update_slider(self.dropdown_menu_storage_image_names.currentIndex())


    def previous_picture(self):
        print('previous_picture')
        '''
        update dropdown image index to previous image
        '''

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
        print('string_to_list')
        '''
        translate data stored as list in a string format to list
        :param string_data: str , example - "[123,456]"
        :return: list [123,456]
        '''

        #translate string data to list
        if string_data:
            time_stamps_from_storage = string_data[1:-1].split(',')
            data = [float(i) for i in time_stamps_from_storage]
            return data
        else:
            return []


    def scale_dial_activated(self):
        print('scale_dial_activated')
        '''
        update picture size with new scale stored in widget.
        '''
        # print(self.scale_dial.value())
        self.storage_picture_scale.setText(str(self.scale_dial.value()))
        self.Dropdown_image_activated()
        self.Dropdown_image_activated2()


    def hide_unhide_second_picture(self):
        print('hide_unhide_second_picture')
        '''
        * unhide second image when button pushed.
        * hide second image if it is visible.
        '''

        #add new image
        if self.picture_frame2.isHidden():
            #unhide second image to compare widgets
            self.picture_frame2.setHidden(0)
            self.dropdown_menu_storage_image_names2.setHidden(0)
            self.btn_open_picture2.setHidden(0)
            self.picture_frame.setFixedSize(1700,260)
            self.picture_frame2.setFixedSize(1700,260)
            self.add_another_picture.setText('-')
        else:
            #hide second image to compare widgets
            self.picture_frame2.setHidden(1)
            self.dropdown_menu_storage_image_names2.setHidden(1)
            self.btn_open_picture2.setHidden(1)
            self.picture_frame.setFixedSize(1700,500)
            self.add_another_picture.setText('+')


    def btn_reset_scale(self):
        print('btn_reset_scale')
        '''
        reset scale storage widget
        '''
        self.storage_picture_scale.setText('1000')
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
        print('search_bar_activated_function')
        '''
        lowercase search input and all csv header condent , search for the desired field , display results in a list.
        :param search_bar: QLineEdit
        :param display_search_results: QListWidget
        :param Csv_dropdown_menu: QComboBox

        '''

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
        print('display_search_results_clicked_function')
        '''
        :param Csv_dropdown_menu:  QComboBox
        :param item: clicked item
        :param Csv_dropdown_menu_activated: function
        :param display_search_results: QListWidget
        :param search_bar: QLineEdit
        '''


        #change plot so selected value
        for i in range (Csv_dropdown_menu.count()):
            if Csv_dropdown_menu.itemText(i) == item.text():
                Csv_dropdown_menu.setCurrentIndex(i)

        Csv_dropdown_menu_activated()
        display_search_results.hide()
        search_bar.clear()


    def add_another_plot(self):
        '''
        unhide search bar + csv dropdown + graph widget
        '''


        print('add_another_plot')
        # show / unhide plot
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
        if self.search_bar5.isHidden():
            self.search_bar5.show()
            self.Csv_dropdown_menu5.show()
            self.graphWidget5.show()

            return


    def remove_plot(self):
        print('remove_plot')
        '''
        hide search bar + csv dropdown + graph widget
        '''
        # show / unhide plot
        if not self.search_bar5.isHidden():
            self.search_bar5.hide()
            self.Csv_dropdown_menu5.hide()
            self.graphWidget5.hide()
            return
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


    def update_slider(self , current_item_index):
        '''
        :param current_item_index: index of the desired picture out of all pictures
        :return:
        '''
        number_of_items = self.dropdown_menu_storage_image_names.count()
        self.slider.setValue(current_item_index/number_of_items*100)


    def Time_stamp_display_pressed(self):
        print("Time_stamp_display_pressed")

        #get time stamps from image name out of image dropdown list
        picture_time_stamps = []
        for i in range(self.dropdown_menu_storage_image_names.count()):
            picture_time_stamps.append(int(self.dropdown_menu_storage_image_names.itemText(i)[-20:-4]))
        Time_stamp_display = int(self.Time_stamp_display.text())

        #find requested time stamp in time stamps taken out of picture
        index = 0
        for picture_time_stamp in picture_time_stamps:
            if abs(Time_stamp_display) == picture_time_stamp:
                print("time stamp found", picture_time_stamp)
                if not self.dropdown_menu_storage_image_names2.isHidden():
                    self.dropdown_menu_storage_image_names.setCurrentIndex(index)
                    self.dropdown_menu_storage_image_names2.setCurrentIndex(index)
                    self.Dropdown_image_activated()
                    self.Dropdown_image_activated2()
                    self.update_slider(index)
                else:
                    self.dropdown_menu_storage_image_names.setCurrentIndex(index)
                    self.Dropdown_image_activated()
                    self.update_slider(index)
            index += 1
            print(index)


    def storage_picture_scale_pressed(self):
        '''
        update picture size if scale changed manually using text
        '''
        self.Dropdown_image_activated()
        self.Dropdown_image_activated2()


        # time_stamps_from_storage = self.string_to_list(self.storage_CSV_timestamps.toPlainText())# get data from dropdown list
        # print(time_stamps_from_storage)

    def download_images_from_mapi(self):
        '''
        download images out of dc and draw visual markers
        '''

        self.btn_download_picture.setStyleSheet("background-color : yellow")
        dc = DataCenter(user_email=self.mail.text(), allow_load_from_cache=False)
        # base_path = '/home/michael/git/Michael_temporary_git/gui_development/download_images'
        # session_name = 'CBLA_ens169_v0_53_121_equal_league_city'
        # config_path = r'/home/michael/git/automotive/src/python/automotive/POCs_Scripts/mts_mapi_analysis_platform/inference_results_visualisation_CFG.json'
        base_path = self.download_images_path.text()
        session_name = self.mapi_session_name.text()
        config_path = self.inference_json_path.text()

        time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        output_dir = f'{base_path}/{session_name + "_" +  time}'

        #run main inference script (eric script)
        inference_results_visualisation.process_images(session_name, output_dir, config_path)
        results_name = self.get_results_path(output_dir)

        #search for 'results' string in folder names and add to label
        for result_name in results_name:
            if 'results' in result_name:
                print('results: ', result_name)
                result_dir = os.path.join(output_dir,result_name)
                self.label9.setText(result_dir)
                self.add_mapi_inference_to_main.show()
                return


    def get_results_path(self, output_dir):
        '''
        get path as str
        return: containing folder names as [str]
        '''

        # finds only directories in path
        results_path = []
        if os.path.isdir(output_dir):
            for file in os.listdir(output_dir):
                my_list = os.path.join(output_dir, file)
                if os.path.isdir(my_list):
                    results_path.append(my_list)

        results_name = []
        for result_path in results_path:
            results_name.append(os.path.basename(os.path.normpath(result_path)))

        return results_name

    def add_mapi_inference_to_main(self):
        self.show_picture_function(0, self.label9.text())
        self.add_mapi_inference_to_main.setStyleSheet("background-color : yellow")
        self.add_mapi_inference_to_main.setText('done')

        print('add_mapi_inference_to_main')



if __name__ == "__main__":

    #read text from file mto form manual
    text_path = 'text.txt'
    logo_path = 'logo.png'
    with open(text_path) as f:
        lines = f.readlines()
    text = ' '.join(lines) #uses as global info
    text = 'info file path: ' + text_path + '\n\n' + text

    app = qtw.QApplication([])
    mw = MainWindow()
    app.setStyle(qtw.QStyleFactory.create('Fusion'))
    app.exec_()
