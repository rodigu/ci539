import pandas as pd

def get_avg_assignment(sample: pd.DataFrame):
  """How much time students spend on each assignment on average

  :param sample: _description_
  :return: _description_
  """
  
  # Dopping NaN
  df = sample[sample['end_time'].notna()]
  
  # Function to convert into timedelta formattable string
  convert_time = lambda t: '0 days 00:' + t[:-2]+ '.' +t[-1]

  df['start_time'] = pd.to_timedelta(df['start_time'].apply(convert_time))
  df['end_time'] = pd.to_timedelta(df['end_time'].apply(convert_time))

  df['total_time'] = df['end_time'] - df['start_time']
  
  # Drop sections where start time is greater than end time
  df = df[df['start_time'] < df['end_time']]
  
  df = df.drop(columns=['user_id', 'problem_id', 'assistment_id', 'hint_count', 'original', 'correct'])
  
  # Average
  df = df.groupby('assignment_id').mean(numeric_only=False)
  
  def td_to_str(td: pd.Timedelta):
    s = str(td)
    s = s.split()[2]
    s.split(':')
    return
  
  # Turn timedelta back to string
  df['total_time'] = df['total_time'].apply(str).apply(lambda s: s.split()[2])
  
  return df
