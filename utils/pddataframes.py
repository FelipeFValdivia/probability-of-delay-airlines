import matplotlib.pyplot as plt
import numpy as np

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
