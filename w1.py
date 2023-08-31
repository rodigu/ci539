import pandas as pd


def get_avg_assignment(sample: pd.DataFrame):
    """How much time students spend on each assignment on average

    :param sample: dataframe with original sample data extracted from CSV
    :return: df grouped by assignment with average time column
    """

    # Dopping NaN
    df = sample[sample['end_time'].notna()]

    # Function to convert into timedelta formattable string
    def convert_time(t): return '0 days 00:' + t[:-2] + '.' + t[-1]

    df['start_time'] = pd.to_timedelta(df['start_time'].apply(convert_time))
    df['end_time'] = pd.to_timedelta(df['end_time'].apply(convert_time))

    df['total_time'] = df['end_time'] - df['start_time']

    # Drop sections where start time is greater than end time
    df = df[df['start_time'] < df['end_time']]

    # Drop unused columns
    df = df.drop(columns=['user_id', 'problem_id',
                 'assistment_id', 'hint_count', 'original', 'correct', 'skill', 'problem_type', 'start_time', 'end_time'])

    # Average
    df = df.groupby('assignment_id').mean(numeric_only=False)

    # Turn timedelta back to string
    df['average_time'] = df['total_time'].apply(
        lambda s: s.seconds)

    df = df.drop(columns=['total_time'])

    return df
