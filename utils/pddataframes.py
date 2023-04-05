import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, time

def print_ocurrencies(dataframe, columns, text="Ocurrencies for {} column"):
    for column in columns:
        print(text.format(column))
        print(dataframe[column].value_counts())
        print("\n")


def plot_barchar(value_count_dict, column, label="{} distribution"):

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
    ax.set_title(label.format(column)) 

def plot_grouped_barchar(first_dataframe, second_dataframe, columns):
    for column in columns:
        fdf_values = first_dataframe[column].value_counts().to_dict()
        sdf_values = second_dataframe[column].value_counts().to_dict()
        all_labels = list(set(fdf_values.keys()).union( set(sdf_values.keys())))
        x = np.arange(len(all_labels))
        y1 = fdf_values.values()
        y2 = sdf_values.values()
        width = 0.40

        plt.bar(x-0.2, y1, width)
        plt.bar(x+0.2, y2, width)
        plt.xticks(x, all_labels)
        plt.legend(["delayed", "in time"])
        plt.title("{} delayed compared".format(column))
        plt.show()


def plot_grouped_barchar_withpd(df, columns):
    df_gb = df.groupby(columns).size().unstack(level=1)
    df_gb.plot(kind = 'bar')


def plot_multiple_barchar(dataframe, columns, label="{} distribution"):
    for column in columns:
        value_count_dict = dataframe[column].value_counts().to_dict()

        plot_barchar(value_count_dict, column, label)
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

def get_ratios(delayed_flights, in_time_flights, columns):
    all_ratios = {}
    for column in columns:
        
        dly_flight_values = delayed_flights[[column]].value_counts().to_dict()
        int_flight_values = in_time_flights[[column]].value_counts().to_dict() 
        ratio_dict = {}
        for key, value in dly_flight_values.items():
            key_val = key[0] if isinstance(key, tuple) else key
            ratio_dict[key_val] =  value / (value + int_flight_values[key]) if key in int_flight_values else 1
        all_ratios[column] = ratio_dict
    return all_ratios