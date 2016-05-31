'''
This module handles the graph operations and visualizations using the networkx library.

Usage: For a Graph object g, g.most_central(F,centrality_type) will return a subgraph of g which has nodes with centrality > F*(mean centrality of all nodes)

Author: Prithvijit Chakrabarty (prithvichakra@gmail.com)
'''

from __future__ import division
from matplotlib import pyplot as plt
import networkx as nx
import copy

class Graph:
    def __init__(self,adj,labels):
        self.adj = adj
        self.char_list = labels
        self.lab = dict(enumerate(labels))
        self.G = nx.from_numpy_matrix(adj)

    #Return the most central nodes. These have 
    def most_central(self,F=1,cent_type='betweenness'):
        if cent_type == 'betweenness':
            ranking = nx.betweenness_centrality(self.G).items()
        elif cent_type == 'closeness':
            ranking = nx.closeness_centrality(self.G).items()
        elif cent_type == 'eigenvector':
            ranking = nx.eigenvector_centrality(self.G).items()
        elif cent_type == 'harmonic':
            ranking = nx.harmonic_centrality(self.G).items()
        elif cent_type == 'katz':
            ranking = nx.katz_centrality(self.G).items()
        elif cent_type == 'load':
            ranking = nx.load_centrality(self.G).items()
        elif cent_type == 'degree':
            ranking = nx.degree_centrality(self.G).items()
        ranks = [r for n,r in ranking]
        cent_dict = dict([(self.lab[n],r) for n,r in ranking])
        m_centrality = sum(ranks)
        if len(ranks) > 0:
            m_centrality = m_centrality/len(ranks)
        #Create a graph with the nodes above the cutoff centrality- remove the low centrality nodes
        thresh = F*m_centrality
        lab = {}
        for k in self.lab:
            lab[k] = self.lab[k]
        g = Graph(self.adj.copy(),self.char_list)
        for n,r in ranking:
            if r < thresh:
                g.G.remove_node(n)
                del g.lab[n]
        return (cent_dict,thresh,g)

    #Displays the graph visualization
    def show(self):
        pos = nx.spring_layout(self.G)
        nx.draw_networkx_nodes(self.G,pos,alpha=0.5)
        
        edge_weights = dict([((u,v),int(d['weight'])) for u,v,d in self.G.edges(data=True)])
        nx.draw_networkx_labels(self.G,pos,self.lab,alpha=0.5)
        nx.draw_networkx_edges(self.G,pos,alpha=0.5)

        plt.show()
