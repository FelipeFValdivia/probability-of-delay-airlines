import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, time

def print_ocurrencies(dataframe, columns, text="Ocurrencies for {} column"):
    for column in columns:
        print(text.format(column))
        print(dataframe[column].value_counts())
        print("\n")


def plot_barchar(value_count_dict, column):

    column_values = list(value_count_dict.keys())

    # Fixing random state for reproducibility
    if len(column_values) < 5:
        size = (7,5)
    elif len(column_values) < 15:
        size = (7,10)
    elif len(column_values) < 30:
        size = (15,20)
    else:
        size = (15,30)

    fig, ax = plt.subplots(figsize = size)

    # Example data
    y_pos = np.arange(len(column_values))
    ocurrencies = list(value_count_dict.values())
    ax.barh(y_pos, ocurrencies, align = 'center')
    ax.set_yticks(y_pos, labels = column_values)
    ax.invert_yaxis()  # labels read top-to-bottom\
    ax.set_title('{} distribution'.format(column)) 


def plot_multiple_barchar(dataframe, columns):
    for column in columns:
        value_count_dict = dataframe[column].value_counts().to_dict()

        plot_barchar(value_count_dict, column)
    plt.show()


def get_high_season(df_column):
    return list(
        map(
            lambda dt: compare_high_season_dates(dt), 
            df_column.to_numpy()
        )
    )


def compare_high_season_dates(string_dt):
    dt = datetime.strptime(
                string_dt,
                '%Y-%m-%d %H:%M:%S'               
            )
    if dt >= datetime(2017,12,15) or dt < datetime(2017,3,4):
        return 1
    elif dt >= datetime(2017,7,15) and dt < datetime(2017,8,1):
        return 1
    elif dt >= datetime(2017,9,11) and dt < datetime(2017,10,1):
        return 1
    else:
        return 0


def get_period_day(df_column):
    return list(
        map(
            lambda dt: compare_times_of_day(dt), 
            df_column.to_numpy()
        )
    )

def compare_times_of_day(string_dt):
    dt = datetime.strptime(
                string_dt,
                '%Y-%m-%d %H:%M:%S'               
            ).time()
    if dt >= time(19,0,0) or dt <= time(4,59,59):
        return "night"
    elif dt >= time(5,0,0) and dt <= time(11,59,59):
        return "morning"
    else:
        return "afternoon"
