import datetime
from os.path import dirname, join
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column, row, layout
from bokeh.models import ColumnDataSource, DataRange1d, Select, Slider, Tabs, Panel
from bokeh.palettes import Blues4
from bokeh.plotting import figure
import numpy as np
df = pd.read_csv('temperature.csv')
hum = pd.read_csv('humidity.csv')
df.dropna(inplace=True)
hum.dropna(inplace=True)

#This function obtains the humidity data
def get_humid(src,city,year='2016'):
    #Making a copy of the datframe
    olde=(df[df['datetime'].str.contains(str(year))]).copy()
    olde['datetime'] = pd.to_datetime(olde.datetime)
    #Create humid datasource with temperture.
    humid = ColumnDataSource(data=dict(x=hum[city],y=olde[city]))
    return humid

def get_data(src,city,year='2016'):
    #Making a copy of the datframe
    olde=(df[df['datetime'].str.contains(str(year))]).copy()
    #print(olde.head())
    #converting datetime column to datetime
    olde['datetime'] = pd.to_datetime(olde.datetime)
    #From the dataframe, selecting the chosen city.
    #chosen=olde[['datetime',city]]
    #Setting source to chosen city.
    source = ColumnDataSource(data=dict(x=olde['datetime'],y=olde[city]))
    return source

#Build the temperature graph
def makeGraph(source):
    plot = figure(x_axis_type='datetime', plot_width=800,tools="",toolbar_location=None)
    plot.title.text=city
    plot.line(x='x',y='y',line_width=2,color='red',alpha=0.6,source=source)
    plot.yaxis.axis_label="Temperature (F)"
    plot.yaxis.major_label_text_color = 'orange'
    plot.axis.axis_label_text_font_style = "bold"
    return plot

#Build the temp vs humid graphs
def makeTempHumid(humid):
    plot2 = figure(plot_width=800,tools="",toolbar_location=None)
    plot2.scatter(x='x',y='y',color='green',alpha=0.6,source=humid)
    plot2.yaxis.axis_label="Temperature (F)"
    plot2.xaxis.axis_label="Humidity"
    plot2.title.text='Temperature vs Humidity for: ' + str(city)
    plot2.yaxis.major_label_text_color = 'blue'
    plot2.axis.axis_label_text_font_style = "bold"
    return plot2

#update both plots when city is selected
def updatePlot(attr,old,new):
    city = new
    plot.title.text='Temperature for: ' + str(city)
    plot2.title.text='Temperature vs Humidity for: ' + str(city)
    src=get_data(df,city)
    humi=get_humid(df,city)
    humid.data=humi.data
    source.data=src.data

#Update both plots when year is chosen.
def updateYear(attr,old,new):
    print(new)
    year = new
    src=get_data(df,city,year)
    humi=get_humid(df,city,year)
    humid.data=humi.data
    source.data=src.data

#Obtaining the years in the dataset
years=list(pd.DatetimeIndex(df['datetime']).year.unique())
#Creating slider.
yearSlider = Slider(start=np.min(years), end=np.max(years), value=2012, step=1, title="Years")
yearSlider.on_change('value',updateYear)
#Default value
city='Vancouver'
year='2012'
#Creating a list of cities from df
cities=df.columns.values[1:]
cities=[x for x in cities]

#Selection box
selection = Select(value=city,title='City',options=cities)
source = get_data(df,city)
humid=get_humid(df,city)
plot = makeGraph(source)
plot2 = makeTempHumid(humid)
selection.on_change('value',updatePlot)

l1 = layout([[plot,selection,yearSlider],[plot2]], sizing_mode='fixed')
#l2 = layout([[fig3]],sizing_mode='fixed')
tab1 = Panel(child=l1,title="Temperature vs Year")
tabs = Tabs(tabs=[ tab1 ])
curdoc().add_root(tabs)
curdoc().title = "Temperature"
