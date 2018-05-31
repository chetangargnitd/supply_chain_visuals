import pandas as pd
from collections import defaultdict
from decimal import Decimal
from re import sub
import json
df = pd.read_csv("test3.csv")
jsonfile = open('tree_map.json', 'w')
main_dict = {}
main_dict['name'] = 'Decision Support System'
main_dict['children'] = []
classification_dict = defaultdict(list)


df_len = len(df)

for i in range(df_len):
    stage = df['stageClassification'][i]
    stageName = df['stageName'][i]
    stageCost = round(Decimal(sub(r'[^\d.]', '', df['stageCost'][i]))*10)
    classification_dict[stage].append([stageName , stageCost])

# classification_len = len(classification_dict)

for key in classification_dict:
    l = []
    dict = {}
    dict['name'] = key
    dict['children'] = []
    for value in classification_dict[key]:
        small_dict = {}
        small_dict['name'] = value[0]
        small_dict['size'] = value[1]
        dict['children'].append(small_dict)

    main_dict['children'].append(dict)

out = json.dumps(main_dict,indent=4)
jsonfile.write(out)