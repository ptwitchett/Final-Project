import numpy as np
import matplotlib.pyplot as plt

# Sample feature names and average feature values
#feature_names = ['Danceability', 'Energy', 'Loudness', 'Tempo', 'Instrumentalness']
#average_values = [0.7, 0.8, -5.2, 120, 0.2]  # Sample average values for demonstration
#standardize
#average_values[3] = average_values[3]/200
#average_values[2] = average_values[2]/-60
#print(average_values[3])


# Number of features
#num_features = len(feature_names)

# Create a function to plot radar chart
def plot_radar_chart(feature_names, values, ax=None):
    if ax is None:
        ax = plt.subplot(111, polar=True)
    values[4] = values[4]/200
    values[3] = values[3]/-60
    num_features = len(feature_names)

    # Calculate angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_features, endpoint=False)

    # Plot data
    ax.fill(angles, values, color='b', alpha=0.1)
    ax.plot(angles, values, color='b', linewidth=2, linestyle='solid')
    
    #ax.set_yticks([])
    ax.set_ylim(0, 1)

    # Add feature labels
    ax.set_xticks(angles)
    ax.set_xticklabels(feature_names)

    return ax

# Create a new figure
#plt.figure(figsize=(8, 8))

# Plot radar chart
#plot_radar_chart(feature_names, average_values)

# Show the radar chart
#plt.show()
