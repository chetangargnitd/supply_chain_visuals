import pandas as pd
import json

main_dict = {}

radius = {'D':6,'R':4, 'M':5,'P':3,'T':7}

jsonfile = open('test_force_directed.json', 'w')
node = pd.read_csv("7n.csv")
link = pd.read_csv("7e.csv")
len_nodes = len(node)
len_link = len(link)
nodes = []
links = []
cost = {}

for i in range(len_nodes):
    if i!=0:
        if(node['stageTime'][i] > main_dict['max']):
            main_dict['max'] = node['stageTime'][i]
        if(node['stageTime'][i] < main_dict['min']):
             main_dict['min'] = node['stageTime'][i]
    else:
        main_dict['max'] = node['stageTime'][0]
        main_dict['min'] = node['stageTime'][0]

for i in range(len_nodes):
    dict= {}
    dict["id"] = node['stageName'][i]
    dict["group"] = node['stageClassification'][i]
    s = node['stageCost'][i]
    s = s[1:]
    dict["cost"] = float(s)
    s = node['stageTime'][i]
    dict["time"] = float(s)
    dict["size"] = radius[node['stageClassification'][i][0]]
    cost[node['stageName'][i]] =  node['stageCost'][i]
    nodes.append(dict)

# print(nodes)
for i in range(len_link):
    dict= {}
    dict["source"] = link['sourceStage'][i]
    dict["target"] = link['destinationStage'][i]
    s = cost[link['sourceStage'][i]]
    dict["value"] = float(s[1:])
    links.append(dict)

# print(links)

main_dict['nodes'] = nodes
main_dict['links'] = links

# print(main_dict)

out = json.dumps(main_dict,indent=4)
jsonfile.write(out)