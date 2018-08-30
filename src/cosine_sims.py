import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from kmodes import kmodes
from kmodes import kprototypes
import prince
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from scipy.spatial import distance
from scipy.spatial.distance import cdist

def get_data():
    merged = pd.read_csv('../data/merged.csv')
    meta = merged[['Name', 'location', 'stars']]
    df = pd.read_csv('../data/famd.csv')
    df2 = pd.concat([meta,df], axis = 1)

    return df2

def filter_df(df, location, difficulty, distance, stars, feat1, feat2, feat3):

    loc = df[df['location'] == location]
    dif = loc[loc['Difficulty'] == difficulty]
    dist = dif[dif['Distance'] < distance]
    sta = dist[dist['stars'] > stars]
    final_df = sta.ix[(sta[feat1] == 'yes') & (sta[feat2] == 'yes') & (sta[feat3] == 'yes')]
    mms = StandardScaler()
    final_df[['Distance','elevation_gain']] = mms.fit_transform(final_df[['Distance','elevation_gain']])
    index_name = final_df['Name'].values
    final_df = final_df.drop(['Name','location','stars'], axis = 1)

    return final_df, list(final_df.index), index_name

def dim_reduct(df):
    famd = prince.FAMD(n_components=10, n_iter=10, copy=True, engine='auto',random_state=42)
    famd = famd.fit(df)
    print(sum(famd.explained_inertia_))
    dim_red = famd.row_coordinates(df)

    return dim_red

def recommendations(hike_idx, df, index_name, df_index, n=5):
    hike = df.iloc[hike_idx].values.reshape(1,10)
    cs = cosine_similarity(hike, df.loc[df_index].values)
    # cs = cosine_similarity(X, y).mean(axis=1)
    rec_index = np.argsort(cs)[0][-6:][::-1][1:]
    recommendations = []
    for rec in rec_index:
        recommendations.append(index_name[rec])
    return recommendations

if __name__ == '__main__':
    merged = pd.read_csv('../data/merged.csv')
    df_famd = pd.read_csv('../data/famd.csv')
    index_name_int = merged['Name'].values
    hike_name = 'Royal Arch Trail'
    for idx, name in enumerate(index_name_int):
        if name == hike_name:
            hike_idx = idx
    df = get_data()
    dim_red = dim_reduct(df_famd)
    df2, index, index_name = filter_df(df, 'White River National Forest', 'HARD', 12, 4, 'hiking', 'views','lake')
    recommendations = recommendations(hike_idx, dim_red, index_name, index, n=5)
