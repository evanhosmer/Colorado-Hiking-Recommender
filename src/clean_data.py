import pandas as pd
import numpy as np
import pickle

with open ('../data/locations', 'rb') as fp:
    location = pickle.load(fp)

with open ('../data/stars', 'rb') as fp:
    stars = pickle.load(fp)

with open('../data/mis_loc','rb') as f:
    miss = pickle.load(f)

miss.insert(0, 'Boulder, Colorado')
loc = np.array(location)
sta = np.array(stars)
new_locs = np.array(miss)

df = pd.read_csv('../data/dataframe.csv')
df['location'] = pd.Series(loc, index = df.index)
df['stars'] = pd.Series(sta, index = df.index)
df = df.dropna()
missing_locs = df[df['location'].str.contains('None')]
missing_locs = missing_locs.drop(['location'], axis = 1)
df = df.drop(df[df['location'].str.contains('None')].index)
missing_locs['location'] = pd.Series(np.array(miss), index = missing_locs.index)
merged_df = pd.concat([df,missing_locs], axis = 0).reset_index()
merged_df = merged_df.drop(['index'], axis = 1)
merged_df = merged_df.drop(merged_df[merged_df['Name'] == 'Argentine Pass Trail'].index)

names = merged_df['Name']
locations = merged_df['location']
star_list = merged_df['stars']
features = merged_df.drop(['Name','location'], axis = 1)

features = features.rename(index = str, columns = {'Route Type': 'route_type', 'Elevation Gain': 'elevation_gain'})

features['Distance'] = features['Distance'].str.replace('miles','')
features['Distance'] = features['Distance'].str.replace('km','')
features['Distance'] = features.Distance.astype(float)
features['elevation_gain'] = features['elevation_gain'].str.replace('feet','')
features['elevation_gain'] = features['elevation_gain'].str.replace('m','')
features['elevation_gain'] = features['elevation_gain'].str.replace(',','')
features['elevation_gain'] = pd.to_numeric(features['elevation_gain'])
features['stars'] = features.stars.astype(float)
features.Difficulty = pd.Categorical(features.Difficulty)
features['difficulty'] = features.Difficulty.cat.codes.astype('category')

features.route_type = pd.Categorical(features.route_type)
features['route'] = features.route_type.cat.codes.astype('category')

difficulty_dict = dict(enumerate(features['Difficulty'].cat.categories))
route_dict = dict(enumerate(features['route_type'].cat.categories))

features = features.drop(['Difficulty','route_type'],axis = 1)

features.to_csv('../data/clean_data.csv', index = False)
