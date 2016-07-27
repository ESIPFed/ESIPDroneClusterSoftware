""" Common tools for manipulating data files coming of the drone """
import subprocess
import csv


def check_make(path,type):
    """ Preforms the tedious process of checking is a file/directory exists and creating it if not.
    :param path: path
    :param type: file or directory
    :return: 0 on success, 1 on failure
    """


    if type.lower() == "file":
        try:
            retcode = subprocess.call("touch {}".format(path), shell=True)
            if retcode < 0:
                print("Child was terminated by signal", -retcode, file=sys.stderr)
            else: return 0

        except OSError as e: print("Execution failed:", e, file=sys.stderr)

    elif type.lower() == "directory":

        try:
            retcode = subprocess.call("mkdir {}".format(path), shell=True)
            if retcode < 0:
                print("Child was terminated by signal", -retcode, file=sys.stderr)
            else: return 0

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