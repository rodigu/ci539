import pandas as pd


def get_avg_time_per_action(data: pd.DataFrame) -> pd.DataFrame:
    """Returns dataframe with average time taken per action on each Gaming clip

    Def: *The average time, in seconds, spent on each action included in the clip.*

    1. Removes NaN Gaming clip values from data
    2. Groups by Gaming clip id
    3. Averages numeric values
    4. Drops Row ID
    5. Renames time to `AvgTimePerAction`

    :param data: original dataset
    :return: dataset with `Gaming clip` id and AvgTimePerAction
    """
    return get_gaming_clip(data)\
        .groupby('Gaming clip')\
        .mean(numeric_only=True)\
        .drop(columns=['Row ID'])\
        .rename(columns={'time': 'AvgTimePerAction'})


def get_gaming_clip(data: pd.DataFrame) -> pd.DataFrame:
    return data[data['Gaming clip'].notna()]


def context_changes(data: pd.DataFrame) -> pd.DataFrame:
    shifted = data.shift(1)
    copied = data.copy()

    copied['#ContextChanges'] = (shifted['context'] == copied['context'])*1

    return get_gaming_clip(copied)\
        .groupby('Gaming clip')\
        .sum(numeric_only=True)\
        .drop(columns=['Row ID', 'time'])


def correct_actions(data: pd.DataFrame) -> pd.DataFrame:
    gaming_data = get_gaming_clip(data)

    gaming_data['#CorrectActions'] = (
        gaming_data['assessment'] == 'RIGHT') * 1

    return gaming_data\
        .groupby('Gaming clip')\
        .sum(numeric_only=True)\
        .drop(columns=['Row ID', 'time'])


def total_time_to_solve(data: pd.DataFrame):
    return data.groupby(['student', 'lesson']).sum(numeric_only=True).drop(columns=['Gaming clip', 'Row ID'])


def average_solve_time(data: pd.DataFrame):
    return data.groupby(['student', 'lesson']).sum(numeric_only=True).reset_index().groupby(['lesson']).mean(numeric_only=True).drop(columns=['Gaming clip', 'Row ID'])


def deviation_mean_solve_time(data: pd.DataFrame):
    tts = data.groupby(['student', 'lesson']).sum(numeric_only=True).drop(
        columns=['Gaming clip', 'Row ID']).reset_index()
    at = data.groupby(['student', 'lesson']).sum(
        numeric_only=True).reset_index().groupby(['lesson']).mean(numeric_only=True)
    avg_solve_time = average_solve_time(data)
    tts['DeviationFromMean'] = 0
    tts['TotalTimeToSolve'] = total_time_to_solve(data).reset_index()[
        'time']
    tts['AverageSolveTime'] = 0
    for lesson, content in at.iterrows():
        avg_time = content['time']
        tts.loc[tts['lesson'] == lesson, 'DeviationFromMean'] =\
            tts.loc[tts['lesson'] == lesson, 'time']\
            .apply(lambda x: avg_time-x)
        tts.loc[tts['lesson'] == lesson, 'AverageSolveTime'] =\
            avg_solve_time.loc[lesson]['time']

    return tts.drop(columns=['time'])
