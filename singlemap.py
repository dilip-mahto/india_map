import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import os
os.chdir(r'C:\Users\dilip.mahto\Desktop\Personal\Learning\Python\India Map')

# Load the Excel file
excel_file = r'C:\Users\dilip.mahto\Desktop\Personal\Learning\Python\India Map\Benefitted_Farmers_Applications.xlsx'  # Replace with your Excel file path
df_enrollment = pd.read_excel(excel_file)

# Load the GeoJSON file
geojson_file = (r'C:\Users\dilip.mahto\Desktop\Personal\Learning\Python\India Map\India_states4.json')  
gdf_states = gpd.read_file(geojson_file)
# Load the Excel file
df_enrollment = pd.read_excel(excel_file)
print("Enrollment DataFrame Columns:", df_enrollment.columns)

# Strip whitespace from column names
df_enrollment.columns = df_enrollment.columns.str.strip()
gdf_states.columns = gdf_states.columns.str.strip()

# Merge the enrollment data with the GeoJSON data
gdf_merged = gdf_states.merge(df_enrollment, left_on='State_Name', right_on='State_Name', how='left')  # Adjust 'State_Name' as necessary

# Define color bins and corresponding colors
bins = [0, 100, 300, 500, 1000, 2000]
colors = ['#FFB6C1', '#ADD8E6', '#ffbf00', '#90EE90', '#779B52']  # Light to dark green

labels = ['0-100', '100-300', '300-500', '500-1000', '1000-2000'] 

# Create a color map based on enrollment percentage
cmap = plt.cm.colors.LinearSegmentedColormap.from_list('custom', colors, N=len(bins)-1)

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
gdf_merged.boundary.plot(ax=ax, linewidth=1)

# Plot with the correct colors and store the mappable object
mappable = gdf_merged.plot(column='Applications_Insured', ax=ax, cmap=cmap, edgecolor='black', legend=False)

# Remove axis labels and ticks
ax.set_xticks([])  # Remove x-axis ticks
ax.set_yticks([])  # Remove y-axis ticks
ax.set_xlabel('')  # Remove x-axis label
ax.set_ylabel('')  # Remove y-axis label

# Customize the legend
legend_handles = [Line2D([0], [0], marker='o', color='w', label=f'{bins[i]}-{bins[i+1]}%', 
                          markerfacecolor=colors[i], markersize=10) for i in range(len(colors))]

# Add the legend to the plot
ax.legend(handles=legend_handles, title='Applications Insured (In Lakh)', loc='upper right')

# Save the figure
plt.title('State Wise Farmers Applications Insured under PMFBY')
plt.savefig('state_enrollment_map10.jpeg', format='jpeg', dpi=400)
plt.close()

