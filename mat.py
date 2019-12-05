#https://docs.bokeh.org/en/latest/docs/reference/tile_providers.html
#THis makes a map with given lat and long coords

#Possibly could take min lat and max lat then get min long and max long
# # to produce overall map showing all cities
from bokeh.plotting import figure, show
from bokeh.tile_providers import get_provider, Vendors
tile_provider=get_provider('CARTODBPOSITRON_RETINA')
import math
from ast import literal_eval

def merc(Coords):
    Coordinates = literal_eval(Coords)    
    lat = Coordinates[0]
    lon = Coordinates[1]
    r_major = 6378137.000
    x = r_major * math.radians(lon)
    scale = x/lon
    y = 180.0/math.pi * math.log(math.tan(math.pi/4.0 + 
        lat * (math.pi/180.0)/2.0)) * scale    
    return x, y

x,y=merc('(49.249660,-123.119339)')
p = figure(x_range=(x, x+10000), y_range=(y, y+15000),
            x_axis_type="mercator", y_axis_type="mercator")
p.add_tile(tile_provider)
show(p)