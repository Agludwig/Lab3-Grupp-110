# visualization of shortest path in Lab 3, modified to work with Django

from .trams import readTramNetwork
from .graphs import dijkstra
from .color_tram_svg import color_svg_network
import os
from django.conf import settings

def tramWork(graph):
    G = readTramNetwork()
    G.clear()
    for i in graph.linelist:
        
        for j in graph.linelist[i].get_stops():
            G.add_vertex((i,j))
    # A separate start node is added for every stop which serves as both start and end.
    # This is so that you can start from any stop without knowing what lines pass it
    for i in graph.stopdict:
        G.add_vertex(("start", i))

    for i in graph.linedict:
        a = True
        for k in graph.linedict[i]:
            if a == False:
                G.add_edge((i, k),(i, graph.linedict[i][graph.linedict[i].index(k)-1]))
            a = False
    
    for i in G.vertices():
        for j in G.vertices():
            if i[1] == j[1] and i != j:
                G.add_edge((i),(j))
    
    return G

def getTime(graph, a, b):
    
    if a[0] == b[0]:
 
        return graph.timedict[a[1]][b[1]]

    else: return 10

def getDist(graph, a, b):
    if a[0] == b[0]:
        return graph.geo_distance(a[1],b[1])
    else: return 0.00018 #Eftersom avstånd räknas i koordinater istället för meter så är 20 m ca 0.00018 grader
#I båda dessa funktioner ignorerar jag tid/avstånd mellan start och giltig station eftersom detta inte påverkar vilken som är snabbast rutt

def show_shortest(dep, dest):
    
    net = readTramNetwork()
    network = tramWork(net)
    
    quickest = dijkstra(network, ("start", dep), getTime)[("start", dest)]
    shortest = dijkstra(network, ("start", dep), getDist)[("start", dest)] 
    
    #Konverterar till lista med enbart stopp
    def route(path):
        route = []
        a = True
        for i in path:
            if a == False:
                if i[1] != path[path.index(i)-1][1]:
                    route.append(i[1])

            else: route.append(i[1])    
            a = False
        return route

        
    quickroute = route(quickest)
    shortroute = route(shortest)

    def colors(v):  
        if v in shortroute and v in quickroute:
            return 'cyan'
        elif v in shortroute:
            return 'green'
        elif v in quickroute:
            return 'orange'
        else: return "white"
       
            
    color_svg_network(colormap=colors)

    return quickroute, shortroute
