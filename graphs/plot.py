import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from matplotlib.pyplot import xticks
import datetime
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


def generateDummyData():
    """
    Generate dates and hardcoded values
    Return tuples in format ([dates...], [values...])
    """
    x = pd.date_range(start='2016/08/01',  end='2016/10/01',  freq='MS')
    y = [1295541, 1687282, 2099517]
    return (x, y)


# Docs: https://matplotlib.org/3.1.1/gallery/pie_and_polar_charts/pie_features.html#sphx-glr-gallery-pie-and-polar-charts-pie-features-py
def generatePie(labels, values):
    fig1, ax1 = plt.subplots()

    # Credits: https://stackoverflow.com/a/46693008/2535658
    def hide_0_percent_pies_labels(pct):
        return ('%1.1f%%' % pct) if pct > 1 else ''

    ax1.pie(values, labels=labels, autopct=hide_0_percent_pies_labels,
          shadow=True, startangle=90)

    # def autopct_more_than_1(pct):
    #     return ('%1.f%%' % pct) if pct > 1 else ''

    # ax1.pie(values, labels=labels, autopct='%1.1f%%',
    #       shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


def prepareGraphData(x, y):
    """
    Prepare the data for the graph
    """
    # TODO: matplot lib has problem with 4 bytes characters
    currency = os.getenv("currency")
    # Blue used in examples on matplotsite
    # https://github.com/matplotlib/matplotlib/blob/v3.1.2/lib/matplotlib/_color_data.py#L17
    base_color = '#1f77b4'

    # Create 1 figure
    ax = plt.subplot(111)
    ax.bar(x, y, width=10, color=base_color)
    ax.xaxis_date()

    # Set the figure title and the axis labels
    ax.set(xlabel='time (months)', ylabel=f'Amount ({currency})',
           title='Monthly balances')
    ax.grid(True, which='major')

    # Turns the date labels by 90 degrees, so they do not overlap
    plt.setp(plt.gca().get_xticklabels(), rotation=90, horizontalalignment='right')

    # Force all dates labels to be displayed on the x axis
    xticks(((x)))

    # Make sure the x axis is not showing after or before the values we do have
    ax.set_xbound(lower=x[0], upper=x[-1])

    # TODO: add horizontal line with goal1, goal2...etc


def generatePieGraph(labels, values):
    """
    Create the pie graph and write it to a file
    """
    generatePie(labels, values)
    # Workaround for machines that do not have TKAgg
    plt.savefig('static/images/pie-graph.png')


def generateGraph(x, y):
    """
    Create the graph and write it to a file
    """
    prepareGraphData(x, y)

    # Workaround for machines that do not have TKAgg
    plt.savefig('static/images/graph.png', bbox_inches="tight")


def main(data, save_to_file=True):
    # Close plots that might have been left open
    plt.close(1)

    if data is None:
        # TODO: handle this
        print("Need data!")
        return 1
    else:
        x, y = data

    # Process and prepare the data
    prepareGraphData(x, y)

    # Workaround for machines that do not have TKAgg
    if save_to_file:
        plt.savefig('static/images/graph.png', bbox_inches="tight")
    else:
        # matplotlib.use('TkAgg')
        plt.show()


# Display demo graph if this file is called from cli
if __name__ == "__main__":
    # Generate some data to display
    save_to_file = False
    data = generateDummyData()
    main(data, save_to_file)
