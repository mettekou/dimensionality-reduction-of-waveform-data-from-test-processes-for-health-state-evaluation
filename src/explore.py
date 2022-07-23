import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.image import NonUniformImage
import json

def univariate(data: pd.DataFrame):
    fig, axs = plt.subplots(1, 2)
    axs[0].hist(data[data["ok"] == True]["Maximum_pressure_hysteresis_100-400mA"])
    axs[1].hist(data[data["ok"] == False]["Maximum_pressure_hysteresis_100-400mA"])
    plt.show()

def bivariate(data: pd.DataFrame):
    corr = data.select_dtypes(include=["float64"]).corr()
    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0, linewidths=.5, cbar_kws={"shrink": .5})
    plt.ylabel("Variable")

def waveform_heatmap(data):
    rows, columns = np.shape(data)
    x = np.array([ i % columns for i in range(rows * columns) ])
    heatmap, xedges, yedges = np.histogram2d(x, np.reshape(data, rows * columns), bins = (3500, 3056))
    fig, ax = plt.subplots()
    ax.pcolormesh(xedges, yedges, np.log(heatmap.T), cmap='rainbow')
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Pressure (bar)")
    #im = NonUniformImage(ax, interpolation='bilinear')
    #xcenters = (xedges[:-1] + xedges[1:]) / 2
    #ycenters = (yedges[:-1] + yedges[1:]) / 2
    #im.set_data(xcenters, ycenters, heatmap.T)
    #ax.images.append(im)
