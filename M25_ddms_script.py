import pandas as pg
import geopandas as gpd
from matplotlib_scalebar.scalebar import ScaleBar
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines



# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles


# load the datasets
assets = gpd.read_file(r'C:\Users\wytna\Desktop\GIS_Course\EGM722\M25_ddms\M25-ddms-J16\data_files\m25J16points.shp')
assetsdef = gpd.read_file(r'C:\Users\wytna\Desktop\GIS_Course\EGM722\M25_ddms\M25-ddms-J16\data_files\m25_j16points_defect.shp')
studyarea = gpd.read_file(r'C:\Users\wytna\Desktop\GIS_Course\EGM722\M25_ddms\M25-ddms-J16\data_files\study_area_M25_J16.shp')
topoline = gpd.read_file(r'C:\Users\wytna\Desktop\GIS_Course\EGM722\M25_ddms\M25-ddms-J16\data_files\m25_j16polyline.shp')

# create a figure of size 10x10 representing the page size in inches, adding backgroung color
fig, ax = plt.subplots(figsize=(10, 10), facecolor = 'ivory')

#plotting shapefiles on the map
assets.plot(column='Layer', markersize=45, ax=ax)
assetsdef.plot(ax=ax, markersize=10, color='r')
topoline.plot(cmap='Greys', ax=ax, alpha=.5)


# getting a list of unique names for the drainage assets with defects
assets_def_names = list(assetsdef.Layer.unique())
assets_def_names.sort() # sort the drainage assets with defects alphabetically by name

# pick colours for assets to appear on the map
assets_def_colors = ['darkgreen', 'brown', 'darkviolet', 'darkblue', 'olive', 'darkgoldenrod', 'steelblue']
assets_colors = ['maroon']

# generate a list of handles for the asset datasets
assetsdef_handles = generate_handles(assetsdef.Layer.unique(), assets_def_colors, alpha=0.25)
assets_handle = generate_handles(assets.RefName.unique(), assets_colors, alpha=0.25)

# update drainage asset names to the legend, https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
nice_names = [name.title() for name in assets_def_names]

# taking a list of handles and updating the lables for the legend
handles = assetsdef_handles + assets_handle
labels = nice_names + ['IC-UTR seized', 'GU-UTR seized', 'OL-UTGA', 'PN-UTGA', 'CP-UTR seized', 'GN-UTL']

# spesifying the appearance of legend
leg = ax.legend(handles, labels, title='Legend', title_fontsize=14, fontsize=12, loc='upper left', frameon=True, framealpha=1)


# add the text labels for the drainage assets, optimized iteration loop through rows at https://engineering.upside.com/a-beginners-guide-to-optimizing-pandas-code-for-speed-c09ef2c6a4d6
for i, row in assetsdef.iterrows():
    x, y = row.geometry.x, row.geometry.y
    plt.text(x, y, row['RefName'].title(), fontsize=8)# use plt.text to place a label at x, y
   
    
# Add a north arrow, https://stackoverflow.com/a/58110049/604456
x, y, arrow_length = 0.85, 0.10, 0.07
ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length), arrowprops=dict(facecolor='black', width=5, headwidth=15), ha='center', va='center', fontsize=20, xycoords=ax.transAxes)


# add scale bar, https://pypi.org/project/matplotlib-scalebar/
scalebar = ScaleBar(1) # 1 pixel = 1 meter
ax.add_artist(scalebar)


# add a title to the plot
ax.set(title='M25 Junction-16 DDMS The location of Drainage Assets with defects')

# plot the figure 
plt.show()

# save the figure 
fig.savefig('map.png', bbox_inches='tight', dpi=300)
