import pandas as pd
import numpy as np
import json

jsonfile = open('chord.json', 'w')
df = pd.read_csv("test1.csv")
data = np.zeros(shape=(10,10))

dict_names = {'M' : 0 , 'D' : 1 , 'P' : 2 , 'R' : 3 , 'T':4}

for i in range(len(df)):
    source = dict_names[df['sourceStage'][i][0]]
    destination = dict_names[df['destinationStage'][i][0]]
    data[source][destination+5] = data[source][destination+5] + 1
    data[destination+5][source] = data[destination+5][source] + 1

chord_list = []

for i in range(10):
    chord_list.append(data[0])

chord_list = []
for i in range(10):
    small =[]
    for j in range(10):
        small.append(int(data[i][j]))
    chord_list.append(small)

out = json.dumps(chord_list)
jsonfile.write(out)