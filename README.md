# Understanding crime in Vancouver

As a beginner data science project, I wanted to study something I'm really passionate about: cities. Cities produce a huge amount of interesting data, and luckily, my hometown of Vancouver maintains a very nice [open data catalogue](http://data.vancouver.ca/datacatalogue/index.htm) with data on everything from [crime](http://data.vancouver.ca/datacatalogue/crime-data.htm), to [bikeways](http://vanmapp1.vancouver.ca/gmaps/covmap_data.htm?map=bikeways.kmz&data=1), to the location of every single street [tree](http://data.vancouver.ca/datacatalogue/streetTrees.htm). I can't wait to dive into all the weird details on this site, but I decided to start with crime, largely because it is a good sized data set with interesting connections to some of the unique attributes of different neighbourhoods. I feel like some good crime predictors will be found in the [census](http://data.vancouver.ca/datacatalogue/censusLocalAreaProfiles2011.htm), [business licenses](http://data.vancouver.ca/datacatalogue/businessLicence.htm), [homeless shelters](http://vanmapp1.vancouver.ca/gmaps/covmap_data.htm?map=homeless_shelters.kmz&data=1), and [traffic counts](http://data.vancouver.ca/datacatalogue/trafficCounts.htm).

The Vancouver Police Department data set has a few interesting things to look at, even before I delve into the potential crime predictors. The data spans 14 years (from 2003) and is updated weekly. It categorizes crimes into 7 categories
* BNE Commercial: (Commercial Break and Enter) Breaking and entering into a commercial property with intent to commit an offence
* BNE Residential/Other: (Residential Break and Enter) Breaking and entering into a dwelling/house/apartment/garage with intent to commit an offence
* Homicide: A person, directly or indirectly, by any means, causes the death of another person.
* Mischief: A person commits mischief that willfully causes malicious destruction, damage, or defacement of property. This also includes any public mischief towards another person.
* Offence Against a Person: An attack on a person causing harm that may include usage of a weapon.
* Other Theft: Theft of property that includes personal items (purse, wallet, cellphone, laptop, etc.), bicycle, etc.
* Theft from Vehicle: theft of property from a vehicle 
* Theft of Vehicle: Theft of a vehicle, motorcycle, or any motor vehicle

The first thing I wanted to do is plot the physical locations of all of the crimes, to see if there might be differences in the type and density of crime in various neighbourhoods. 

![alt text](https://github.com/myamaximus/VPD/blob/master/spatial_crime_data.png)

The first plot was made using the Basemap package to plot the crime locations directly on top of a map of Vancouver.
```python
from mpl_toolkits.basemap import Basemap
map = Basemap(projection='merc', 
    resolution='f', area_thresh=0.05,  
    llcrnrlon=-123.3, llcrnrlat=49.15,  
    urcrnrlon=-123, urcrnrlat=49.35)

map.drawrivers(linewidth=1.0, color='0.8', antialiased=1)
map.drawcoastlines()
map.fillcontinents(color = 'burlywood')
map.drawmapboundary()

# crimeLat and crimeLon are the locations of the crimes from the dataframe
cx, cy = map(crimeLat, crimeLon)
yoffset = 229 
cy = np.array(cy)+yoffset
map.plot(cx, cy, 'b.',markersize = 5, alpha=0.01)
plt.show()
```
This is *seriously* slow, probably because it is loading a map of the entire Earth. I'm still looking for a way to make this faster, and maybe put in other city features like streets (or False Creek!). The VPD removes all location data from assaults and homicides from their public data, and offsets all crime location data. I guess they are trying to preserve the privacy of victims. I adjusted by hand, but eventually I can use image registration to get the correct locations (this will be important in correlating to location data for other properties). 

Because the Basemap function was so slow, I just plotted 2D histograms of the crime data by type. But already we can see some interesting patterns. This will make more sense if you know Vancouver a bit. First, surprise, surprise, the highest crime occurs in the areas of highest density: downtown and the areas basically north of 12th. I think crime/population would be a better measure of personal risk. You can also see that the bar street downtown shows up as a bright yellow line in the mischief category. And commercial BNEs happen mostly in commercial areas, downtown and on the main streets. The other categories are a bit more interesting. Residential BNEs are fairly evenly spread. I wonder if single dwelling homes are easier to break into than apartments. And why the difference between thefts *from* cars, and thefts *of* cars? Could the dark areas in the car theft plot come from lower density dwellings having garages? The best I can do is speculate until I dive into the other data sources.

The second thing I was interested in is how crime has changed with time. I've read a lot about the fact that crime has generally been on a downward trajectory the world over since the 90s. This data only starts from 2003, but we can still see a clear downward trend.

![alt text](https://github.com/myamaximus/VPD/blob/master/temporal_crime_data.png)

For this plot I did a stacked bar plot so that the trends in total crime and for individual types of crime could be seen. First, I have to be thankful that Vancouver is really a very safe city. The levels of homicide and assault are very low. What I found most interesting though is that there really is no clear downward trend in any category except for thefts from vehicles and thefts of vehicles. I am guessing that this has less to do with people becoming less criminal and more to do with better car securing technology. Although I also remember that the VPD has a [bait car program](http://www.huffingtonpost.ca/2013/01/31/bc-bait-car-program-new_n_2593849.html) which has apparently been running since 2003. I'd love to get my hands on the pre-2003 data.

This is all I have so far. Check back for updates soon!

