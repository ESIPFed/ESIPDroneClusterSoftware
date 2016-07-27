""" Library of common CO2 flight data plotting functions """

# Create pretty colours for plots
tableau20 = [(31, 119, 180), (123, 102, 210), (44, 160, 44), (255, 152, 150), (214, 39, 40), (23, 190, 207), (188, 189, 34), (127, 127, 127),
             (220,95,189),(140, 86, 75), (174, 199, 232), (255, 127, 14),
             (255, 187, 120),(152, 223, 138), (197, 176, 213),(196, 156, 148),
             (247, 182, 210), (199, 199, 199), (219, 219, 141), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)




