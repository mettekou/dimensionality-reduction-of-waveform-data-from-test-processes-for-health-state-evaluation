import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.image import NonUniformImage
import plotly.express as px
import json

def univariate(data: pd.DataFrame):
    column_names = list(data.select_dtypes(include=["float64"]))
    data_long = pd.melt(data,
                            id_vars=["part_number", "revision_number", "item_batch_number",
                                     "item_serial_number", "process_name", "execution_start","ok"],
                            var_name="variable_path",
                            value_name="quantity_value_value",
                            value_vars=column_names)
    fig = px.histogram(data_long, x="quantity_value_value", color="ok", facet_col="variable_path", facet_col_wrap = 8, histfunc="count", nbins=50000, barmode="overlay")
    fig.update_xaxes(matches=None, showticklabels = True)
    fig.update_yaxes(matches=None, showticklabels = True)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    #fig.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))
    fig.show()
    #fig, axs = plt.subplots(8, 4)
    #fig.set_size_inches(6, 10)
    #column = 0
    #for column_name in column_names:
    #    sns.boxplot(y = column_name, x = "ok", data = data, ax=axs[column // 4, column % 4])
    #    column += 1
    #print(data.select_dtypes(include=["float64"]).describe(include="all").to_latex(float_format="%.3f"))
    #axs[0].hist(data[data["ok"] == True]["Maximum_pressure_hysteresis_100-400mA"])
    #axs[1].hist(data[data["ok"] == False]["Maximum_pressure_hysteresis_100-400mA"])
    #plt.show()

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

def cooks_d(model):
    influence = model.get_influence()
    influence.plot_influence()
    #distance = influence.cooks_distance
    #length = np.shape(distance)[0]
    #print(length)
    #plt.scatter(np.arange(length), influence.cooks_distance)
