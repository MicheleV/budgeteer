import base64
import datetime
from io import BytesIO
import os

from dotenv import load_dotenv
from matplotlib import use as mpl_use
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.cm as cmx
from matplotlib.cm import get_cmap
from matplotlib.dates import DayLocator
from matplotlib.dates import HourLocator
from matplotlib.dates import DateFormatter
from matplotlib.dates import drange
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
from matplotlib.pyplot import xticks
import numpy as np
import pandas as pd

from graphs.themes import _tab20c_data

# Read env variables from .env file
load_dotenv()

# Avoid threading issues
# Credits: https://stackoverflow.com/a/51178529
mpl_use('Agg')

# Address https://github.com/pandas-dev/pandas/issues/18301
pd.plotting.register_matplotlib_converters()


# Source: https://matplotlib.org/3.1.1/faq/howto_faq.html#how-to-use-matplotlib-in-a-web-application-server
def generatePieGraph(labels, values):
    """
    Create the pie graph data
    Returns the data in base64
    Return False in case of failure
    """
    fig = Figure(dpi=310)
    canvas = FigureCanvasAgg(fig)

    # Credits: https://stackoverflow.com/a/46693008/2535658
    def hide_less_2_perc_pies_labels(pct):
        return ('%1.1f%%' % pct) if pct > 2 else ''

    ax1 = fig.add_subplot(111)
    theme = _tab20c_data

    ax1.set_prop_cycle("color", _tab20c_data)

    explode = tuple([0.05] * len(values))
    # explode = (0.05,0.05,0.05,0.05)

    patches, texts, _ = ax1.pie(values, autopct=hide_less_2_perc_pies_labels,
                                shadow=False, startangle=90, explode=explode)

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    ax1.axis('equal')

    circle = Circle((0, 0), 0.80, facecolor='white')
    ax1.add_artist(circle)

    # Legend
    ax1.legend(patches, labels, loc="best", facecolor="white", framealpha=0.3)
    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=230)
    # Embed the result in the html output.
    return base64.b64encode(buf.getbuffer()).decode("ascii")


def generateBarGraph(x, y, goals):
    """
    Create the bar graph data
    Returns the data in base64
    Return False in case of failure
    """
    currency = os.getenv("CURRENCY")
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
        plt.legend(handles=legend_items, loc="center left")

    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=230)
    # Embed the result in the html output.
    return base64.b64encode(buf.getbuffer()).decode("ascii")
