# Understanding crime in Vancouver

As a beginner data science project, I wanted to study something I'm really passionate about: cities. Cities produce a huge amount of interesting data, and luckily, my hometown of Vancouver maintains a very nice [open data catalogue](http://data.vancouver.ca/datacatalogue/index.htm) with data on everything from [crime](http://data.vancouver.ca/datacatalogue/crime-data.htm), to [bikeways](http://vanmapp1.vancouver.ca/gmaps/covmap_data.htm?map=bikeways.kmz&data=1), to the location of every single street [tree](http://data.vancouver.ca/datacatalogue/streetTrees.htm). I seriously can't wait to dive into all the weird details on this site, but I decided to start with crime, largely because it is a good sized data set with interesting connections to some of the unique attributes of different neighbourhoods. I feel like some good crime predictors will be found in the [census](http://data.vancouver.ca/datacatalogue/censusLocalAreaProfiles2011.htm), [business licenses](http://data.vancouver.ca/datacatalogue/businessLicence.htm), [homeless shelters](http://vanmapp1.vancouver.ca/gmaps/covmap_data.htm?map=homeless_shelters.kmz&data=1), and [traffic counts](http://data.vancouver.ca/datacatalogue/trafficCounts.htm).

The Vancouver Police Department data set has a few interesting things to look at, even before I delve into the potential crime predictors. The data spans 14 years (from 2003) and is updated weekly. It categorizes crimes into 7 categories
* BNE Commercial: (Commercial Break and Enter) Breaking and entering into a commercial property with intent to commit an offence
* BNE Residential/Other: (Residential Break and Enter) Breaking and entering into a dwelling/house/apartment/garage with intent to commit an offence
* Homicide: A person, directly or indirectly, by any means, causes the death of another person.
* Mischief: A person commits mischief that willfully causes malicious destruction, damage, or defacement of property. This also includes any public mischief towards another person.
* Offence Against a Person: An attack on a person causing harm that may include usage of a weapon.
* Other Theft: Theft of property that includes personal items (purse, wallet, cellphone, laptop, etc.), bicycle, etc.
* Theft from Vehicle: theft of property from a vehicle o	Theft of Vehicle: Theft of a vehicle, motorcycle, or any motor vehicle

The first thing I wanted to do is plot the physical locations of all of the crimes, to see if there might be differences in the type and density of crime in various neighbourhoods. 

![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")
