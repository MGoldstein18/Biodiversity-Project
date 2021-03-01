#### Import Python modules

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

##### Load data from CSV files
# There are 2 CSV files - observations and species

observations = pd.read_csv('observations.csv')
observations.head()

species = pd.read_csv('species_info.csv')
species.head()


##### Explore the Species data

print('There are {} species in this data'.format(species.scientific_name.nunique()))

print('There are {} categories of species and they are : {}'.format(species.category.nunique(), species.category.unique()))

print('Here is breakdown of the number of animals/plants per species: \n\n{}'.format(species.groupby('category').size()))


#### Explore the Observations Data

print('There are {} parks in this data and they are : \n\n {}'.format(observations.park_name.nunique(), observations.park_name.unique()))

print("Here is a breakdown of the total number of sightings in each park: \n\n{}".format(observations.groupby('park_name').observations.sum()))


##### Replace the NaN values of the Conservation Status in the Species dataframe with "No Intervention" and then display the breakdown of animal/plant by status

species.conservation_status.fillna('No Intervention', inplace = True)
conservation_status = species.groupby('conservation_status').size()
print('Here is a breakdown of number of animals/plants in each conservation status category: \n\n {}'.format(conservation_status))


# ##### Pie chart of animals/plants with a conservation status which is not "No Intervention" by category of species

conservation_status = species[species.conservation_status != 'No Intervention']
plt.figure(figsize = (12, 9))
ax = plt.subplot()
plt.axis('equal')
plt.title('Pie chart of animals/plants with a conservation status which is not "No Intervention" by category of species')
plt.pie(x = conservation_status.groupby('category').size(), autopct = '%1d%%')
plt.legend(conservation_status.category.unique())
plt.show()
# ##### Analysis: It appears that, of the animals/plants which required some form of conservation intervention, birds make up a much larger percentage that other categories of species. 


##### Bar graph of number of animals/plants in each category of conservation status broken down by categort of species

plt.figure(figsize = (12, 9))
ax = plt.subplot()
plt.title('Bar graph of number of animals/plants in each category of conservation status broken down by categort of species')
sns.countplot(data = conservation_status, x = 'conservation_status', hue = 'category')
plt.legend(loc = 'upper right')
plt.show()


##### Add "protected" and "category" columns to the observations to dataframe to indicate whether or not that animal/plant is proetcted

np_array_observed = observations.scientific_name.to_numpy()
protected = []
category = []
for name in np_array_observed:
    animal = species[species.scientific_name == name]
    if animal.conservation_status.values[0] != 'No Intervention':
        protected.append(True)
        category.append(animal.category.values[0])
    else:
        protected.append(False)
        category.append(animal.category.values[0])
observations['protected'] = protected
observations['category'] = category
observations.head()


##### Breakdown of total sighting by procted or not

print('Breakdwon of total sightings by protected or not: \n\n{}'.format(observations.groupby('protected').observations.sum()))


##### Bar graph of average number of sightings per park with a hue of whether or not they are protected

plt.figure(figsize = (12, 9))
ax = plt.subplot()
plt.title('Bar graph of average number of sightings per park with a hue of whether or not they are protected')
sns.barplot(data = observations, x = 'park_name', y = 'observations', hue = 'protected')
plt.show()
# ##### Analysis: This graph indicates that, on average, when a protected animal/plant is sighted, it is sighted less often than non-protected animals


##### Bar graph of average number of sightings per park with a hue of category of animal/plant

plt.figure(figsize = (12, 9))
ax = plt.subplot()
plt.title('Bar graph of average number of sightings per park with a hue of category of animal/plant')
sns.barplot(data = observations, x = 'park_name', y = 'observations', hue = 'category')
plt.show()


##### Bar graph of sightings of protected animals/plants, broken down by park and category

protected_observations = observations[observations.protected == True]
plt.figure(figsize = (12, 9))
ax = plt.subplot()
plt.title('Bar graph of sightings of protected animals/plants, broken down by park and category')
sns.barplot(data = protected_observations, x = 'park_name', y = 'observations', hue = 'category')
plt.show()
# ##### Analysis: It appears that Yellowstone National Park has the most sighting of animals/plants in general and specifically protected wildlife. 
