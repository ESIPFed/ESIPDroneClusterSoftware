# Introduction

Note1: All commands except clean can recieve multiple input files at once and depending on the command will eithe rplot multiple data sets into one fingure or generate multiple separate figures
Note2: -s will show each plot as its generated and require each be closed before the next can be generated, if creating many plots leave this flag off
Note3: All figures are saved in ./images/  There is currently NO OVERWRITE PROTECTION

# Get help
```
$ python main.py -h
```

# Plot simple profile scatter plot (CO2 and Altitude)
```
$ python main.py -s Splot morning1.csv afternoon1.csv
```

# Plot simple historgram
```
$ python main.py -s Hplot 100 morning1.csv
```

# Plot 1 or more CO2 logs' quartiles in boxplots on the same figure
```
$ python main.py -s Bplotmulti 0.0 morning1.csv afternoon1.csv #Will align files based on reaching the take-off altitude
$ python main.py -s Bplotmulti 60 morning1.csv afternoon1.csv #Will align files based on when each flight reached 60m altitude for the first time
```

# Plot CO2 vs Altitude
```
$ python main.py -s plotCVsA 20  morning1.csv afternoon1.csv      #Will align files based on when each flight reached 20m altitude for the first time
$ python main.py -s plotCVsA 0.0  morning1.csv afternoon1.csv     #Will align files based on reaching the take-off altitude
```

# Plot CO2 and Altitude logs aligned to a given altitude

Note below example creates 2 plots, neither of which will be shown but only saved
```
$ python main.py plotaligned 0.0 ../example/morning1.csv ../example/afternoon1.csv  #Will align/begin plot based on log reaching takeoff altitude (or specified altitude if give)
```

# Plot multiple CO2 and Alt logs aligned on the same figure:
```
$ python main.py -s plotVmulti 20  morning1.csv afternoon1.csv      #Will align files based on when each flight reached 20m altitude for the first time
$ python main.py -s plotVmulti 0.0  morning1.csv afternoon1.csv     #Will align files based on reaching the take-off altitude
```