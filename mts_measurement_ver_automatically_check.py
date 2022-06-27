import py7zr
import os
from os import listdir
from os.path import isfile, join
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
    * use extractor_vers2.cfg configuration
what the script do:
    1. extract new mts_measurement from 7z file. you can put as many 7z files as you wannt in the folder.
    2. Run MTS session
    3. cut new files to the "mts_measurement_7z_folder" with new name.
    4. loop for all files.
"""

mts_measurement_7z_folder = r'C:\MTS_TEST_SCRIPT\MTS_MEAS_VER' #folder with all mts_measurement as 7z format
mts_measurement_original_path = r'C:\MFC520_Cartex\06_Deliverables\MTS' #location of the mts_measurement folder
CONFIG_PATH = r"C:\MTS_TEST_SCRIPT\extractor_vers2.cfg"
recording_path = r"C:\MTS_TEST_SCRIPT\2022.06.07_at_20.48.26_camera-mi_804_truck_with_trailer.rrec"
MTS_DIR = r"C:\CARTICA\MTS_21"


# build path for MTS to reach measapp.exe
mts_path = os.path.join(MTS_DIR, "MTS", "mts_system", "measapp.exe") #add path, not regarding OS system
MTS_CMD = [mts_path, f"-lc{CONFIG_PATH}", f"-lr{recording_path}", "-pal", "-eab", "-silent", "-eoe"]

#get 7z files name from directory:
onlyfiles = [f for f in listdir(mts_measurement_7z_folder) if isfile(join(mts_measurement_7z_folder, f))]
print("all versions list: \n" , onlyfiles)

for onlyfile in onlyfiles:
    # extract new files from 7z folder to destination:
    my_path_file = os.path.join(mts_measurement_7z_folder,onlyfile)
    with py7zr.SevenZipFile(my_path_file,mode='r') as z:
        z.extractall(mts_measurement_original_path )
        print("7z extracted : \n" , my_path_file)

    # run MTS session:
    print("MTS session starts")
    os_utilities.run_cmd(MTS_CMD)
    print("MTS session finish")

    # cut current folder after script finishes:
    source_dir = os.path.join(mts_measurement_original_path ,'mts_measurement')
    destination_dir = os.path.splitext(os.path.join(mts_measurement_7z_folder,onlyfile))[0] + '_copy'

    print("Success, see results at: \n", destination_dir)
    shutil.move(source_dir, destination_dir)











