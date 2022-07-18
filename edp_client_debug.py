import os
import time
import shutil
import datetime
import tempfile
import traceback
import subprocess
from threading import Thread
from multiprocessing import Value, Lock
from werkzeug.exceptions import HTTPException
from flask import Flask, request, send_file, json
import time
import csv
from csv import writer
from cartica_services.data_center import data_center
from cartica_utilities.utilities import os_utilities, logging_utilities, compression_utilities




app = Flask(__name__)
lock = Lock()

ACCEPTABLE_SUFFIXES = {".csv", ".bsig", ".avi"}
MTS_DIR = r"C:\MFC520_Cartex\MTS\05_Testing\MTS"
BURN_IMG_CMD = r"python -u C:\MFC520_Cartex\06_Deliverables\DPUEDP\client\python\edp_control.py --bootelf {} --numberA53Cores 2 --timeout 60"
CONFIG_MTS_CMD = r'python2 C:\MFC520_Cartex\MTS\05_Testing\MTS\mts_measurement\cfg\00_Projects\MFC520\JOINT\jointsim.pyw -g -m "Triggered" -s ACAL:{} -s CB:MEAS -s CHIPS:EDP -s ISP:EDP -s EM:MEAS -s FCT_SEN:SIM -s FCT_VEH:SIM -s GEOS:SIM -s GRAPPA:EDP -s HLA:MEAS -s LCF_SEN:SIM -s LCF_VEH:SIM -s LD:MEAS -s LSD:SIM -s PC:MEAS -s PFC:SIM -s RUM2:MEAS -s SR:EDP -s TSA:SIM -s VDY:MEAS -n'
RUN_MTS_CMD = r"{MTS_DIR}\mts_system\measapp.exe -lc{{}} -lr{{}} -pal -eab -silent -eox".format(MTS_DIR=MTS_DIR)
COM_SERVER_PATH = "C:\\MFC520_Cartex\\06_Deliverables\\DPUEDP\\comserver"
EDP_CONTROL_PATH = "C:\\MFC520_Cartex\\06_Deliverables\\DPUEDP\\client\\python"
FTP_PREFIX_CONVERTION = data_center.FTP_PREFIX + "/Recordings"
CONFIG_PATHS = {
    "meas": r"X:\MTS_CONFIGS\full_meas.cfg",
    "sim": r"X:\MTS_CONFIGS\full_sim.cfg",
    "eba_sim": r"X:\MTS_CONFIGS\extractor_vers2.cfg",
    "eba_sim_hpc": r"X:\MTS_CONFIGS\extractor_vers2_hpc.cfg",
    "old_eba_sim": r"X:\MTS_CONFIGS\extractor_vers3.cfg",
    "ncap_sim": r"X:\MTS_CONFIGS\NCAP_EBA_CONFIG.cfg",      # for open-loop   -> use SIM
    "ncap_meas": r"X:\MTS_CONFIGS\NCAP_EBA_CONFIG.cfg",     # for closed loop -> use MEAS
    "visual_experience_meas": r"X:\MTS_CONFIGS\VISUAL_EXPERIENCE_MEAS.cfg",
    "jointsim": r"X:\MTS_CONFIGS\jointsim.cfg",
    "vacc_sim": r"X:\MTS_CONFIGS\VACC_SIM_CONFIG.cfg",
    "vacc_meas": r"X:\MTS_CONFIGS\VACC_MEAS_CONFIG.cfg",
}
COM_SERVER_PROCESS = None

dir_csv = r"C:\Users\EDP_Station_1\Desktop\git\Cartica-Services\cartica_services\multi_api\runners"
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



def _update_configs():
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"_update_configs"])
    for path in os_utilities.get_file_paths(r"X:\MTS_CONFIGS"):
        CONFIG_PATHS[os.path.basename(path).lower()[:-4]] = path
    logging_utilities.LOGGER.info("Can use configs:")
    for k, v in CONFIG_PATHS.items():
        logging_utilities.LOGGER.info(f"{k.rjust(50)}: {v}")


@app.errorhandler(HTTPException)
def handle_exception(e):
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"handle_exception"])
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


def convert_ftp_path_to_samba(ftp_path: str) -> str:
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"convert_ftp_path_to_samba"])
    """ converts FTP path to SMB path """
    return ftp_path.replace(FTP_PREFIX_CONVERTION, "Y:", 1)


def kill_mts() -> int:
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"kill_mts"])
    return os_utilities.run_cmd("taskkill /f /im measapp.exe /t")


