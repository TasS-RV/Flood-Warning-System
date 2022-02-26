import matplotlib.pyplot as plt
import numpy as np

def plot_water_levels(station, dates, levels, show_plot=True):
    # Plot
    plot = plt.plot(dates, levels)

    # Add axis labels, rotate date labels and add plot title
    plt.xlabel('Date')
    plt.ylabel('Water Level (m)')
    plt.xticks(rotation=45)
    plt.title(station.name)

    # Plot typical ranges
    low, high = station.typical_range
    plt.axhline(low, linestyle='--')
    plt.axhline(high, linestyle='--')

    # Display plot
    plt.tight_layout()  # This makes sure plot does not cut off date labels
    
    if show_plot == True:
        plt.show()

    return plot



