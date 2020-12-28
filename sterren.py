import os
from pathlib import Path
import requests
import pandas as pd
from matplotlib import pyplot as plt

linksFile = "links.txt"

# Downloading
with open(linksFile) as f:
    urls = f.readlines()

urls = [x.strip() for x in urls]

for url in urls:
    if url.find('/'):
        filename = url.rsplit('/', 1)[1]
        print("Downloading: " + filename)
    else:
        filename = "oeps.tbl"

    r = requests.get(url, allow_redirects=True)
    open('data/' + filename, 'wb').write(r.content)

# Converting to csv
pathlist = Path("data/").glob('**/*.tbl')
for path in pathlist:
    filename = str(path)
    if filename.find('\\'):
        filename = filename.rsplit('\\')[1]

    print("Converting: " + filename)

    cols = ["Time", "Time_BJD", "Time_Err", "CADENCENO", "Star_Flux", "a", "b", "xc", "xe", "egx",
            "thx", "xsef", "xsf", "xtyh", "xwef", "xweuy", "weerkx", "xrtrt", "ymntbrvecx", "xmnbv", "ytrex"]
    data = pd.read_table(
        path, comment='|', delim_whitespace=True, header=207, names=cols)

    data.to_csv("csv/" + filename[:-3] + "csv")

# make plot and find keppler id
pathlist = Path("csv/").glob('**/*.csv')
for path in pathlist:
    filename = str(path)
    if filename.find('\\'):
        filename = filename.rsplit('\\')[1]

    print("Making plot for: " + filename)

    keppler = filename.rsplit('-', 1)[0][4:].lstrip("0")

    data = pd.read_csv(path)
    x = data.Time
    y = data.Star_Flux
    plt.plot(x, y)
    plt.xlabel("Time")
    plt.ylabel("Star intensity")
    plt.title(keppler + " Transit light curve")
    plt.savefig("images/" + keppler + ".png")