def verify_com_server_online(logger, com_server_running: bool = None) -> bool:
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"verify_com_server_online"])
    """ tests that COM Server is running """
    def run_check_output(order) -> bool:
        line = "schtasks /{} /tn run_conti_COMServer"
        p = subprocess.Popen(line.format(order), stdout=subprocess.PIPE)
        p.wait()
        output = p.communicate()[0].decode()
        worked = (p.poll() == 0) if order != "query" else "Running" in output
        return worked

    retry_counter = 3
    com_server_running = run_check_output("query") if com_server_running is None else com_server_running
    logger.write(f"COM Server running? {com_server_running}\n")
    while not com_server_running and retry_counter > 0:
        logger.write(f"Trying to start COM SERVER... retries left: {retry_counter}\n")
        run_check_output("end")
        time.sleep(5)       # wait 5 seconds to make sure COM server has closed all open resources
        run_check_output("run")
        time.sleep(120)     # wait 120 seconds to make sure COM server is online (timeout from Conti's wrapper)
        com_server_running = run_check_output("query")
        retry_counter -= 1
    return com_server_running


def powercycle_edp(logger) -> int:
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"powercycle_edp"])
    powercycle_cmd = r"python -u edp_control.py --powercycle"
    logger.write("Powercycling EDP...\n")
    rc = os_utilities.run_cmd(powercycle_cmd, timeout=60, stdout=logger, cwd=EDP_CONTROL_PATH)  # 60 seconds to powercycle the EDP
    time.sleep(10)       # 10 seconds after powercycle for clean startup
    return rc == 0


def run_process(cmd, log_file) -> bool:
    """ runs a cmd """
    t1 = datetime.datetime.now()
    log_file.write(f"Running Command: {cmd}\n")
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"run_process","runs a cmd and write to log file",cmd])
    rc = os_utilities.run_cmd(cmd, timeout=65, shell=True, stdout=log_file, stderr=log_file)
    if rc != 0:
        log_file.write(f"WARNING: Run command failed with ERROR CODE {rc}\n")
        csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"), r"WARNING: Run command failed with ERROR CODE"])
    t2 = datetime.datetime.now()
    log_file.write(f"Command runtime: {t2 - t1}\n")
    time.sleep(5)       # 5 seconds - time to close correctly
    return rc == 0


def run_mts_process(log_file, recording_path, rrec_name, config_path):
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"run_mts_process",rrec_name])
    run_mts_cmd = RUN_MTS_CMD.format(config_path, recording_path)
    _rrec_size = os.stat(recording_path).st_size
    _timeout_secs = int(_rrec_size / 5000000) * 3
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"), r"_timeout_secs set to:", _timeout_secs])
    _csv_size = Value('i', -1)
    rc = -1

    # clear the MTS data dir
    os_utilities.delete_path(get_mts_data_dir())
    os.makedirs(get_mts_data_dir())

    t1 = datetime.datetime.now()
    log_file.write(f"Running Command: {run_mts_cmd}\n")
    with subprocess.Popen(run_mts_cmd, shell=True, stdout=log_file, stderr=log_file) as _process:
        _thread = Thread(target=_verify_mts_running, args=(rrec_name, _csv_size))
        _thread.start()
        try:
            _thread.join()
            if _csv_size.value == 0:
                log_file.write("MTS didn't load recording\n")
                csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"), r"MTS did not create CSVs"])
                raise RuntimeError("MTS did not create CSVs")
            _process.communicate(None, timeout=_timeout_secs)
        except subprocess.TimeoutExpired:
            _process.communicate()
            _process.kill()
            csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"), r"Run process timed out"])
            raise RuntimeError("Run process timed out")
        except Exception:
            _process.kill()
            _process.wait()
            raise
        rc = _process.returncode
    t2 = datetime.datetime.now()
    if rc != 0:
        log_file.write(f"WARNING: Run command failed with ERROR CODE {rc}\n")
    log_file.write(f"Command runtime: {t2 - t1}\n")
    kill_mts()  # Kill MTS
    return rc


def get_mts_data_dir() -> str:
    return os.path.join(MTS_DIR, "mts_measurement", "data")


