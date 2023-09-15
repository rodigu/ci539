import pandas as pd
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


def plot_percent_incorrect(df: pd.DataFrame, student: str):
    """Question 3

    Plots the percent of actions that resulted in either a `WRONG` or a `BUG` assessment for a given student.

    :param df: DataFrane with data extracted from `CognitiveTutorAlgebra-gaming-clips.csv`
    :param student: student id string
    """
    def map_assessment(val: str):
        return lambda x: 1 if x == val else 0
    df['Correct'] = df['assessment'].apply(map_assessment('RIGHT'))
    df['Incorrect'] = df['assessment'].apply(
        lambda x: 1 if x == 'WRONG' or x == 'BUG' else 0)
    df = df[df['assessment'] != 'HELP']
    k = df.groupby(['student', 'action']).mean(numeric_only=True).reset_index()
    k[k['student'] == student]\
        .sort_values('Correct')\
        .set_index('action')['Incorrect']\
        .plot.bar(title=f'Student {student} Percent Incorrect', ylabel='Percent Inorrect', ylim=(0, 1))
    return k


def learning_curve_for(original_df: pd.DataFrame, skill: str):
    """Learning curves for the skills named “Box and Whisker” and “Inverse Relation”

    :param original_df: DataFrame from `ASSISTments-sample.csv`
    :param skill: skill string
    """
    df = original_df[original_df['skill'] == skill]\
        .sort_values(['user_id', 'start_time'])\
        .reset_index()
    df['skill_encounter_number'] = df.groupby('user_id').cumcount() + 1
    df['correct'] = df.groupby(
        'user_id')['correct'].cumsum() / df['skill_encounter_number']
    df['error'] = 1 - df['correct']

    ax = df.groupby('skill_encounter_number')['error'].mean().plot(
        label=skill, ylabel='% of mistakes')
    ax.legend()
