import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from matplotlib.pyplot import xticks
import datetime
import numpy as np
import pandas as pd

# Close polts that might have been left open
plt.close(1)

# Generate some data to display
x = pd.date_range(start='2016/08/01',  end='2016/10/01',  freq='MS')
y = [42, 420, 250]
y = y[::-1]


# Create 1 figure, in the
ax = plt.subplot(111)
ax.bar(x, y, width=1)
ax.xaxis_date()

# Set the figure title and the axis labels
ax.set(xlabel='time (months)', ylabel='money (JPY)',
       title='Graph title!')
ax.grid()

# Turns the date labels by 90 degrees, so they do not overlap
plt.setp(plt.gca().get_xticklabels(), rotation=90, horizontalalignment='right')
locs, labels = xticks()

# Set x labels (i.e. prevents in between dates labels)
xticks(((x)))

# Make sure the x axis is not showing after or before the values we do have
ax.set_xbound(lower=x[0], upper=x[-1])

# Workaround for machines that can't plot to GUI
if False:
    plt.savefig("mygraph.png", bbox_inches="tight")
else:
    # matplotlib.use('TkAgg')
    plt.show()
