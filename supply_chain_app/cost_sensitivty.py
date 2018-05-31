import pandas as pd
import csv
from re import sub
from decimal import Decimal
from collections import defaultdict
import math
import matplotlib.pyplot as plt



node = pd.read_csv("chain_data/14n.csv")
link = pd.read_csv("chain_data/14e.csv")
len_nodes = len(node)
len_link = len(link)
nodes = []
links = []
graph = defaultdict(list)
rev_graph = defaultdict(list)
cost = {}
demand = {}
length = {}
demand_stages = []

def dfs(stage , i):
    if stage=='Dist_0005':
        total = cost[stage] * ((i*20)/100)
    else:
        total = cost[stage]
    for pre in rev_graph[stage]:
        total+=dfs(pre , i)
    return total

def dfs2(stage):
    total = length[stage]
    maxx = 0
    for pre in rev_graph[stage]:
        if dfs2(pre) > maxx:
            maxx = dfs2(pre)
            
    return total+maxx

def dfs1(stage):
    if demand[stage]!=0:
        demand_stages.append(stage)
    for stages in graph[stage]:
        dfs1(stages)

for i in range(len_nodes):
    if math.isnan(node['avgDemand'][i]):
        demand[node['Stage Name'][i]] = 0
    else:
        demand[node['Stage Name'][i]] = node['avgDemand'][i]
    if math.isnan(float(Decimal(sub(r'[^\d.]', '', node['stageCost'][i])))):
        cost[node['Stage Name'][i]] = 0
    else:
        cost[node['Stage Name'][i]] = float(Decimal(sub(r'[^\d.]', '', node['stageCost'][i])))
    if math.isnan(node['stageTime'][i]):
        length[node['Stage Name'][i]] = 0
    else:
        length[node['Stage Name'][i]] = node['stageTime'][i]

for i in range(len_link):
    graph[link['sourceStage'][i]].append(link['destinationStage'][i])
    rev_graph[link['destinationStage'][i]].append(link['sourceStage'][i])

for i in range(len_nodes):
    if len(graph[node['Stage Name'][i]]) == 0:
        demand_stages.append(node['Stage Name'][i])
        

total_count  = 0

main_csv = []
variations = []
cogs = []
max_length = []
headings = ['Demand_Variations' , 'COGS']
main_csv.append(headings)
for i in range(0,11):
    total_demand = 0
    total_ans = 0
    total_ans1 = 0
    total_demand1 = 0
    for stage in demand_stages:
        '''if stage=='Retail_0059':
            new_demand = demand[stage] * ((20*i)/100)
            total_ans+=(dfs(stage)*new_demand)
            total_demand+=new_demand
        else:'''
        total_ans+=(dfs(stage , i)*demand[stage])
        total_demand+=demand[stage]
        total_ans1+=(dfs(stage,i))*demand[stage]*(dfs2(stage))
        total_demand1+=(dfs(stage,i))*demand[stage]
    print(total_ans/total_demand)
    variations.append(20*i)
    cogs.append(total_ans / total_demand)
    max_length.append(total_ans1/total_demand1)
print(variations)
print(cogs)
print(max_length)    
#plt.plot(variations , cogs , color = 'blue' , marker='o', markerfacecolor='blue')
plt.plot(variations , max_length , color = 'red' , marker='o', markerfacecolor='red')
plt.xlabel('Change in cost variations')
plt.ylabel('COGS')
plt.legend()
plt.show()
"""while not L.empty():
    q = set()
    g = []
    while not L.empty():
        x = L.get()
        print(x)
        for val in graph[x]:
            cost[val]+=cost[x]
        g.append(x)

        if len(graph[x]) == 0:
            total_ans+=cost[x]*demand[x]
            total_demand+=demand[x]

    for val in g:
        for v in graph[val]:
            q.add(v)

    for val in q:
        L.put(val)
    # if x[0]=='R':
    #     total_ans+=cost[x]*demand[x]
    #     total_demand+=demand[x]"""
