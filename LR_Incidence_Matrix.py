#This program evaluates the shortest-path link-route incidence matrix for a given network and stores it in a .csv file
#Inputs: .csv file with info on all links in the network i.e. linkID, fromNodeID, toNodeID 

#Imports
import networkx as nx
import numpy as np
import csv

#Importing data from .csv file (linkID, fromNodeID, toNodeID respectively)
data = np.genfromtxt('C:\Users\Sudatta\Downloads\Simplified_network_final_actual_counts.csv', delimiter=',', skiprows=1, usecols=(1,26,27))

#Defining the network using a graph
G=nx.Graph()
for i in range(len(data)):
    G.add_node(data[i][1])
    G.add_node(data[i][2])
    G.add_edge(data[i][1],data[i][2],{'ID':data[i][0]})
ID=nx.get_edge_attributes(G,'ID')

#Calculating link-route incidence matrix
a = []
for i in range(len(data)):
    for j in range(len(data)):
        for k in range(len(data)):
            try:
                if (data[k][1] in list(nx.shortest_path(G,data[i][1], data[j][2]))) and (data[k][2] in list(nx.shortest_path(G,data[i][1], data[j][2]))):
                    a.append([1])
                else:
                    a.append([0])
            except (nx.NetworkXNoPath,nx.NetworkXError):
                a.append([0])
a=np.array(a)
b=np.zeros((G.number_of_edges()*G.number_of_edges(),G.number_of_edges()))
for i in range(G.number_of_edges()*G.number_of_edges()):
    for j in range(G.number_of_edges()):
        b[i][j]=a[i*G.number_of_edges()+j]

#Storing in .csv file
with open('C:\Users\Sudatta\Downloads\Incidence_matrix.csv','wb') as f:
    writer = csv.writer(f)
    for i in range(len(b)):
        writer.writerow(b[i])
                  

         
