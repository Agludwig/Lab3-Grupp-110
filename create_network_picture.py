# baseline tram visualization for Lab 3
# creates by default an SVG image usable on the home page
# this image can then be coloured by using tramviz.py, which operates directly on the SVG file
# You only need to run this file once, to change the URLs of vertices
# rename the resulting file to gbg_tramnet.svg when you have your final version

from trams import readTramNetwork
import graphviz
import json

MY_GBG_SVG = 'D:\\Pythonfiles\\lab3\\tram\\templates\\tram\\images\\my_gbg_tramnet.svg'  
MY_TRAMNETWORK_JSON = 'D:\\PythonFiles\\lab3\\static\\tramnetwork.json' 
TRAM_URL_FILE = 'D:\\PythonFiles\\lab3\\TRAM_URL_FILE.json' 
#Okar absolut inte hålla på med rätt filväg. Inte problemet för nuvarande

gbg_linecolors = {
    1: 'gray', 2: 'yellow', 3: 'blue', 4: 'green', 5: 'red',
    6: 'orange', 7: 'brown', 8: 'purple', 9: 'cyan',
    10: 'lightgreen', 11: 'black', 13: 'pink'}


# compute the scale of the map; you may want to test different heuristics to make map look better
def scaled_position(network):
    minlat, minlon, maxlat, maxlon = network.extreme_position()
    size_x = maxlon - minlon
    scalefactor = len(network)/4  # heuristic
    x_factor = scalefactor/size_x
    size_y = maxlat - minlat
    y_factor = scalefactor/size_y
    
    return lambda xy: (x_factor*(float(xy[0])-minlon), y_factor*(float(xy[1])-minlat))

# create a json file that returns the actual traffic information, and rerun the map creation

def stop_url(stop):
    with open(TRAM_URL_FILE) as file:
        stop_urls = json.loads(file.read())  
          
    return stop_urls.get(stop, '.')


# You don't probably need to change this, if your TramNetwork class uses the same
# method names and types and represents positions as ordered pairs.
# If not, you will need to change the method call to correspond to your class.

def network_graphviz(network, outfile=MY_GBG_SVG, positions=scaled_position):
    dot = graphviz.Graph(engine='fdp', graph_attr={'size': '12,12'})

    for stop in network.get_all_stops():
        
        x, y = network.get_position(stop)
        if positions:
            x, y = positions(network)((x, y))
        pos_x, pos_y = str(x), str(y)
        
        col = 'white'
            
        dot.node(stop, label=stop, shape='rectangle', pos=pos_x + ',' + pos_y +'!',
            fontsize='8pt', width='0.4', height='0.05',
            URL=stop_url(stop),
            fillcolor=col, style='filled')
        
    for line in network.get_all_lines():
        stops = network.get_stops(line)
        for i in range(len(stops)-1):
            dot.edge(stops[i], stops[i+1],
                         color=gbg_linecolors[int(line)], penwidth=str(2))

    dot.format = 'svg'
    s = dot.pipe().decode('utf-8')
    with open(outfile, 'w') as file:
        file.write(s)


if __name__ == '__main__':
    network = readTramNetwork(tramfile=MY_TRAMNETWORK_JSON)
    network_graphviz(network)

"""
# this is how the url json file was created
    import urllib.parse
    dict = {}
    google_url = 'https://www.google.com/search'
    for stop in network.all_stops():
        attrs = urllib.parse.urlencode({'q': 'Gothenburg ' + stop})
        dict[stop] = google_url + '?' + attrs
    with open(TRAM_URL_FILE, 'w') as file:
        json.dump(dict, file, indent=2, ensure_ascii=False)
"""

