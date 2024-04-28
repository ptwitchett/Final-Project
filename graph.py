import numpy as np
import matplotlib.pyplot as plt


# Create a function to plot radar chart
def plot_radar_chart(feature_names, values, ax=None):
    if ax is None:
        ax = plt.subplot(111, polar=True)
    #adjusts certain values to be  in line with other variables (0-1 scale)
    values[4] = values[4]/200
    values[3] = values[3]/-60
    num_features = len(feature_names)

    #calculate angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_features, endpoint=False)

    #plot data
    ax.fill(angles, values, color='b', alpha=0.1)
    ax.plot(angles, values, color='b', linewidth=2, linestyle='solid')
    
    ax.set_ylim(0, 1)

    #add feature labels
    ax.set_xticks(angles)
    ax.set_xticklabels(feature_names)

    return ax
