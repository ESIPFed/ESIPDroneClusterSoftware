""" Shared CO2 flight data plotting functions """

import matplotlib as plt
import pandas as pd

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


def simple_plot(afile, count, show=False):
    """Creates a Vprofile plot from a single cleaned Vprofile log
    :param afile    A source file containing aligned CO2 and Alt readings
    :param count   The image number of this run
    :param show: Default false, if true will show plots as generated
    """

    # Pretty setup
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
    # TODO Check for overwriting
    plt.savefig("./images/{}_{}.png".format(count, "_".join(afile.split("_")[1:])), bbox_inches="tight")

    if show:
        plt.show()


def multi_plot(files, show=False):
    """
    :param files: Creates plot from list of files
    :param show: Default false, if true will show plots as generated
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
        ax1.plot(x, co, color=plots.tableau20[i], label=l)
        i += 1

    i = 0
    for (alt, l) in zip(Alts, lables):
        x = range(len(alt))
        ax2.plot(x, alt, color=plots.tableau20[i], label=l, linestyle="--")
        i += 1

    # plt.title("Vertical profile plot",color=black)
    # TODO Check for overwriting
    plt.savefig("./images/multiplot.png", bbox_inches="tight")

    if show:
        plt.show()
