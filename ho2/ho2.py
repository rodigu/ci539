import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np


def scatter_to_heat(df: pd.DataFrame) -> pd.DataFrame:
    """Converts DataFrame in scatterplot format
    (X, Y columns with one row for each point) into heatmap
    DataFrame (integer rows representing X and integer columns representing Y)

    :param df: scatterplot DataFrame
    :return: heatmap DataFrame
    """
    empty_row = [0] * int(df['X'].max()+2)
    num_rows = int(df['Y'].max()+2)
    heat = pd.DataFrame([empty_row] * num_rows)

    rounded = df.apply(np.round)
    for _, r in rounded.iterrows():
        x = r['X']
        y = r['Y']
        heat[x][y] += 1
    return heat


def plot_heatmap(df: pd.DataFrame):
    """Plots heatmap using seaborn

    :param df: heatmap data
    """
    ax = sns.heatmap(scatter_to_heat(df))
    ax.invert_yaxis()


def plot_scatter(df: pd.DataFrame):
    """Plot scatter data

    :param df: scatter DataFrame
    """
    df.plot.scatter(x='X', y='Y')
