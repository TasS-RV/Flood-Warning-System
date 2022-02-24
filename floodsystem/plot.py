import matplotlib.pyplot as plt
import numpy as np

def plot_water_levels(station, dates, levels, plot=True):
    # Plot
    plot_ax = plt.plot(dates, levels)

    # Add axis labels, rotate date labels and add plot title
    plt.xlabel('Date')
    plt.ylabel('Water Level (m)')
    plt.xticks(rotation=45)
    plt.title(station.name)

    # Display plot
    plt.tight_layout()  # This makes sure plot does not cut off date labels
    
   # plt.show() #Slight issue with firsts graph: Letcombe Bassette appears to be empty, therefore plot == True is not satified and pyplot window does not open

    if plot == True:
        plt.show()

    return plot_ax



