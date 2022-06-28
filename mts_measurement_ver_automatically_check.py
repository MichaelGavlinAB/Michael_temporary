import py7zr
import os
from os import listdir
from os.path import isfile, join
from os import path
import shutil
from cartica_utilities.utilities import os_utilities

"""
script purpose:
    check a recc file for errors using different mts_measurement versions that
    stored in folder as 7z format, automatically one by one.
    all results are stored at "mts_measurement_7z_folder" path as folders.

notes:
    * Folder "mts_measurement_7z_folder" shall contain only 7z files.
    * first delete mts_measurement from origin path.
    * use recording_validator configuration
what the script do:
    1. Delete existing mts_measurement folder (works only sometimes, windows permissions error)
    2. Extract new mts_measurement from 7z file. you can put as many 7z files as you want in the folder.
    3  Delete log folder
    4. Run MTS session
    5. cut new files to the "mts_measurement_7z_folder" with new name.
"""

mts_measurement_original_path = r"C:\MFC520_Cartex\MTS\05_Testing\MTS" #folder containing the mts_measurement
measapp_path = r"C:\MFC520_Cartex\MTS\05_Testing\MTS\mts_system\measapp.exe" #verify it is the same folder as mts_measurement_original_path
CONFIG_PATH = r"C:\MTS_TEST_SCRIPT\recording_validator.cfg"
recording_path = r"C:\MTS_TEST_SCRIPT\2022.06.07_at_20.48.26_camera-mi_804_truck_with_trailer.rrec"
mts_measurement_7z_folder = r'C:\MTS_TEST_SCRIPT\MTS_MEAS_VER' #folder with all mts_measurement as 7z format

#config
MTS_CMD = [measapp_path, f"-lc{CONFIG_PATH}", f"-lr{recording_path}", "-pal", "-eab", "-silent"]

#get 7z files name from directory:
onlyfiles = [f for f in listdir(mts_measurement_7z_folder) if isfile(join(mts_measurement_7z_folder, f))]
print("All versions list: \n", onlyfiles)

# Delete existing mts_measurement folder:
delete_path = os.path.join(mts_measurement_original_path, 'mts_measurement')
if str(path.exists(delete_path)) == True:
    try:
        shutil.rmtree(delete_path)
    except OSError as e:
        print("Error while delete : %s : %s" % (delete_path, e.strerror))

for onlyfile in onlyfiles:
    print("-----------------------------------------------------------------------------")

    # extract new files from 7z folder to destination:
    my_path_file = os.path.join(mts_measurement_7z_folder,onlyfile)
    print("--- Extracting 7z file: \n",my_path_file )
    print("To: \n", mts_measurement_original_path )
    with py7zr.SevenZipFile(my_path_file, mode='r') as z:
        z.extractall(mts_measurement_original_path )
        print("--- 7z extracted : \n", my_path_file)

    # Delete log folder:
    print("--- deleting log folder")
    delete_path = os.path.join(mts_measurement_original_path, 'mts_measurement',"log")
    try:
        shutil.rmtree(delete_path)
    except OSError as e:
        print("Error while delete : %s : %s" % (delete_path, e.strerror))

    # run MTS session:
    print("--- MTS session starts")
    os_utilities.run_cmd(MTS_CMD)
    print("--- MTS session finish")

    # cut current folder after script finishes:
    source_dir = os.path.join(mts_measurement_original_path ,'mts_measurement')
    destination_dir = os.path.splitext(os.path.join(mts_measurement_7z_folder,onlyfile))[0] + '_copy'

    print("--- Success, see results at: \n", destination_dir)
    shutil.move(source_dir, destination_dir)











