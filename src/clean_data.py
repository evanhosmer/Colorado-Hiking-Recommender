import pandas as pd
import numpy as np

df = pd.read_csv('../data/dataframe.csv')

names = df['Name']
features = df.drop(['Name'], axis = 1)

features = features.dropna()

features = features.rename(index = str, columns = {'Route Type': 'route_type', 'Elevation Gain': 'elevation_gain'})

features['Distance'] = features['Distance'].str.replace('miles','')
features['Distance'] = features['Distance'].str.replace('km','')
features['Distance'] = features.Distance.astype(float)
features['elevation_gain'] = features['elevation_gain'].str.replace('feet','')
features['elevation_gain'] = features['elevation_gain'].str.replace('m','')
features['elevation_gain'] = features['elevation_gain'].str.replace(',','')
features['elevation_gain'] = pd.to_numeric(features['elevation_gain'])

features.Difficulty = pd.Categorical(features.Difficulty)
features['difficulty'] = features.Difficulty.cat.codes.astype('category')

features.route_type = pd.Categorical(features.route_type)
features['route'] = features.route_type.cat.codes.astype('category')

difficulty_dict = dict(enumerate(features['Difficulty'].cat.categories))
route_dict = dict(enumerate(features['route_type'].cat.categories))

features = features.drop(['Difficulty','route_type'],axis = 1)

features.to_csv('../data/clean_data.csv', index = False)
