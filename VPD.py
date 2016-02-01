import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import utm
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as colors
import matplotlib.cm as cm

# read in Vancouver crime data
print('Loading data...')
crime_data = pd.read_csv('crime_csv_all_years.csv')

# I want to plot the spatial data: the locations of all crimes in Vancouver

# get coordinates of all crimes from the df
crime_coords = crime_data[['X','Y']]

# remove zeros from coordinates 
# (the location data was removed from the crime types Offense against a Person (assault?) and Homicide
crime_coords = crime_coords[(crime_data['X'] >0) & (crime_data['Y']>0)]

# make a list out of the coordinates
x = crime_coords['X'].tolist()
y = crime_coords['Y'].tolist()

# data is in UTM Zone 10, change to latitude/longitude for placing on a map
latlon = [utm.to_latlon(xs, ys, 10, northern = True) for xs, ys in zip(x,y)]

crimeLon, crimeLat = zip(*latlon)

# Plot on top of a world map (from Basemap)
# Note that I messed with the formatting by hand in iPython Notebook, and it looks much worse in the
# saved out files from this script. I could fix that, but I ran out of time and didn't think it was 
# that important.
print('Plotting map (this is really slow)...')
fig1 = plt.figure(1)
ax0 = plt.subplot2grid((2,5),(0,0),colspan=2,rowspan=2)

map = Basemap(projection='merc', 
    resolution='f', area_thresh=0.05,  
    llcrnrlon=-123.3, llcrnrlat=49.15,  
    urcrnrlon=-123, urcrnrlat=49.35)
 
map.drawrivers(linewidth=1.0, color='0.8', antialiased=1)
map.drawcoastlines()
map.fillcontinents(color = 'burlywood')
map.drawmapboundary()

plt.show()
plt.title('All crime')

# VPD offsets all locations to protect privacy. This is my manual adjustment. Can do better with image registration later.
print('Plotting crime locations...')
cx, cy = map(crimeLat, crimeLon)
yoffset = 229 
cy = np.array(cy)+yoffset
map.plot(cx, cy, 'b.',markersize = 5, alpha=0.01)
plt.show()

# I'm also interested in how the specific crime types vary by location
# Plot heat maps of each crime type
print('Plotting heat maps for crime types...')

ax1 = plt.subplot2grid((2,5),(0,2))
ax2 = plt.subplot2grid((2,5),(0,3))
ax3 = plt.subplot2grid((2,5),(0,4))
ax4 = plt.subplot2grid((2,5),(1,2))
ax5 = plt.subplot2grid((2,5),(1,3))
ax6 = plt.subplot2grid((2,5),(1,4))

# get group categories
years = np.sort(pd.unique(crime_data.YEAR))
types = pd.unique(crime_data.TYPE)

axlist = [ax1,ax2,ax3,ax4,ax5,ax6]

# for each type of crime, create a heat map of the crime locations
# Remove the cases for assault and homicide which have no location data
# I know this data is available via a VPD API, so I will try to get it later on
for counter, index in enumerate([0,2,3,4,5,6]):  
    type = types[index]
    
    # new df of crimes of each type
    sub_crime = crime_data[crime_data['TYPE']==type]
    
    # coordinates of the crime
    crime_coords = sub_crime[['X','Y']]
    
    # remove zeros from coordinates
    crime_coords = crime_coords[(crime_coords['X'] >0) & (crime_coords['Y']>0)]
    
    # make x,y coordinates into a list
    x = crime_coords['X'].tolist()
    y = crime_coords['Y'].tolist()

    # plot histogram
    frame = axlist[counter]
    plt.axes(frame)
    
    histplot = frame.hist2d(x, y, bins=100)
    plt.title(type)
    plt.xlim([484500,498000])
    plt.ylim([5450000,5462000])
 
    frame.axes.xaxis.set_ticklabels([])
    frame.axes.yaxis.set_ticklabels([])

plt.show()
plt.savefig('Fig1.png')

# So far I've just lumped all of the years of data together
# Now, I want to see how the various crime stats change with time
print('Plotting temporal data...')
grouped = crime_data.groupby(['TYPE'])
grouped_types = grouped['YEAR'].value_counts()

# I realize this is inefficient, but I'm still not that familiar with pandas
# I remove the current year from the data because it is not complete yet
all_data = years[:len(years)-1]
for type in types:
    data = grouped_types[type]
    array_data = np.vstack((data.index.values,data.values)).T
    array_data = array_data[array_data[:len(years)-1,0].argsort()]
    all_data = np.vstack((all_data,array_data[:,1]))

crime_totals = all_data[1:,:]

# order the data so that less frequent crimes will be at the top of the bar plot
ind = [0,4,3,2,6,1,5,7]
crime_totals = crime_totals[ind,:].T
types = types[ind]

# Make a stacked bar plot to show the data for each crime type, and the 
# total crime on the same plot
cmap = cm.jet
c = cmap(np.linspace(0,1,len(types)))
y = years[:len(years)-1]

plt.figure(2)
width = 0.35
ind = np.arange(len(years)-1)
plt.bar(ind, crime_totals[:,0], width, color=c[0,:]) #c[0,:]

# b stores the bottom of the bar
b = 0
# loop through all crime types
for itype in range(1,len(types)):
    itype
    b += crime_totals[:,itype-1]
    plt.bar(ind, crime_totals[:,itype], width, color=c[itype,:], bottom=b) #[itype,:]

plt.xlabel('Year')
plt.ylabel('Crimes')
plt.title('Crimes by year and type')
plt.xticks(ind + width/2., years)
plt.legend(types)

plt.savefig('Fig2.png')

print('Done')