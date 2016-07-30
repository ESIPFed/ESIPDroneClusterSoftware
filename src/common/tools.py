""" Shared tools for manipulating data files coming off the drone """
import subprocess
import csv
import pandas as pd
import numpy as np
#TODO add proper logging

def dodo():
    print("woofwoof")
    if S:
        print("meewoo")


def align_logs(afile, st_alt=0.0):
    """ Remove rows from prior to start_alt and rewrite into an "aligned" file for use in plotting
    :param st_alt: Altitude on which to begin aligned file for plotting (this is the first instance of reaching a height
     above that given, should probbaly be greater than 25 as this is the default take-off and hover altitutde prior to
     being put into mission mode).  If set to 0.0 the local peak that indicates start of mission will instead be found
     and used as the starting point.
    :param afile: CO2meter csv log file
    :return: 0 on success, 1 on failure
    """
    seek_start = 0
    cfile = str(afile.split("/")[-1:][0])

    with open("./temp/cleaned_" + cfile, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        next(csv_reader)

        with open("./temp/aligned_" + cfile, 'w', newline='') as aligned:
            csv_writer = csv.writer(aligned)
            csv_writer.writerow(["CO2", "Altitude"])

            # TODO reafctor around if tools should be writeing out csv file or something else given its now doing actual data manipulation
            if st_alt == 0.0:
                # If no altitude to align by is given instead align by drop in alt from initial takeoff (indicates
                # entering mission mode)

                # Read in Alt
                df = pd.read_csv("./temp/cleaned_" + cfile)
                alt = df['Altitude']
                # Differentiate series
                alt_ = np.diff(alt)
                # Find switch to negative(descent)
                for i in enumerate(alt_):
                    if i[1] < 0:
                        break

                # Only write out rows after switch
                for row in enumerate(csv_reader):  # Scroll through lines till beyond switch to neg
                    if row[0] > i[0]:
                        break

                for row in enumerate(csv_reader):  # Continues from next line after last read in above loop
                    try:
                        csv_writer.writerow([row[1][0], row[1][1]])
                    except:
                        print("Failed to write row to \"{}\"".format(csv_writer))
                        return 1
            # An altitude to align by was given(this will be the first occurance of reaching above the given altitude)
            else:
                for row in csv_reader:
                    if seek_start == 0:
                        if float(row[1]) >= float(st_alt):
                            seek_start = 1
                    else:
                        try:
                            csv_writer.writerow([row[0], row[1]])
                        except:
                            print("Failed to write row to \"{}\"".format(csv_writer))
                            return 1
            return 0


def clean_up():
    """
    Cleans up after script removing temporary files
    """
    print("Cleaning up")
    subprocess.call("rm -r ./temp/", shell=True)


def check_make(path, dXf):
    """ Preforms the tedious process of checking is a file/directory exists and creating it if not.
    :param dXf: directory or file
    :param path: path
    :return: 0 on success, 1 on failure
    """

    if dXf.lower() == "file":
        try:
            retcode = subprocess.call("touch {}".format(path), shell=True)
            if retcode < 0:
                print("Child was terminated by signal", -retcode, file=sys.stderr)
            else:
                return 0

        except OSError as e:
            print("Execution failed:", e, file=sys.stderr)

    elif dXf.lower() == "directory":

        try:
            retcode = subprocess.call("mkdir {}".format(path), shell=True)
            if retcode < 0:
                print("Child was terminated by signal", -retcode, file=sys.stderr)
            else:
                return 0

        except OSError as e:
            print("Execution failed:", e, file=sys.stderr)

    else:
        return 1


def bclean_log(afile):
    """ Basic cleaning of data file: Remove all data lines where drone was not in AUTO mode
    :param afile: CO2meter csv log file
    :return: 0 on success, 1 on failure
    """

    with open(afile, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        cfile = str(afile.split("/")[-1:][0])

        with open(str("./temp/cleaned_" + cfile), 'w', newline='') as cleaned:
            csv_writer = csv.writer(cleaned)
            csv_writer.writerow(["CO2", "Altitude"])

            for row in csv_reader:
                # Remove all rows not from during the mission ("AUTO") and containing outlier CO2 readings above 1000PPM
                if "AUTO" in row and (float(row[0]) <= 1000):
                    try:
                        csv_writer.writerow([row[0], row[3]])
                    except:
                        print("Failed to write row to \"{}\"".format(csv_writer))
                        return 1

    return 0

    def diff(alt):
        """
        :param alt: list/pd/other of alt data for a log
        :return: list/pd/other of instantaneous rate change
        """
        # TODO Find a better way of detecting start of mission, 2 options:
        # - Differentiate altitude (convert alt array into an array of instantaneous rate of change as a better start 'trigger'
        # - Watch for a negative descent/ascent rate (MAV_CMD_CONDITION_CHANGE_ALT)
        pass

def clean_up():
    """
    Cleans up after script removing temporary files
    """
    print("Cleaning up")
    subprocess.call("rm -r ./temp/", shell=True)