def get_results(recording_name: str, log_path: str = None, config_path: str = None, log_file=None) -> str:
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"get_results",recording_name])
    data_path = get_mts_data_dir()
    related_files = [os.path.join(data_path, f) for f in os.listdir(data_path) if recording_name in f and any(f.endswith(suffix) for suffix in ACCEPTABLE_SUFFIXES)]
    if config_path:
        csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"), "copy mts_config.cfg"])
        shutil.copy(config_path, os.path.join(data_path, "mts_config.cfg"))
        related_files.append(os.path.join(data_path, "mts_config.cfg"))
    if log_path:
        if log_file:
            log_file.write(f"Logging Files {related_files}\n")
            log_file.close()
        os.rename(log_path, os.path.join(data_path, "log.txt"))
        related_files.append(os.path.join(data_path, "log.txt"))
    return related_files


def get_log_file():
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"get_log_file"])
    name_prefix = ""
    log_created = False
    while not log_created:
        try:
            log_path = os.path.join(os.getcwd(), 'log.txt')
            if os.path.isfile(log_path):
                os.remove(log_path)
            log_created = True
        except PermissionError:
            name_prefix += "_"
    log_file = open(log_path, 'w+')
    return log_file, log_path


def _burn_elf_file_to_edp(mts_measurement, elf, log_file):
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"_burn_elf_file_to_edp"])
    log_file.write(f"mts_measurement: {mts_measurement}\n")
    log_file.write(f"elf: {elf}\n")
    if not mts_measurement.filename:
        raise FileNotFoundError("Could not find mts_measurements in request")
    if not elf.filename:
        raise FileNotFoundError("Could not find elf in request")

    kill_mts()  # Kill MTS

    with tempfile.TemporaryDirectory() as temp_dir:
        # save mts_measurements dir
        mts_measurements_zip_path = os.path.join(temp_dir, "mts_measurement.zip")
        csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"), f"Saving mts_measurements"])
        log_file.write(f"Saving mts_measurements to {mts_measurements_zip_path}...\n")
        mts_measurement.save(mts_measurements_zip_path)
        mts_measurement_path = os.path.join(MTS_DIR, "mts_measurement")
        os_utilities.delete_path(mts_measurement_path)

        # uncompress zip file
        log_file.write(f"Uncompressing mts_measurement.zip to {mts_measurement_path}...\n")
        csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"), f"Uncompressing mts_measurement.zip"])
        compression_utilities.uncompress_zip_to_path(mts_measurements_zip_path, temp_dir)
        shutil.copytree(os.path.join(temp_dir, "mts_measurement"), os.path.join(MTS_DIR, "mts_measurement"))

        # save elf file
        elf_path = os.path.join(temp_dir, "mfc520edp_dpu.elf")
        log_file.write(f"Saving elf to {elf_path}...\n")
        elf.save(elf_path)
        log_file.write("Burning elf to EDP...\n")

        # burn image to EDP
        burn_image_cmd = BURN_IMG_CMD.format(elf_path)
        rc = False
        retries = 3
        while retries > 0 and not rc:
            retries -= 1

            # verify that EDP is ready to receive commands
            if not verify_com_server_online(log_file):
                log_file.write("COM Server not running. Run aborted\n")
                return False
            if not powercycle_edp(log_file):
                raise RuntimeError("Failed to powercycle EDP")

            rc = run_process(burn_image_cmd, log_file)
            if not rc:
                log_file.write(f"Burn image has failed. retries left: {retries}\n")
                if retries == 0:
                    log_file.write("Ran out of retries. Aborting...\n")
    return 200 if rc else 400


@app.route("/burn", methods=["POST"])
def burn():
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"burn"])
    status_code = 500
    # create assets
    try:
        log_file, log_path = get_log_file()
        mts_measurement = request.files.get('mts_measurement')
        elf = request.files.get('elf')
    except Exception as e:
        error_msg = "\n".join([f"Failed to Prepare to Burn: {e}", traceback.format_exc().split("\n")])
        return error_msg, status_code

    try:
        retry_counter = 3
        while retry_counter > 0 and status_code != 200:
            try:
                status_code = _burn_elf_file_to_edp(mts_measurement, elf, log_file)
            except Exception as e:
                log_file.write(f"Failed to Burn: (attempt {2 - retry_counter}) {e}\n")
                for line in traceback.format_exc().splitlines():
                    if not line.endswith("\n"):
                        line += "\n"
                    log_file.write(line)
                retry_counter -= 1
                log_file.write("\n\n\n")
    except Exception as e:
        log_file.write(f"Failed to run: {e}\n")
        for line in traceback.format_exc().splitlines():
            if not line.endswith("\n"):
                line += "\n"
            log_file.write(line)
        status_code = 400
    finally:
        log_file.close()
    return send_file(log_path), status_code


