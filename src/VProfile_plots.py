"""
Reads in 1 or more CO2Meter profile logs and creates plots accordingly.  All comands except clean "-c" can be run
with multiple files
"""
import csv
import subprocess
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import sys

# Create pretty colours for plots
tableau20 = [(31, 119, 180), (123, 102, 210), (44, 160, 44), (255, 152, 150)
             (214, 39, 40), (23, 190, 207), (188, 189, 34), (127, 127, 127),
             (220,95,189),(140, 86, 75), (174, 199, 232), (255, 127, 14),
             (255, 187, 120),(152, 223, 138), (197, 176, 213),(196, 156, 148),
             (247, 182, 210), (199, 199, 199), (219, 219, 141), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

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




def clean_log(afile):
    """ Remove all data lines where drone was not in AUTO mode
    :param afile: CO2meter csv log file
    :return: 0 on success, 1 on failure
    """

    with open(afile, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        cfile=str(afile.split("/")[-1:][0])

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
    # TODO differentiate altitude (convert alt array into an array of instantaneous rate of change as a better start 'trigger'
    pass


def align_logs(afile, st_alt):
    """ Remove rows from prior to start_alt
    :param afile: CO2meter csv log file
    :return: 0 on success, 1 on failure
    """
    seek_start = 0
    cfile=str(afile.split("/")[-1:][0])

    with open("./temp/cleaned_" + cfile, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        next(csv_reader)

        with open("./temp/aligned_" + cfile, 'w', newline='') as aligned:
            csv_writer = csv.writer(aligned)
            csv_writer.writerow(["CO2", "Altitude"])

            # TODO replace this crude approximation with a differential based 'trigger'
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

    pass


def create_multiplot(files):
    """
    :param files: Creates plot from list of files
    :return: 0 on success, 1 on failure
    """
    # Setup
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Time step')
    ax1.set_ylabel('CO2 (PPM)', color='black')
    for tl in ax1.get_yticklabels():
        tl.set_color('black')
    ax1.spines["top"].set_visible(False)
    ax1.spines["bottom"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_visible(False)
    ax1.get_xaxis().tick_bottom()
    ax1.get_yaxis().tick_left()

    ax2 = ax1.twinx()
    ax2.set_ylabel('Altitude (m above sea level)', color='black')
    for tl in ax2.get_yticklabels():
        tl.set_color('black')
    ax2.spines["top"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.get_xaxis().tick_bottom()

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    # Read in CO2 and Alt
    CO2s = []
    Alts = []
    lengths = []
    lables = []

    for afile in files:
        df = pd.read_csv(str(afile))
        CO2s.append(df['CO2'])
        Alts.append(df['Altitude'])
        lables.append(afile)

        lengths.append(len(df['Altitude']))

    x = range(max(lengths))

    i = 0
    for (co, l) in zip(CO2s, lables):
        x = range(len(co))
        ax1.plot(x, co, color=tableau20[i], label=l)
        # ax1.plot(x, co, color=tableau20[i],label=l)
        # ax1.plot(x, co, color=tableau20[i])
        i += 1

    i = 0
    for (alt, l) in zip(Alts, lables):
        x = range(len(alt))
        ax2.plot(x, alt, color=tableau20[i], label=l, linestyle="--")
        # ax2.plot(x, alt, color=tableau20[i],label=l)
        i += 1

    # plt.title("Vertical profile plot",color=tableau20[0])
    #TODO Check for overwriting
    plt.savefig("./images/multiplot.png", bbox_inches="tight")

    # TODO add flag to turn this on and off
    #plt.show()


def make_plot(afile,count):
    """Creates a profile plot from a single cleaned profile log
    :param afile    A source file containing aligned CO2 and Alt readings
    :param count   The image number of this run
    """

    # Pretty setup
    # These are the "Tableau 20" colors as RGB.
    c1 = tableau20[4]
    c2 = tableau20[18]

    # Read in CO2 and Alt
    df = pd.read_csv(afile)
    # print(list(df.columns.values))
    co = df['CO2']
    alt = df['Altitude']
    x = range(len(alt))

    fig, ax1 = plt.subplots()
    ax1.plot(x, co, color=c1)
    ax1.set_xlabel('Time step')
    ax1.set_ylabel('CO2 (PPM)', color=c1)
    for tl in ax1.get_yticklabels():
        tl.set_color(c1)
    ax1.spines["top"].set_visible(False)
    ax1.spines["bottom"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_visible(False)
    ax1.get_xaxis().tick_bottom()
    ax1.get_yaxis().tick_left()

    ax2 = ax1.twinx()
    ax2.plot(x, alt, color=c2)
    ax2.set_ylabel('Altitude (m above sea level)', color=c2)
    for tl in ax2.get_yticklabels():
        tl.set_color(c2)
    ax2.spines["top"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.get_xaxis().tick_bottom()

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    # plt.title("Vertical profile plot",color=tableau20[0])
    #TODO Check for overwriting
    plt.savefig("./images/{}_{}.png".format(count,"_".join(afile.split("_")[1:])), bbox_inches="tight")

    # TODO add flag to turn this on and off
    #plt.show()


def clean_up():
    """
    Cleans up after script removing temporary files
    """
    print("Cleaning up")
    subprocess.call("rm -r ./temp/", shell=True)


def main():
    """ Run commands in correct sequence to create plot
    :return: 0 o success, 1 on failure
    """

    print(sys.version)

    # args parsing
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", help="A command is required")
    subparsers.required = True

    # Plot clean command
    pc_parser = subparsers.add_parser("plotcleaned",
                                      help="Clean and plot files: data point not associated with the \"AUTO\" status "
                                           "are removed")
    pc_parser.add_argument("files", nargs='+', help="(Required) Supply paths to CO2meter csv log files")

    # Plot aligned command
    pa_parser = subparsers.add_parser("plotaligned",
                                      help="Clean, align to st_alt, and plot files: logs will be cleaned and begin "
                                           "only after the trigger start_alt is reached")
    pa_parser.add_argument('st_alt', type=float,
                           help="(Required) Supply the GPS read altitude from which to trigger plotting in all "
                                "supplied files ")

    pa_parser.add_argument("files", nargs='+', help="(Required) Supply paths to CO2meter csv log files")

    # Plot multi plot command
    pm_parser = subparsers.add_parser("plotmulti",
                                      help="Clean, align to st_alt, and plot all supplied log files on the same graph: "
                                           "logs will be cleaned and begin only after the trigger start_alt is reached")
    pm_parser.add_argument('st_alt', type=float,
                           help="(Required) Supply the GPS read altitude from which to trigger plotting in all "
                                "supplied files ")
    pm_parser.add_argument("files", nargs='+', help="(Required) Supply paths to CO2meter csv log files")

    # Clean directory command
    c_parser = subparsers.add_parser("clean",
                                     help="Clean local directory, WARNING: this will remove all generated csv in the "
                                          "./temp directory")

    args = parser.parse_args()



    # Command Selection
    if args.command == "plotcleaned":
        check_make("./temp","directory")
        check_make("./images","directory")
        i = range(len(args.files))

        for f,i in zip(args.files,i):
            clean_log(f)
            ffile="./temp/cleaned_{}".format(str(f.split("/")[-1:][0]))
            make_plot(ffile,i)
            # make_plot("./temp/cleaned_{}".format(cf[0]),i)
        return 0

    elif args.command == "plotaligned":
        check_make("./temp","directory")
        check_make("./images","directory")
        i = range(len(args.files))

        for f,i in zip(args.files,i):
            clean_log(f)
            align_logs(f, args.st_alt)
            ffile="./temp/aligned_{}".format(str(f.split("/")[-1:][0]))
            make_plot(ffile,i)
        return 0

    elif args.command == "plotmulti":
        check_make("./temp","directory")
        check_make("./images","directory")

        aligned = []
        for f in args.files:
            # for f in args.files:
            clean_log(f)
            align_logs(f, args.st_alt)
            # aligned.append("./temp/aligned_{}".format(cf))
            aligned.append("./temp/aligned_{}".format(str(f.split("/")[-1:][0])))

        create_multiplot(aligned)
        return 0

    elif args.command == "clean":
        clean_up()
        return 0

    else:
        print("Unknown command")
        return 1



# Run main
main()
