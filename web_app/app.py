from flask import Flask, request
import pickle
import pandas as pd
import numpy as np
from flask import Flask, render_template
from sklearn.preprocessing import StandardScaler
from kmodes import kmodes
from kmodes import kprototypes
import prince
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from scipy.spatial import distance
from scipy.spatial.distance import cdist
import pdb

with open('../data/links', 'rb') as f:
    links = pickle.load(f)

app = Flask(__name__, static_url_path='/static')

def get_data():
    merged = pd.read_csv('../data/merged.csv')
    meta = merged[['Name', 'location', 'stars']]
    df = pd.read_csv('../data/famd.csv')
    df2 = pd.concat([meta,df], axis = 1)

    return df2

def filter_df(df, location, difficulty, distance, stars):

    loc = df[df['location'] == location]
    dif = loc[loc['Difficulty'] == difficulty]
    dist = dif[dif['Distance'] < distance]
    sta = dist[dist['stars'] > stars]
    mms = StandardScaler()
    sta[['Distance','elevation_gain']] = mms.fit_transform(sta[['Distance','elevation_gain']])
    index_name = sta['Name'].values
    sta = sta.drop(['Name','location','stars'], axis = 1)

    return sta, list(sta.index), index_name

def dim_reduct(df):
    famd = prince.FAMD(n_components=10, n_iter=10, copy=True, engine='auto',random_state=42)
    famd = famd.fit(df)
    print(sum(famd.explained_inertia_))
    dim_red = famd.row_coordinates(df)

    return dim_red

def recom(hike_idx, df, index_name, df_index, n):
    hike = df.iloc[hike_idx].values.reshape(1,10)
    cs = cosine_similarity(hike, df.loc[df_index].values)
    # cs = cosine_similarity(X, y).mean(axis=1)
    rec_index = np.argsort(cs)[0][-(n+1):][::-1][1:]
    recommendations = []
    for rec in rec_index:
        recommendations.append(index_name[rec])
    return recommendations

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/submit', methods=['POST','GET'])
def submit():
    return render_template('index2.html')

@app.route('/pref', methods=['GET', 'POST'])
def pref():
    hike = str(request.form['hike_input'])
    n = int(request.form['num_rec'])
    return render_template('index3.html', hike=hike, n = n)

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    hike = str(request.form['hike_input'])
    n = int(request.form['num_rec'])
    location = str(request.form['location_input'])
    difficulty = str(request.form['difficulty_input'])
    distance = float(request.form['distance_input'])
    stars = float(request.form['stars_input'])

    merged = pd.read_csv('../data/merged.csv')
    df_famd = pd.read_csv('../data/famd.csv')
    index_name_int = merged['Name'].values
    for idx, name in enumerate(index_name_int):
        if name == hike:
            hike_idx = idx
    df = get_data()
    dim_red = dim_reduct(df_famd)
    df2, index, index_name = filter_df(df, location, difficulty, distance, stars)
    if len(df2) < n:
        return render_template('warning.html')
    recommendations = recom(hike_idx, dim_red, index_name, index, n)
    df_w_links = pd.read_csv('../data/hikes_w_links.csv')
    hiking_links = df_w_links[(df_w_links['Name'].isin(recommendations)) & (df_w_links['location'] == location)]['link']
    recommended = df_w_links[(df_w_links['Name'].isin(recommendations)) & (df_w_links['location'] == location)]['Name']
    r = recommended.values
    r2 = r.reshape(r.shape[0],1)
    l = hiking_links.values
    l2 = l.reshape(l.shape[0],1)
    comb = np.concatenate((r2,l2),axis = 1)

    return render_template('index4.html', comb = comb)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)
