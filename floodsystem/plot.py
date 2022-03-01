import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mplt
import datetime
import itertools


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




def plot_water_level_with_fit(station, dates, levels, p, range_plot=True, show_plot=True): #By default choose to plot the typical range High and Low

    #Initially due to empty plot stations with anomalous data
    if levels == None or dates == None:
        return "Error: Empty Data Set"

    elif len(levels) == 0 or len(dates) == 0: 
        return "Error: Empty Data Set"
    
    else:
        
    #Dates converted into float objects - required for polynomial fitting function
        x_dates = mplt.dates.date2num(dates)   
        x_dates_shift = [(date - x_dates[-1]) for date in x_dates] #Shifted by proportion of dates relative to earlier 
        #x_dates_shift: required for increased accuracy of polynomial fit

        coeff = np.polyfit(x_dates_shift, levels, p)  #Coefficient finding for fitting level and dates data with polynomial or degree p
    # Convert coefficient into a polynomial that can be evaluated
        poly = np.poly1d(coeff)

        plt.plot(dates, levels, color = 'r', label = "Real Data")
        poly_plot, = plt.plot(dates, poly(x_dates_shift), color = 'b', label = "Best-fit Curve")


        if range_plot == True:
           # range_dates = np.linspace(x_dates_shift[0], x_dates_shift[-1], len(x_dates_shift))
          #  range_dates = np.linspace(dates[0], dates[-1], len(x_dates_shift))

            range_low = list(itertools.repeat(station.typical_range[0],len(x_dates_shift)))
            range_high = list(itertools.repeat(station.typical_range[1],len(x_dates_shift)))
            
            plt.plot(dates, range_low, color = 'g', label = "High line") 
            rangeplot_high, = plt.plot(dates, range_high, color = '#00FA10', label = "Low line")     
            plt.xticks(rotation = 45)
            plt.legend()
       
    #Customising presentation of Graph:
        plt.legend()
        plt.xlabel("Dates: (MM DD Hr)")
        plt.ylabel("Water level")
    
        plt.xticks(rotation = 45) #Can accomodate days number easily on x-axis
        plt.title(station.name)

    #Display plot
        plt.tight_layout()  # This makes sure plot does not cut off date labels
        if show_plot == True:
            plt.show()

        return poly_plot, rangeplot_high


