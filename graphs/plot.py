import base64
import datetime
from io import BytesIO
import os

from dotenv import load_dotenv
from matplotlib import use as mpl_use
import matplotlib.cm as cmx
from matplotlib.cm import get_cmap
from matplotlib.dates import DayLocator
from matplotlib.dates import HourLocator
from matplotlib.dates import DateFormatter
from matplotlib.dates import drange
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.pyplot import xticks
import numpy as np
import pandas as pd

# Read env variables from .env file
load_dotenv()

# Avoid threading issues
# Credits: https://stackoverflow.com/a/51178529
mpl_use('Agg')


def generatePie(labels, values):
    """
    Prepare the data for the pie graph
    """
    fig1, ax1 = plt.subplots()

    # Credits: https://stackoverflow.com/a/46693008/2535658
    def hide_less_2_perc_pies_labels(pct):
        return ('%1.1f%%' % pct) if pct > 2 else ''

    # Add theme
    # Credits: https://www.pythonprogramming.in/how-to-pie-chart-with-different-color-themes-in-matplotlib.html
    theme = plt.get_cmap('tab20c')
    ax1.set_prop_cycle("color", [theme(1. * i / len(values))
                             for i in range(len(values))])

    explode = tuple([0.05] * len(values))
    # explode = (0.05,0.05,0.05,0.05)

    patches, texts, _ = ax1.pie(values, autopct=hide_less_2_perc_pies_labels,
                                shadow=False, startangle=90, explode=explode)

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    ax1.axis('equal')

    centre_circle = plt.Circle((0, 0), 0.80, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Legend
    plt.legend(patches, labels, loc="best", facecolor="white", framealpha=0.3)
    plt.tight_layout()


def prepareGraphData(x, y, goals=None):
    """
    Prepare the data for the bar graph
    """
    currency = os.getenv("currency")
    # The blue color used in the examples on matplot docs
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
    x_ticket_labels = plt.gca().get_xticklabels()
    plt.setp(x_ticket_labels, rotation=90, horizontalalignment='right')

    # Force all dates labels to be displayed on the x axis
    xticks(((x)))

    # Draw goals if present
    if goals:
        cmap = get_cmap("Set1")
        color_list = cmap.colors

        legend_items = []
        for idx in range(len(goals)):
            goal = goals[idx]
            colorVal = color_list[idx]
            ax.axhline(y=goal.amount, xmin=0.0, xmax=1.0, color=colorVal)
            # Set goal legend
            red_patch = mpatches.Patch(color=colorVal, label=goal.text)
            legend_items.append(red_patch)
        plt.legend(handles=legend_items)


# Source: https://matplotlib.org/3.1.1/faq/howto_faq.html#how-to-use-matplotlib-in-a-web-application-server
def generatePieGraph(labels, values):
    """
    Create the pie graph data
    Returns the data in base64
    Return False in case of failure
    """
    generatePie(labels, values)
    # TODO: remove this (also update deploy playbook)
    plt.savefig('static/images/pie-graph.png',  bbox_inches="tight", dpi=130)
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=130)
    # Embed the result in the html output.
    return base64.b64encode(buf.getbuffer()).decode("ascii")


def generateGraph(x, y, goals):
    """
    Create the bar graph data
    Returns the data in base64
    Return False in case of failure
    """
    prepareGraphData(x, y, goals)
    # TODO: remove this (also update deploy playbook)
    plt.savefig('static/images/graph.png', bbox_inches="tight", dpi=130)
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=130)
    # Embed the result in the html output.
    return base64.b64encode(buf.getbuffer()).decode("ascii")
