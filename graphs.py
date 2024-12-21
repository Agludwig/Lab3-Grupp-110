import networkx as nx

import graphviz as gr

#Enda skillnad från lab2 var att jag satte ett extra argument på cost() för att göra det enklare att beräkna på rad 46.

class Graph(nx.Graph):
    def __init__(self, start=None):
        super().__init__(start)
        
    def add_vertex(self,a):
        
        self.add_node(a)
    
    def vertices(self):
        return self.nodes()

    def neighbours(self, v):
        return list(self.neighbors(v))
    def remove_vertex(self,b):
        
        self.remove_node(b)

    def get_vertex_value(self,v):
        return self.nodes[v]
    def set_vertex_value(self,v,x):
        self.nodes[v]["location"] = x
  

class WeightedGraph(Graph):
    def __init__(self,start = None):
        super().__init__(start)
        
    def get_weight(self,a,b):
        return self[a][b]["weight"]
    def set_weight(self,a,b,w):
        self[a][b]["weight"] = w

def dijkstra(graph, source, cost=lambda u,v: 1):
    costs2attributes(graph, cost, attr='weight')
    
    return nx.shortest_path(graph, source, weight="weight")

def costs2attributes(G, cost, attr='weight'):
    for a, b in G.edges():
        G[a][b][attr] = cost(G,a, b)
        

