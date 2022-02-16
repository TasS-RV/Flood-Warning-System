import matplotlib.pyplot as plt

def plot_water_levels(station, dates, levels, plot=True):
    # Plot
    plot = plt.plot(dates, levels)

    # Add axis labels, rotate date labels and add plot title
    plt.xlabel('Date')
    plt.ylabel('Water Level (m)')
    plt.xticks(rotation=45)
    plt.title(station.name)

    # Display plot
    plt.tight_layout()  # This makes sure plot does not cut off date labels

    if plot == True:
        plt.show()

    return plot