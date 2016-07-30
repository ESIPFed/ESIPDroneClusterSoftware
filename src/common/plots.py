""" Shared CO2 flight data plotting functions """

import matplotlib.pyplot as plt
import pandas as pd

# TODO add proper logging
# Create pretty colours for plots
tableau20 = [(31, 119, 180), (123, 102, 210), (44, 160, 44), (255, 152, 150), (214, 39, 40), (23, 190, 207),
             (188, 189, 34), (127, 127, 127),
             (220, 95, 189), (140, 86, 75), (174, 199, 232), (255, 127, 14),
             (255, 187, 120), (152, 223, 138), (197, 176, 213), (196, 156, 148),
             (247, 182, 210), (199, 199, 199), (219, 219, 141), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)


def simple_Splot(afile, count, show=False):
    """Creates a scatter plot from a single cleaned CO2, ALT log
    :param afile    A source file containing aligned CO2 and Alt readings
    :param count   The image number of this run
    :param show: Default false, if true will show plots as generated
    """

    # Read in CO2 and Alt
    df = pd.read_csv(afile)
    # print(list(df.columns.values))
    co = df['CO2']
    alt = df['Altitude']
    x = range(len(alt))
    fig, ax1 = plt.subplots(figsize=(12, 14))
    # TODO Pick a plot option - scatter or line?
    ax1.plot(x, co, "o", color=tableau20[0], )  # Scatter
    # ax1.plot(x, co, color=tableau20[0],) #line
    ax1.set_xlabel('Time step')
    ax1.set_ylabel('CO2 (PPM)', color='k')
    for tl in ax1.get_yticklabels():
        tl.set_color('k')
    ax1.spines["top"].set_visible(False)
    ax1.spines["bottom"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_visible(False)
    ax1.get_xaxis().tick_bottom()
    ax1.get_yaxis().tick_left()

    ax2 = ax1.twinx()
    ax2.plot(x, alt, color=tableau20[1], linestyle="--")
    ax2.set_ylabel('Altitude (m above sea level)', color='k')
    for tl in ax2.get_yticklabels():
        tl.set_color('k')
    ax2.spines["top"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.get_xaxis().tick_bottom()

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc=1)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    # plt.title("Vertical profile plot",color=tableau20[0])
    # TODO Check for overwriting
    plt.savefig("./images/Scatter{}_{}.png".format(count, "_".join(afile.split("_")[1:])), bbox_inches="tight")

    if show:
        plt.show()


def simple_Hplot(afile, bins, count, show=False):
    """Creates a basic histogram plot from a single cleaned CO2, ALT log
    :param afile    A source file containing aligned CO2 and Alt readings
    :param bins: Number of bins to use
    :param count   The image number of this run
    :param show: Default false, if true will show plots as generated
    """
    # Read in CO2 and Alt
    df = pd.read_csv(afile)
    co = df['CO2']

    plt.hist(co, bins, color=tableau20[count])  # histogram with 100 bins
    plt.xlabel("CO2 (ppm)")
    plt.ylabel("Number of Measurements")

    # TODO Check for overwriting
    plt.savefig("./images/Historgram{}_{}.png".format(count, "_".join(afile.split("_")[1:])), bbox_inches="tight")

    if show:
        plt.show()


def multi_Vplot(files, show=False):
    """
    :param files: Creates plot from list of files
    :param show: Default false, if true will show plots as generated
    :return: 0 on success, 1 on failure
    """
    # Setup
    fig, ax1 = plt.subplots(figsize=(12, 14))
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
    # plt.tight_layout()
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

    for (i, co, l) in zip(tableau20, CO2s, lables):
        x = range(len(co))
        # TODO Pick a plot option - scatter or line?
        ax1.plot(x, co, color=i, label="CO2_" + l.split("/")[-1].split("_")[-1])  # Scatter
        # ax1.plot(x, co, "o", color=i, label="CO2-"+l.split("/")[-1].split("_")[-1]))

    for (i, alt, l) in zip(tableau20, Alts, lables):
        x = range(len(alt))
        ax2.plot(x, alt, color=i, label="Alt_" + l.split("/")[-1].split("_")[-1], linestyle="--")

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    print("lables for ax1:", h1, l1)
    print("lables for ax1:", h2, l2)
    ax1.legend(h1 + h2, l1 + l2, loc=1)
    # plt.title("Vertical profile plot",color=black)
    # TODO Check for overwriting
    plt.savefig("./images/multiplot.png", bbox_inches="tight")

    if show:
        plt.show()


def co2_height(files, show=False):
    """Plot CO2 concentration by altitude
    Adapted from Bar's Jupyter notebook
    :param files: Creates plot from list of files
    :param show: Default false, if true will show plots as generated
    :return: 0 on success, 1 on failure
    """

    CO2s = []
    Alts = []
    lables = []

    for afile in files:
        df = pd.read_csv(str(afile))
        CO2s.append(df['CO2'])
        Alts.append(df['Altitude'])
        lables.append(afile)

    for (i, co, alt, l) in zip(tableau20, CO2s, Alts, lables):
        plt.plot(co, alt, color=i, label="CO2_" + l.split("/")[-1].split("_")[-1])

    plt.xlabel("CO2 (ppm)", fontsize=15, fontweight="bold");
    plt.ylabel("Altitude", fontsize=15, fontweight="bold");
    plt.legend(loc=0, fontsize=14)
    # TODO Check for overwriting
    plt.savefig("./images/CO2VSAlt.png", bbox_inches="tight")

    if show:
        plt.show()
    return 0


def Bplot_multi(files, show=False):
    """
    Create multiple box plots in the same figure
    Adapted from Bar's Jupyter notebook
    :param files: Creates plot from list of files
    :param show: Default false, if true will show plots as generated
    :return: 0 on success, 1 on failure
    """

    fig, ax = plt.subplots(figsize=(12, 14))

    CO2s = []
    Alts = []
    blables = []

    for afile in files:
        df = pd.read_csv(str(afile))
        CO2s.append(df['CO2'])
        Alts.append(df['Altitude'])
        blables.append(afile.split("/")[-1].split("_")[-1])

    # Create the boxplot
    bp = ax.boxplot(CO2s, patch_artist=True, sym='+')

    # Customise labels
    ax.set_xticklabels(blables, fontsize=20)
    plt.xlabel("Flights", fontsize=15, fontweight="bold");
    plt.ylabel("CO2 (ppm)", fontsize=15, fontweight="bold");

    #TODO remove alternative imlementation (commented out) that rotates colours
    # change outline color, fill color and line-width of boxes and medians
    for i in range(len(bp['boxes'])):
        # change outline and fill color
        bp['boxes'][i].set(color='k',linewidth=1)
        bp['boxes'][i].set(facecolor='w')
        # bp['boxes'][i].set(facecolor=tableau20[i])

        # change color and linewidth of the medians
        bp['medians'][i].set(color='r', linewidth=3)
        # bp['medians'][i].set(color=tableau20[i], linewidth=3)

    #Change colour of parameters that come in pairs (whiskers and caps)
    # for i in range(0,len(bp['whiskers']),2):
        # change color and line-width of the whiskers
        # bp['whiskers'][i].set(color=tableau20[i], linewidth=2)
        # bp['whiskers'][i+1].set(color=tableau20[i], linewidth=2)

        # change color and linewidth of the caps
        # bp['caps'][i].set(color=tableau20[i], linewidth=2)
        # bp['caps'][i+1].set(color=tableau20[i], linewidth=2)


    # # TODO Check for overwriting and/or ensure unique name
    plt.savefig("./images/BoxPlot{}.png", bbox_inches="tight")

    if show:
        plt.show()
    return 0
