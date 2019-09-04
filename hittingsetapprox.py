__author__ = "Kaustav Basu"

'''
Please read the papers under Research, to better grasp the concept of Identifying Codes.
This program computes the O(log n) Approximate Identifying Code Set for a given graph. 
I utilize the Greedy Hitting Set Problem to obtain the approximate solution.
'''


# Packages required in this program


import networkx as nx
import pandas as pd
import numpy as np
import time
from itertools import combinations


def readGraphEdgelist():
    G = nx.Graph()
    G = nx.read_edgelist("Facebook/3980.edges", nodetype = int, create_using = nx.Graph())
    #G = nx.read_edgelist("as20000102.txt", nodetype = int, create_using = nx.Graph())
    return nx.to_numpy_matrix(G, nodelist = sorted(G.nodes()))

def readGraphCSV():
    df = pd.read_csv("UndirectedGraphs/COCAINE_MAMBO_UN.csv")
    #print(df)
    df = df.drop(df.columns[[0]], axis = 1)
    return df.values

# This function removes twins by forming super nodes (removing duplicates)
def twinRemoval():
    # Filetype is a user input to allow the program to select the appropriate file

    '''if filetype == 'csv':
        M = readGraphCSV()
    elif filetype == 'txt':
        M = readGraphEdgelist()'''
    M = readGraphEdgelist() 
    m, _ = M.shape
    print("Original Shape: ", M.shape)

    # Diagonal elements set to 1 to capture the closed neighborhood concept
    for i in range(len(M)):
        M[i, i] = 1

    df = pd.DataFrame(M)
    #print(df.values)

    # Utilizing Pandas to remove duplicate rows (and columns, since it's an adjacency matrix)
    dupRemoved = pd.DataFrame.drop_duplicates(df)
    _, idx = np.unique(dupRemoved, axis = 1, return_index = True)
    dupRemoved = dupRemoved.iloc[:, idx]
    dupRemoved.sort_index(axis = 1, inplace = True)
    print("New Shape: ", dupRemoved.shape)
    #print(dupRemoved)
    # Creating the graph from the new matrix with duplicates removed
    G = nx.from_numpy_matrix(dupRemoved.values)
    G = nx.convert_node_labels_to_integers(G, first_label = 1, ordering = 'sorted')
    return G

#Gerating the Universal Set (i.e., set of nodes in the graph)
def computeU():
    G = nx.Graph()
    G = twinRemoval()
    start = time.time()
    U = list(G.nodes())
    print("-------------------------------------------------------")
    print("Finished Generating Universal Set")
    print("Time Taken: {}s".format(time.time() - start))
    print("-------------------------------------------------------")
    return G, U

#Generating the Collection Set (i.e., the set of closed neighborhoods and symmetric differences)
def computeS(G, U):
    numNodes = G.number_of_nodes()
    #nodes = sorted(list(G.nodes))
    pairs = combinations(U, 2)
    S = dict()
    i = 1
    start = time.time()
    for pair in pairs:
        node1 = pair[0]
        node2 = pair[1]
        neighborhood1 = set(list(G.neighbors(node1)))
        neighborhood2 = set(list(G.neighbors(node2)))
        S[i] = neighborhood1.symmetric_difference(neighborhood2)
        i += 1

    for node in U:
        S[i] = set(list(G.neighbors(node)))
        i += 1
    print("-------------------------------------------------------")
    print("Finished Generating Set of Sets")
    print("Time Taken: {}s".format(time.time() - start))
    print("-------------------------------------------------------")

    return S

#Computing the number of times each element in U appears in S
def computeLen(U, S):

    lenU = dict()
    values = S.values()
    for i in U:
        counter = 0
        for value in values:
            if i in value:
                counter += 1
        lenU[i] = counter
    return lenU

#Computing the maximum index of lenU
def getMaxElement(lenU):
    
    maxE = max(lenU, key = lenU.get)
    return maxE

#Compute the indices of S which are to be removed
def findIndices(S, ind):
    indices = []
    for k, v in S.items():
        if ind in v:
            indices.append(k)
    return indices

def main():

    G = nx.Graph()
    G, U = computeU()
    S = computeS(G, U)
    lenU = computeLen(U, S)
    numNodes = G.number_of_nodes()
    
    print("Start")
    copyS = S
    lenS = len(copyS)
    cover = []
    start = time.time()
    while lenS > 0:
        maxE = getMaxElement(lenU)
        #print("Set Covering Maximum Elements = {}".format(ind))
        indices = findIndices(copyS, maxE)
        for i in indices:
            del copyS[i]
        #print("Elements to Remove = {}".format(delElements))
        cover.append(maxE)
        U.remove(maxE)
        lenU = computeLen(U, copyS)
        lenS = len(copyS)
        #print("Resulting Universal Set: {}".format(copyU))
        
        print("Length Remaining: {}".format(lenS))
    
    print("-------------------------------------------------------")
    #print("Cover: {}".format(cover))
    print("Number of Resources Required: {}/{}".format(len(cover), numNodes))
    print("Resources Reduced: {}".format((G.number_of_nodes() - len(cover))/ G.number_of_nodes()))
    print("Time Taken: {}s".format(time.time() - start))
    print("-------------------------------------------------------")


if __name__ == "__main__":
    main()