def _verify_mts_running(_rrec_name, _size):
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"_verify_mts_running"])
    retries = 100
    while retries > 0:
        time.sleep(3)
        try:
            _csvs = get_results(_rrec_name)
            if len(_csvs) == 0:
                raise FileNotFoundError
            _size.value = len(_csvs)
            break
        except FileNotFoundError:
            _size.value = 0
        retries -= 1


def _run(set_id: str, use_config: str, log_path: str, log_file):
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"_run"])
    dc = data_center.DataCenter("read_only_bot@cartica.ai", allow_load_from_cache=False)
    [dataset] = dc.get_sets([set_id])
    rrec_name = dataset.name_3rd_party.replace(".rrec", "")
    recording_path = convert_ftp_path_to_samba(dc.get_recording_url_from_set(dataset, False))
    log_file.write(f"Running on recording (ID: {set_id}) {rrec_name}\n")
    config_path = CONFIG_PATHS[use_config]
    log_file.write(f"Using Config: {config_path}\n")


    # Kill MTS
    kill_mts()

    # Configure where to load ACAL from
    if "sim" in use_config:
        log_file.write("Detected SIM config -> Configurating ACAL to load from SIM\n")
        run_process(CONFIG_MTS_CMD.format("sim"), log_file)
    else:
        log_file.write("Detected MEAS config -> Configurating ACAL to load from MEAS\n")
        run_process(CONFIG_MTS_CMD.format("meas"), log_file)

    # run MTS process
    run_mts_process(log_file, recording_path, rrec_name, config_path)
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"), "run_mts_process","log_file:",log_file,"recording_path:",recording_path,"rrec_name:",rrec_name,"config_path:",config_path])

    # compress results
    zip_name = os.path.join(os.getcwd(), rrec_name + ".zip")
    output_files = get_results(rrec_name, log_path, config_path, log_file)
    compression_utilities.compress_paths_to_zip(output_files, zip_name)
    for path in output_files:
        os_utilities.delete_path(path)
    status_code = 200  # todo: debug... if rc else 400
    return send_file(zip_name, mimetype='zip', as_attachment=True, attachment_filename=f'{rrec_name}.zip'), status_code


@app.route("/run", methods=["GET"])
def run():
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"run"])
    log_file, log_path = get_log_file()
    set_id = request.args.get("set_id", "")
    use_config = request.args.get("mts_config", "sim")
    log_file.write(f"Looking for recording with set ID: [{set_id}]\n")
    try:
        return _run(set_id, use_config, log_path, log_file)
    except Exception as e:
        log_file.write(f"Failed to run: {e}")
        for line in traceback.format_exc().splitlines():
            if not line.endswith("\n"):
                line += "\n"
            log_file.write(line)
        log_file.close()
        zip_name = os.path.join(os.getcwd(), "error" + ".zip")
        compression_utilities.compress_paths_to_zip([log_path], zip_name)
        status_code = 400
        return send_file(zip_name, mimetype='zip', as_attachment=True, attachment_filename='error.zip'), status_code


@app.route("/cleanup_output", methods=["GET"])
def cleanup_output():
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"cleanup_output"])
    set_id = request.args.get("set_id", "")
    dc = data_center.DataCenter("read_only_bot@cartica.ai", allow_load_from_cache=False)
    [dataset] = dc.get_sets([set_id])
    rrec_name = dataset.name_3rd_party.replace(".rrec", "")
    zip_name = os.path.join(os.getcwd(), rrec_name + ".zip")
    os_utilities.delete_path(zip_name)
    return "OK", 200


@app.route("/restart_com_server", methods=["POST"])
def restart_com_server():
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"restart_com_server"])
    status_code = 500
    try:
        log_file, log_path = get_log_file()
        verify_com_server_online(log_file, False)
    except Exception as e:
        error_msg = "\n".join([f"Failed to Prepare to Burn: {e}", traceback.format_exc().split("\n")])
        return error_msg, status_code
    return send_file(log_path), 200


@app.route("/all")
def all():
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"all"])
    burn()
    return run()


if __name__ == "__main__":
    csv_writer(dir_csv, csv_name, [time.strftime("%Y%m%d-%H%M%S"),r"***********************************************"])
    _update_configs()
    app.run("0.0.0.0", 8080, threaded=False)
