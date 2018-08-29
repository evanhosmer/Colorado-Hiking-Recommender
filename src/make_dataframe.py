import pickle
import pandas as pd
import numpy as np


with open ('../data/outfile', 'rb') as fp:
    hikelist = pickle.load(fp)

first_five = [l[0:5] for l in hikelist]
df1 = pd.DataFrame(first_five, columns = ['Name', 'Difficulty','Distance','Elevation Gain', 'Route Type'])


cols = ['hiking','views','nature trips', 'walking','birding','wild flowers','forest','wildlife','trail running',
'dogs on leash', 'kid friendly', 'mountain biking','lake', 'dog friendly','river','horseback riding','no dogs','camping',
'snowshoeing','backpacking','waterfall','fishing', 'off road driving', 'cross country skiing','scenic driving','rock climbing',
'road biking','wheelchair friendly','skiing','historic site','cave','city walk','paddle sports','hot springs','rails trails',
'beach']

rest = [l[5:] for l in hikelist]

rows = []
for l in rest:
    row = []
    rows.append(row)
    for col in cols:
        if col in l:
            row.append(1)
        else:
            row.append(0)

df2 = pd.DataFrame(rows, columns = cols)

final_df = pd.concat([df1,df2], axis = 1)

final_df.to_csv('../data/dataframe.csv', index=False)
