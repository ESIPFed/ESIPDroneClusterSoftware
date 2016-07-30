"""
Reads in 1 or more CO2Meter profile logs and creates plots accordingly.  All commands except clean "-c" can be run
with multiple files
"""
import argparse
import sys

from common import tools, plots


def main():
    """ Run commands in correct sequence to create plot
    :return: 0 on success, 1 on failure
    """

    # print(sys.version)

    # args parsing
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-s', action='store_true', default=False,
                        help="Show plots as generated (requires a displayed plot be closed "
                             "before any further plots will be generated")
    subparsers = parser.add_subparsers(dest="command", help="A command is required")
    subparsers.required = True

    # Plot simple cleaned scatter of CO2 and Alt
    ps_parser = subparsers.add_parser("Splot",
                                      help="Simple clean scatter plots: removes all data points not associated with "
                                           "the \"AUTO\" status ")
    # TODO add configurable "excessive CO2 threashold - currently manually set in common/tools/bclean_log line 133 to 1000
    ps_parser.add_argument("files", nargs='+', help="(Required) Supply paths to CO2meter csv log files")

    # Plot simple cleand historgram
    ph_parser = subparsers.add_parser("Hplot",
                                      help="Simple clean histogram plots: removes all data points not associated with "
                                           "the \"AUTO\" status ")
    ph_parser.add_argument('bins', type=int, default=50, help="Number of histogram bins to use")
    # TODO add configurable "excessive CO2 threashold - currently manually set in common/tools/bclean_log line 133 to 1000
    ph_parser.add_argument("files", nargs='+', help="(Required) Supply paths to CO2meter csv log files")

    # Plot aligned command
    pa_parser = subparsers.add_parser("plotaligned",
                                      help="Clean, align to st_alt, and plot files: logs will be cleaned and begin "
                                           "only after the trigger start_alt is reached")
    pa_parser.add_argument('st_alt', type=float, default=0.0,
                           help=" Supply the GPS read altitude from which to trigger plotting in all "
                                "supplied files ")
    pa_parser.add_argument("files", nargs='+', help="(Required) Supply paths to CO2meter csv log files")

    # Plot multi plot command
    pm_parser = subparsers.add_parser("plotVmulti",
                                      help="Clean, align to st_alt, and plot all supplied log files on the same graph: "
                                           "logs will be cleaned and begin only after the trigger start_alt is reached")
    pm_parser.add_argument('st_alt', type=float, default=0.0,
                           help=" Supply the GPS read altitude from which to trigger plotting in all "
                                "supplied files ")
    pm_parser.add_argument("files", nargs='+', help="(Required) Supply paths to CO2meter csv log files")


    #Plot Box plot
    pb_parser = subparsers.add_parser("Bplotmulti",
                                      help="Clean, align to st_alt, and create box plots for all supplied log files on "
                                           "the same graph: logs will be cleaned and begin only after the trigger start"
                                           "_alt is reached")
    pb_parser.add_argument('st_alt', type=float, default=0.0,
                           help=" Supply the GPS read altitude from which to trigger plotting in all "
                                "supplied files ")
    pb_parser.add_argument("files", nargs='+', help="(Required) Supply paths to CO2meter csv log files")

    # Plot by altitude command
    pac_parser = subparsers.add_parser("plotCVsA",
                                      help="Clean, align to st_alt, and plot all supplied log files on the same graph as CO2 vs Altitude "
                                           "showing CO2 by altitude: "
                                           "logs will be cleaned and begin only after the trigger start_alt is reached "
                                           "if given (or by the decent trigger if not")
    pac_parser.add_argument('st_alt', type=float, default=0.0,
                           help=" Supply the GPS read altitude from which to trigger plotting in all "
                                "supplied files ")
    pac_parser.add_argument("files", nargs='+', help="(Required) Supply paths to CO2meter csv log files")

    # Clean directory command
    c_parser = subparsers.add_parser("clean",
                                     help="Clean local directory, WARNING: this will remove all generated csv in the "
                                          "./temp directory")

    args = parser.parse_args()

    print(args)

    # Command Selection
    if args.command == "Splot":
        tools.check_make("./temp", "directory")
        tools.check_make("./images", "directory")
        i = range(len(args.files))

        for f, i in zip(args.files, i):
            tools.bclean_log(f)
            ffile = "./temp/cleaned_{}".format(str(f.split("/")[-1:][0]))
            plots.simple_Splot(ffile, i, args.s)
        return 0

    if args.command == "Hplot":
        tools.check_make("./temp", "directory")
        tools.check_make("./images", "directory")
        i = range(len(args.files))

        for f, i in zip(args.files, i):
            tools.bclean_log(f)
            ffile = "./temp/cleaned_{}".format(str(f.split("/")[-1:][0]))
            plots.simple_Hplot(ffile, args.bins, i, args.s)
        return 0

    elif args.command == "plotaligned":
        tools.check_make("./temp", "directory")
        tools.check_make("./images", "directory")
        i = range(len(args.files))

        for f, i in zip(args.files, i):
            tools.bclean_log(f)
            tools.align_logs(f, args.st_alt)
            ffile = "./temp/aligned_{}".format(str(f.split("/")[-1:][0]))
            plots.simple_Splot(ffile, i, args.s)
        return 0

    elif args.command == "plotVmulti":
        tools.check_make("./temp", "directory")
        tools.check_make("./images", "directory")

        aligned = []
        for f in args.files:
            # for f in args.files:
            tools.bclean_log(f)
            tools.align_logs(f, args.st_alt)
            aligned.append("./temp/aligned_{}".format(str(f.split("/")[-1:][0])))

        plots.multi_Vplot(aligned, args.s)
        return 0

    elif args.command == "plotCVsA":
        tools.check_make("./temp", "directory")
        tools.check_make("./images", "directory")

        aligned = []
        for f in args.files:
            tools.bclean_log(f)
            tools.align_logs(f, args.st_alt)
            aligned.append("./temp/aligned_{}".format(str(f.split("/")[-1:][0])))

        plots.co2_height(aligned, args.s)
        return 0

    elif args.command == "Bplotmulti":
        tools.check_make("./temp", "directory")
        tools.check_make("./images", "directory")

        aligned = []
        for f in args.files:
            tools.bclean_log(f)
            tools.align_logs(f, args.st_alt)
            aligned.append("./temp/aligned_{}".format(str(f.split("/")[-1:][0])))

        plots.Bplot_multi(aligned, args.s)
        return 0

    elif args.command == "clean":
        clean_up()
        return 0

    else:
        print("Unknown command")
        return 1


# Run main
main()
