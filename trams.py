
from .graphs import *
from .tramdata import *
import json
import os
from django.conf import settings
#identical to lab 2 except the imports and TRAM_FILE
class TramStop:
    def __init__(self, name, lines, pos):
        self.name = name
        self.lines = lines
        self.pos = pos
    def get_name(self):
        return self.name
    
    def get_position(self):
        
        return self.pos
    
    def set_position(self, lat, lon):
        self.pos = (lat, lon)

    def get_lines(self):
        return self.lines
    
    def add_line(self, line):
        self.lines.append(line)
    

class TramLine:
    def __init__(self, line, stops):
        self.line = line
        self.stops = stops
    def get_number(self):
        return self.line
    
    def get_stops(self):
        return self.stops


class TramNetwork(WeightedGraph):
    def __init__(self, stopdict,linedict,timedict, start=None):
        super().__init__(start)
        self.stoplist = {}
        self.linelist = {}
        self.linedict = linedict
        self.stopdict = stopdict
        self.timedict = timedict
        
        for i in stopdict:
            
            j = TramStop(i,lines_via_stop(linedict,i),(stopdict[i]["lat"], stopdict[i]["lon"])) #Skapar och sätter rätt variabler

            self.stoplist[i] = j

            self.add_vertex(i)
           

        for i in linedict:
            j = TramLine(i, linedict[i])

            self.linelist[i] = j

            a = True

            for k in linedict[i]:
                if a == False:
                    self.add_edge(k,linedict[i][linedict[i].index(k)-1])
                a = False
        for i in timedict:

            for j in timedict[i]:

                self.set_weight(i,j,timedict[i][j])


    def get_position(self, stop):

        return self.stoplist[stop].get_position()
    
    def extreme_position(self):
        lonlist = []
        latlist = []
        
        for i in self.stoplist:
            lonlist.append(float(self.stoplist[i].get_position()[1]))
            latlist.append(float(self.stoplist[i].get_position()[0]))
        
        return [max(lonlist), min(lonlist), max(latlist), min(latlist)]

        
    def transition_time(self, stop1, stop2):

        return self.get_weight(stop1,stop2)
    
    def geo_distance(self, stop1, stop2):
        
        return distance_between_stops(self.stopdict, stop1, stop2)

    def get_lines(self, stop):
        
        return self.stoplist[stop].get_lines()

    def get_stops(self, line):
        
        return self.linelist[line].get_stops()

    def get_all_stops(self):
        return self.stoplist
    
    def get_all_lines(self):
        return self.linelist

TRAM_FILE = os.path.join(settings.BASE_DIR,
                        'static/tramnetwork.json')



def readTramNetwork(tramfile=TRAM_FILE):
    with open (tramfile) as file:
        file_ = json.load(file)
        linedict = file_["lines"]
        stopdict = file_["stops"]
        timedict = file_["times"]
        G = TramNetwork(stopdict,linedict,timedict)

    return G
