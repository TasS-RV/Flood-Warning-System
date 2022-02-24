import matplotlib.pyplot as plt
import numpy as np

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
    
    plt.show() #Slight issue with firsts graph: Letcombe Bassette appears to be empty, therefore plot == True is not satified and pyplot window does not open

    #if plot == True:
     #   plt.show()

    return plot



#Trying something for part 2F:

def testing_polyfit():
    

# Create set of 10 data points on interval (0, 2)
    x = np.linspace(0, 2, 10)
    y = [0.1, 0.09, 0.23, 0.34, 0.78, 0.74, 0.43, 0.31, 0.01, -0.05]

# Find coefficients of best-fit polynomial f(x) of degree 4
    p_coeff = np.polyfit(x, y, 4) #The higher the order of polynomial, ther greater rthwe accuracy of the curve mapping 

    print(p_coeff)

# Convert coefficient into a polynomial that can be evaluated,
# e.g. poly(0.3)
    poly = np.poly1d(p_coeff) #Can retrun a sequence of coefficients

# Plot original data points
    plt.plot(x, y, '.')

# Plot polynomial fit at 30 points along interval
    x1 = np.linspace(x[0], x[-1], 30)
    plt.plot(x1, poly(x1))

# Display plot
    plt.show()

    return poly