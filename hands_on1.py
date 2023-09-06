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
