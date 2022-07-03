import py7zr
import os
from os import listdir
from os.path import isfile, join
from os import path
import shutil
from cartica_utilities.utilities import os_utilities , logging_utilities
import glob
from csv import writer
import subprocess
import traceback
# import datetime
import time



import csv

"""
script purpose:
    check a recc file for errors using different mts_measurement versions that
    stored in the folder as 7z format, automatically.
    all results are stored at "mts_measurement_7z_folder" path as folders.
notes:
    * Path "mts_measurement_7z_folder" shall contain only 7z files.
    * recording_pathes is a list and can contain as many rrec files as you want.

what the script does:
    1. Delete the existing mts_measurement folder.
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
mts_measurement_7z_folder = r'C:\MTS_TEST_SCRIPT\MTS_MEAS_VER'  # folder with all mts_measurement as 7z format
what_to_find1 = "No matching reader plugin"
what_to_find2 = "Recording corrupted"
what_to_find3 = "corrupted"
FILE_NOT_RECORDING_ERROR = "No matching reader plugin found for file"
RECORDING_CORRUPTED_ERROR = "Recording corrupted"
dir_csv = r"C:\MTS_TEST_SCRIPT"
csv_name = "results" #without .csv
recording_pathes = [
                    r"Z:\2022.06.14_at_13.50.01_camera-mi_804_0_45m\2022.06.14_at_13.50.01_camera-mi_804_0_45m.rrec",
                    r"Z:\2022.06.14_at_13.39.41_camera-mi_804_0_10m\2022.06.14_at_13.39.41_camera-mi_804_0_10m.rrec",
                    r"Z:\2022.06.14_at_13.37.16_camera-mi_804_0_5m\2022.06.14_at_13.37.16_camera-mi_804_0_5m.rrec",
                    r"Z:\2022.06.14_at_10.57.35_camera-mi_804_15m\2022.06.14_at_10.57.35_camera-mi_804_15m.rrec",
                    r"Z:\2022.06.14_at_11.23.02_camera-mi_804_35m\2022.06.14_at_11.23.02_camera-mi_804_35m.rrec",
                    r"Z:\2022.06.14_at_13.44.00_camera-mi_804_0_20m\2022.06.14_at_13.44.00_camera-mi_804_0_20m.rrec",
                    r"Z:\2022.06.14_at_11.15.28_camera-mi_804_25m\2022.06.14_at_11.15.28_camera-mi_804_25m.rrec",
                    r"Z:\2022.06.14_at_14.07.18_camera-mi_804_0_15m\2022.06.14_at_14.07.18_camera-mi_804_0_15m.rrec",
                    r"Z:\2022.06.14_at_14.06.06_camera-mi_804_0_20m\2022.06.14_at_14.06.06_camera-mi_804_0_20m.rrec",
                    ]

def validate_recording_file(MTS_CMD,log_dir) -> bool:
    # possible fix
    # os_utilities.delete_path(log_dir)

    timeout_secs = max(int(os.path.getsize(recording_path) / 5000000) * 2, 60)
    # mts_path = os.path.join(MTS_DIR, "MTS", "mts_system", "measapp.exe")
    # MTS_CMD = [mts_path, f"-lc{CONFIG_PATH}", f"-lr{recording_path}", "-pal", "-eab", "-silent", "-eoe"]

    try:
        process = subprocess.Popen(MTS_CMD)
        try:
            outs, errs = process.communicate(timeout=timeout_secs)
        except subprocess.TimeoutExpired:
            logging_utilities.LOGGER.warning("Timeout expired. Killing process...")
            process.kill()
            raise TimeoutError("MTS timeout expired")

        # get log files, sorted alphabetically
        log_files = os_utilities.get_file_paths(log_dir, [".xlog"])
        if not log_files:
            raise FileNotFoundError(f"Cannot find MTS logs in {log_dir}")

        # first log file is the latest one
        with open(log_files[0], 'r') as log_stream:
            for line in log_stream.readlines():
                if FILE_NOT_RECORDING_ERROR in line:
                    raise RuntimeError("File is not a recording")
                elif RECORDING_CORRUPTED_ERROR in line:
                    raise RuntimeError("Recording is corrupted")

        # delete all logs
        # for file in log_files:
        #     os_utilities.delete_path(file)
    except Exception as e:
        for line in traceback.format_exc().split("\n"):
            print(line)
        return False
    return True

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
    # CSV initialize:
    csv_writer(dir_csv, csv_name,
               ["Date-time", "mts_measurement_version", "rrec", "str to find 1" , "str to find 2", "str to find 3", "MTS_RESULT"])
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
            # os_utilities.run_cmd(MTS_CMD)
            log_dir = os.path.join(mts_measurement_original_path, 'mts_measurement', "log")
            MTS_RESULT = validate_recording_file(MTS_CMD,log_dir)
            print("--- MTS session finish")
            print("---MTS session result return:",MTS_RESULT)

            # search for string in xlog file:
            cwd = os.getcwd()
            os.chdir(delete_path)
            for filee in glob.glob("*.xlog"):
                print("xlog file name: \n", filee)
                result1 = search_str(filee, what_to_find1)
                result2 =search_str(filee, what_to_find2)
                result3 = search_str(filee, what_to_find3)
            os.chdir(cwd)

            # write to csv
            print("--- write to CSV file")
            csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"), onlyfile,recording_path,result1,result2,result3,MTS_RESULT])

            # cut current folder after script finishes:
            source_dir = os.path.join(mts_measurement_original_path, 'mts_measurement','log')
            destination_dir = os.path.splitext(os.path.join(mts_measurement_7z_folder, onlyfile))[0] + '_copy' + str(time.strftime("%Y%m%d-%H%M%S"))


            try:
                shutil.move(source_dir, destination_dir)
                print("--- Success, see results at: \n", destination_dir)
            except OSError as e:
                print("Error while moving results : %s : %s" % (source_dir, e.strerror))

