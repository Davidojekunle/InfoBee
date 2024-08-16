import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the CSV data
data = pd.read_csv('uploads/air_quality_no2_long.csv', parse_dates=['date.utc'])

# Set the 'date.utc' column as the index
data = data.set_index('date.utc')

# Create a folder for the plots
if not os.path.exists('visuals'):
    os.makedirs('visuals')

# Plot 1: Time series of NO2 levels in Paris
plt.figure(figsize=(12, 6))
data[data['city'] == 'Paris']['value'].plot()
plt.title('NO2 Levels in Paris')
plt.ylabel('NO2 (µg/m³)')
plt.savefig(os.path.join('visuals', 'paris_no2_timeseries.png'))
plt.show()

# Plot 2: Boxplot of NO2 levels in different cities
plt.figure(figsize=(12, 6))
data.boxplot(column='value', by='city')
plt.title('NO2 Levels in Different Cities')
plt.ylabel('NO2 (µg/m³)')
plt.savefig(os.path.join('visuals', 'no2_levels_boxplot.png'))
plt.show()

# Plot 3: Scatter plot of NO2 levels vs. time of day in Paris
plt.figure(figsize=(12, 6))
paris_data = data[data['city'] == 'Paris']
plt.scatter(paris_data.index.hour, paris_data['value'])
plt.title('NO2 Levels in Paris vs. Time of Day')
plt.xlabel('Hour of Day')
plt.ylabel('NO2 (µg/m³)')
plt.savefig(os.path.join('visuals', 'paris_no2_scatter.png'))
plt.show()

# Plot 4: Heatmap of NO2 levels in Paris over time
# plt.figure(figsize=(12, 6))
# paris_data.groupby([paris_data.index.hour, paris_data.index.day]).mean()['value'].unstack().plot(cmap='viridis')
# plt.title('NO2 Levels in Paris - Heatmap')
# plt.xlabel('Day of Month')
# plt.ylabel('Hour of Day')
# plt.savefig(os.path.join('visuals', 'paris_no2_heatmap.png'))
# plt.show()

# Plot 5: Line plot of NO2 levels in different cities over time
plt.figure(figsize=(12, 6))
for city in data['city'].unique():
    data[data['city'] == city]['value'].plot(label=city)
plt.title('NO2 Levels in Different Cities Over Time')
plt.ylabel('NO2 (µg/m³)')
plt.legend()
plt.savefig(os.path.join('visuals', 'no2_levels_lineplot.png'))
plt.show()