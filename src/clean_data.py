import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler

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
missing_locs['location'] = pd.Series(new_locs,index = missing_locs.index)
cols = df.columns
missing_locs = missing_locs[cols]
merged_df = pd.concat([df,missing_locs], axis = 0).reset_index()
merged_df = merged_df.drop(['index'], axis = 1)
merged_df = merged_df.drop(merged_df[merged_df['Name'] == 'Argentine Pass Trail'].index)

names = merged_df['Name']
locations = merged_df['location']
star_list = merged_df['stars']
# features = merged_df.drop(['Name','location', 'stars'], axis = 1)
features = merged_df
features = features.rename(index = str, columns = {'Route Type': 'route_type', 'Elevation Gain': 'elevation_gain'})

features['Distance'] = features['Distance'].str.replace('miles','')
features['Distance'] = features['Distance'].str.replace('km','')
features['Distance'] = features.Distance.astype(float)
features['elevation_gain'] = features['elevation_gain'].str.replace('feet','')
features['elevation_gain'] = features['elevation_gain'].str.replace('m','')
features['elevation_gain'] = features['elevation_gain'].str.replace(',','')
features['elevation_gain'] = pd.to_numeric(features['elevation_gain'])
# features['stars'] = features.stars.astype(float)
# features.Difficulty = pd.Categorical(features.Difficulty)
# features['difficulty'] = features.Difficulty.cat.codes.astype('category')
#
# features.route_type = pd.Categorical(features.route_type)
# features['route'] = features.route_type.cat.codes.astype('category')
#
# difficulty_dict = dict(enumerate(features['Difficulty'].cat.categories))
# route_dict = dict(enumerate(features['route_type'].cat.categories))

# features = features.drop(['Difficulty','route_type'],axis = 1)
df_filtered = features.query('Distance < 30 & elevation_gain < 7000')
features_copy = features.query('Distance < 30 & elevation_gain < 7000')
df_filtered = df_filtered.drop(['Name','location', 'stars'], axis = 1)
### Change All to Categorical
# cat_cols = df_filtered.columns[2:38]
# for c in cat_cols:
#     df_filtered[c] = df_filtered[c].astype('category')
### Normalize numeric columns
# mms = StandardScaler()
# df_filtered[['Distance','elevation_gain']] = mms.fit_transform(df_filtered[['Distance','elevation_gain']])

cols = df_filtered.columns[4:]
for col in cols:
    df_filtered[col] = df_filtered[col].replace((1, 0), ('yes','no'))


# df_filtered.to_csv('../data/clean_data.csv', index = False)
df_filtered.to_csv('../data/famd.csv', index = False)
features_copy.to_csv('../data/merged.csv', index = False)
