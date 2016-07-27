"""
Reads in 1 or more CO2Meter profile logs and creates plots accordingly.  All commands except clean "-c" can be run
with multiple files
"""
import argparse
import sys

from common import tools plots

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
        tools.check_make("./temp","directory")
        tools.check_make("./images","directory")
        i = range(len(args.files))

        for f,i in zip(args.files,i):
            tools.clean_log(f)
            ffile="./temp/cleaned_{}".format(str(f.split("/")[-1:][0]))
            plots.make_plot(ffile,i)
            # make_plot("./temp/cleaned_{}".format(cf[0]),i)
        return 0

    elif args.command == "plotaligned":
        tools.check_make("./temp","directory")
        tools.check_make("./images","directory")
        i = range(len(args.files))

        for f,i in zip(args.files,i):
            tools.clean_log(f)
            tools.align_logs(f, args.st_alt)
            ffile="./temp/aligned_{}".format(str(f.split("/")[-1:][0]))
            make_plot(ffile,i)
        return 0

    elif args.command == "plotmulti":
        tools.check_make("./temp","directory")
        tools.check_make("./images","directory")

        aligned = []
        for f in args.files:
            # for f in args.files:
           tools. clean_log(f)
           tools. align_logs(f, args.st_alt)
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
