import py7zr
import os
from os import listdir
from os.path import isfile, join
from os import path
import shutil
from cartica_utilities.utilities import os_utilities
import glob
from csv import writer
import csv

"""
script purpose:
    check a recc file for errors using different mts_measurement versions that
    stored in folder as 7z format, automatically.
    all results are stored at "mts_measurement_7z_folder" path as folders.
notes:
    * Path "mts_measurement_7z_folder" shall contain only 7z files.
    * recording_pathes is a list and can contain as many rrec files as you want.

what the script do:
    1. Delete existing mts_measurement folder.
    2. Extract new mts_measurement from 7z file. you can put as many 7z files as you want in the folder.
    3  Delete log folder.
    4. Run MTS session.
    5. search for a specific string in the xlog file.
    6. record results in csv file
    7. cut the log files folder to a new destination for further analysis.
"""

mts_measurement_original_path = r"C:\MFC520_Cartex\MTS\05_Testing\MTS"  # folder containing the mts_measurement
measapp_path = r"C:\MFC520_Cartex\MTS\05_Testing\MTS\mts_system\measapp.exe"
CONFIG_PATH = r"C:\MTS_TEST_SCRIPT\recording_validator.cfg"
recording_pathes = [r"Z:\2022.06.23_at_08.45.13_camera-mi_524\2022.06.23_at_08.45.13_camera-mi_524.rrec",
                    r"C:\MTS_TEST_SCRIPT\2022.06.07_at_20.48.26_camera-mi_804_truck_with_trailer.rrec",
                    r"Z:\2021.01.27_at_14.49.37_camera-mi_5022\2021.01.27_at_14.49.37_camera-mi_5022.rrec",
                    r"Z:\2022.06.23_at_08.45.13_camera-mi_524\2022.06.23_at_08.45.13_camera-mi_524.rrec",
                    r"Z:\2022.06.23_at_08.44.02_camera-mi_524\2022.06.23_at_08.44.02_camera-mi_524.rrec",
                    r"Z:\2022.06.23_at_08.42.47_camera-mi_524\2022.06.23_at_08.42.47_camera-mi_524.rrec",
                    r"Z:\2022.06.23_at_08.44.02_camera-mi_524\2022.06.23_at_08.44.02_camera-mi_524.rrec",
                    r"Z:\2020.10.26_at_07.11.14_camera-mi_244_ext_00.06.03.369.855_00.08.12.136.173\2020.10.26_at_07.11.14_camera-mi_244_ext_00.06.03.369.855_00.08.12.136.173.rrec",
                    ]
mts_measurement_7z_folder = r'C:\MTS_TEST_SCRIPT\MTS_MEAS_VER'  # folder with all mts_measurement as 7z format
what_to_find1 = "FILE_NOT_RECORDING_ERROR"
what_to_find2 = "RECORDING_CORRUPTED_ERROR"
dir_csv = r"C:\MTS_TEST_SCRIPT"
csv_name = "results" #without .csv


def csv_writer(dir_csv,csv_name,list_data):
    CSV_path = os.path.join(dir_csv, csv_name) + ".csv"
    with open(CSV_path, 'a', newline='') as f_object:
        # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(list_data)
        # Close the file object
        f_object.close()

def search_str(file_path, word):
    with open(file_path, 'r') as file:
        # read all content of a file
        content = file.read()
        # check if string present in a file
        if word in content:
            print('string : %s  exist' % word)
            return 'exist'
        else:
            print('string : %s does not exist' % word)
            return 'not exist'

if __name__ == '__main__':
    ii = 1
    for recording_path in recording_pathes:
        print("************************************************** \n start session for: \n", recording_path , "\n*****************************************************" )
        # config
        MTS_CMD = [measapp_path, f"-lc{CONFIG_PATH}", f"-lr{recording_path}", "-pal", "-eab", "-silent", "-eoe"]

        # get 7z files name from directory:
        onlyfiles = [f for f in listdir(mts_measurement_7z_folder) if isfile(join(mts_measurement_7z_folder, f))]
        print(" MTS versions list: \n", onlyfiles)

        for onlyfile in onlyfiles:
            # Delete existing mts_measurement folder:
            delete_path = os.path.join(mts_measurement_original_path, 'mts_measurement')
            if os.path.exists(delete_path):
                print("mts_measurement folder exist")
                os.system('rmdir /S /Q "{}"'.format(delete_path))
            else:
                print("mts_measurement folder do not exist")

            print("----------------------------loop start for this rrec file-------------------------------------------------")
            # extract new files from 7z folder to destination:
            my_path_file = os.path.join(mts_measurement_7z_folder, onlyfile)
            print("--- Extracting 7z file: \n", my_path_file)
            print("To: \n", mts_measurement_original_path)
            with py7zr.SevenZipFile(my_path_file, mode='r') as z:
                z.extractall(mts_measurement_original_path)
                print("--- 7z extracted : \n", my_path_file)

            # Delete log folder:
            print("--- deleting log folder")
            delete_path = os.path.join(mts_measurement_original_path, 'mts_measurement', "log")
            try:
                shutil.rmtree(delete_path)
            except OSError as e:
                print("Error while delete log : %s : %s" % (delete_path, e.strerror))

            # run MTS session:
            print("--- MTS session starts")
            os_utilities.run_cmd(MTS_CMD)
            print("--- MTS session finish")

            # search for string in xlog file:
            cwd = os.getcwd()
            os.chdir(delete_path)
            for filee in glob.glob("*.xlog"):
                print("xlog file name: \n", filee)
                result1 = search_str(filee, what_to_find1)
                result2 =search_str(filee, what_to_find2)
            os.chdir(cwd)

            # write to csv
            print("--- write to CSV file")
            csv_writer(dir_csv, csv_name, [onlyfile,recording_path,result1,result2])

            # cut current folder after script finishes:
            source_dir = os.path.join(mts_measurement_original_path, 'mts_measurement','log')
            destination_dir = os.path.splitext(os.path.join(mts_measurement_7z_folder, onlyfile))[0] + '_copy' + str(ii)

            try:
                shutil.move(source_dir, destination_dir)
                print("--- Success, see results at: \n", destination_dir)
            except OSError as e:
                print("Error while moving results : %s : %s" % (source_dir, e.strerror))
        ii = ii + 1


