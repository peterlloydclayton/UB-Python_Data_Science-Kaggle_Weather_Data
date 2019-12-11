import datetime
from math import pi
import numpy as np
from os.path import dirname, join
import pandas as pd
from bokeh.transform import factor_cmap
from bokeh.io import curdoc
from bokeh.layouts import column, row, layout
from bokeh.models import ColumnDataSource, DataRange1d, Select, Slider, Tabs, Panel,FactorRange
from bokeh.plotting import figure
from bokeh.palettes import Turbo256, Spectral11,Reds9,RdYlGn11,Blues4
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure, show
from bokeh.tile_providers import get_provider, Vendors
tile_provider=get_provider('CARTODBPOSITRON_RETINA')
import math
from ast import literal_eval
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn

### csv imports

df = pd.read_csv('temperature.csv')
hum = pd.read_csv('humidity.csv')
countries=pd.read_csv('city_attributes.csv')
pressure = pd.read_csv('pressure.csv')
weatherDesc = pd.read_csv('weather_description.csv')
windDir = pd.read_csv('wind_direction.csv')
windSPD = pd.read_csv('wind_speed.csv')

#Dropping values
df.dropna(inplace=True,how='all')
hum.dropna(inplace=True,how='all')
countries.dropna(inplace=True,how='all')
pressure.dropna(inplace=True,how='all')
weatherDesc.dropna(inplace=True,how='all')
windDir.dropna(inplace=True,how='all')
windSPD.dropna(inplace=True,how='all')

#Convert Kelvin to farenheit
def kelvinToFarenheit(data):
    data = data - 273.15
    data *= 1.8
    data += 32
    return data

#Applying the conversion
cit = list(df.columns[1:])
for x in cit:
    df[x] = kelvinToFarenheit(df[x])

#This function obtains the humidity data
def get_humid(src,city):
    #Making a copy of the datframe
    #olde=(df[df['datetime'].str.contains(str(year))]).copy()
    global year 
    global month
    olde = df.copy()
    olde['datetime'] = pd.to_datetime(olde.datetime)
    olde = olde[pd.DatetimeIndex(olde['datetime']).year == year]
    olde = olde[pd.DatetimeIndex(olde['datetime']).month == month]

    #Create humid datasource with temperture.
    humid = ColumnDataSource(data=dict(x=hum[city],y=olde[city]))
    return humid

#Obtains the temp data for given year and month
def get_data(src,city):
    global year
    global month
    #converting datetime column to datetime
    olde=df.copy()
    olde['datetime'] = pd.to_datetime(olde.datetime)
    olde = olde[pd.DatetimeIndex(olde['datetime']).year == year]
    olde = olde[pd.DatetimeIndex(olde['datetime']).month == month]

    #Setting source to chosen city.
    source = ColumnDataSource(data=dict(x=olde['datetime'],y=olde[city]))
    return source

#Build the temperature graph
def makeGraph(source):
    plot = figure(x_axis_type='datetime', plot_width=600,tools="hover", tooltips="@y(F)",toolbar_location=None)
    plot.title.text=city
    plot.line(x='x',y='y',line_width=2,color='red',alpha=0.6,source=source)
    plot.yaxis.axis_label="Temperature (F)"
    plot.yaxis.major_label_text_color = 'orange'
    plot.axis.axis_label_text_font_style = "bold"
    plot.xaxis.axis_label="Time Range"

    return plot

#Build the temp vs humid graphs
def makeTempHumid(humid):
    plot2 = figure(plot_width=800,tools="hover", tooltips="@x(%):@y(F)",toolbar_location=None)
    plot2.scatter(x='x',y='y',color='green',alpha=0.6,source=humid)
    plot2.yaxis.axis_label="Temperature (F)"
    plot2.xaxis.axis_label="Humidity (%)"
    plot2.title.text='Temperature vs Humidity for: ' + str(city)
    plot2.yaxis.major_label_text_color = 'blue'
    plot2.axis.axis_label_text_font_style = "bold"
    return plot2

#update both plots when city is selected
def updatePlot(attr,old,new):
    global city,year,month
    city = new
    plot.title.text='Temperature for: ' + str(city) +" Year: "+str(year)+" Month: "+str(month)
    plot2.title.text='Temperature vs Humidity for: ' + str(city) +" Year: "+str(year)+" Month: "+str(month)
    src=get_data(df,city)
    humi=get_humid(df,city)
    humid.data=humi.data
    source.data=src.data

#Update both plots when year is chosen.
def updateYear(attr,old,new):
    global year
    global city
    global month
    year = new
    plot.title.text='Temperature for: ' + str(city) +" Year: "+str(year)+" Month: "+str(month)
    plot2.title.text='Temperature vs Humidity for: ' + str(city) +" Year: "+str(year)+" Month: "+str(month)
    src=get_data(df,city)
    humi=get_humid(df,city)
    humid.data=humi.data
    source.data=src.data

#update both plots when month is chosen
def updateMonth(attr,old,new):
    global year
    global city
    global month
    month = new 
    plot.title.text='Temperature for: ' + str(city) +" Year: "+str(year)+" Month: "+str(month)
    plot2.title.text='Temperature vs Humidity for: ' + str(city) +" Year: "+str(year)+" Month: "+str(month)
    src=get_data(df,city)
    humi=get_humid(df,city)
    humid.data=humi.data
    source.data=src.data

#Obtaining the years in the dataset
years=list(pd.DatetimeIndex(df['datetime']).year.unique())
months=list(pd.DatetimeIndex(df['datetime']).month.unique())

#Creating slider.
yearSlider = Slider(start=np.min(years), end=np.max(years), value=2012, step=1, title="Years")
yearSlider.on_change('value',updateYear)

#Global variables
global city
global year
global month
#Setting default values
city='Vancouver'
year=2012
month=1

####### Build bar chart of heat #######

def heatData(df):
    #Making a copy of the datframe
    test = dict()
    hot=[]
    locations = list(df.columns[1:])
    for x in locations:
        test[x] = np.max(df[x])
        hot.append(np.max(df[x]))
   
    #Create humid datasource with temperture.
    src = ColumnDataSource(data=dict(x=locations,y=hot))
    return src

# temps recorded across all years hstack
# def yearHeat(attribs,df,place):
#     yearlyTemp = []
#     yrs = {}

#     locations=list(attribs['City'][attribs['Country'] == 'Israel'])

#     #Got all years
#     yr = list(pd.DatetimeIndex(df['datetime']).year.unique())
#     stringYr =[]
#     yup = []
#     for y in yr:
#         stringYr.append(str(y))
        
#     for y in yr:
#         for loc in locations:
#             yearlyTemp.append(np.max(df[loc][pd.DatetimeIndex(df['datetime']).year == y]))
#         yrs[str(y)]=yearlyTemp
#         yearlyTemp = []

#     x = [(loc,str(y)) for loc in locations for y in yr ]
#     stack = sum(zip(yrs['2012'],yrs['2013'],yrs['2014'],yrs['2015'],yrs['2016'],yrs['2017']),())
#     source = ColumnDataSource(data=dict(x=x,stack=stack))
#     plot = figure(x_range=FactorRange(*x),plot_width=1400, plot_height=400,title='temp by year')
#     plot.vbar(x='x',top='stack',width=1.2,source=source)
#     plot.y_range.start=0
#     plot.x_range.range_padding=0
#     plot.xgrid.grid_line_color = None
#     plot.xaxis.major_label_orientation = pi/2
#     plot.xaxis.group_label_orientation = pi/4
#     return plot,source

def heatGraph(df):
    test = dict()
    hot=[]
    locations = list(df.columns[1:])
    for x in locations:
        test[x] = np.max(df[x])
        hot.append(np.max(df[x]))
   
    #Create humid datasource with temperture.
    src = ColumnDataSource(data=dict(x=locations,y=hot))
    data = {
        'locations':locations,

    }
    p = figure(x_range=locations,plot_width=1000,toolbar_location=None,title='Hottest temps for each city recorded.',tools="hover", tooltips="@x:@y(F)")
    p.vbar(x='x',top='y', width=0.9, source=src,fill_color=factor_cmap('x',palette=Turbo256,factors=locations))
    p.xaxis.major_label_orientation = pi/4
    p.xgrid.grid_line_color = None
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"
    p.axis.axis_label_text_font_style = "bold"
    p.yaxis.axis_label="Temperature (F)"
    p.xaxis.axis_label="Cities"

    # p.legend.orientation = "horizontal"
    # p.legend.location = "top_center"
    return p

monthSlider = Slider(start=np.min(months),end=np.max(months),value=np.min(months),step=1,title="Months")
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
monthSlider.on_change('value',updateMonth)
dat=heatData(df)

plotty = heatGraph(df)

#### Data table #####


#Geoplotting data
# def updateMerc(Coords):
#     Coordinates = literal_eval(Coords)    
#     lat = Coordinates[0]
#     lon = Coordinates[1]
#     r_major = 6378137.000
#     x = r_major * math.radians(lon)
#     scale = x/lon
#     y = 180.0/math.pi * math.log(math.tan(math.pi/4.0 + 
#         lat * (math.pi/180.0)/2.0)) * scale   
#     p = figure(x_range=(x, x+10000), y_range=(y, y+15000),
#                 x_axis_type="mercator", y_axis_type="mercator")
#     p.add_tile(tile_provider)


# def updateCrazy(attr,old,new):
#     global place
#     place = new
#     plot,src=yearHeat(countries,df,place)
#     source.data=src.data

#Make a custom dataframe from all datasets
def makeDFCity(chosencity):
    newDF = pd.DataFrame()
    newDF['Date Time'] = hum['datetime']
    newDF['Country'] = countries['Country'][countries.City == chosencity]
    newDF['Longitude'] = countries['Longitude'][countries.City == chosencity]
    newDF['Latitude'] = countries['Latitude'][countries.City == chosencity]
    newDF['Pressure'] = pressure[chosencity]
    newDF['Weather Description'] = weatherDesc[chosencity]
    newDF['Temp'] = df[chosencity]
    newDF['Wind Speed'] = windSPD[chosencity]
    newDF['Wind Direction'] = windDir[chosencity]
    newDF['Humid'] = hum[chosencity]
    newDF.dropna(thresh=4,inplace=True)
    newDF.replace(np.NaN,'Missing',inplace=True)

    return newDF


global place, tough
place= 'Denver'
country = countries['Country'].values
country = set(country)
country = list(country)
#plug,src=yearHeat(countries,df,place)
tough = makeDFCity(place)
cols = tough.columns
toughSource = ColumnDataSource(tough)
Columns = [TableColumn(field=Ci, title=Ci) for Ci in cols] # bokeh columns
data_table = DataTable(columns=Columns, source=toughSource,width=1000) # bokeh table


####Updaters####

def updateTable(attr,old,new):
    global place
    global tough
    place = new
    src=ColumnDataSource(data=makeDFCity(place))
    toughSource.data=src.data
    
###Selections#####

sel = Select(value=place,title='City',options=cities)
sel.on_change('value',updateTable)

####Peter#######
# process filters for year and or city
def process_data_filters(data, city_filter, year_filter):
    filtered_data = data
    if city_filter == 'all':
        pass
    else:
        filtered_data = filtered_data[filtered_data['City'] == city_filter]
    if year_filter == 'all':
        pass
    else:
        filtered_data = filtered_data.loc[filtered_data['datetime'].dt.year == year_filter]
    return filtered_data


# Apply the appropriate statistical method to the data
def use_statistical_method(data, stat_method):
    processed_data = data
    print("processed data before:", processed_data)
    if stat_method == 'average':
        processed_data = processed_data.mean()
    elif stat_method == 'standard':
        processed_data = processed_data.std()
    elif stat_method == 'variance':
        processed_data = processed_data.var()
    print("processed data after: ", processed_data)
    return processed_data


def get_stat(src,date_frequency,stat_method,city='all',year='all'):
    src['datetime'] = pd.to_datetime(src['datetime'])
    weather_melt = pd.melt(src,id_vars='datetime',var_name='City',value_name='statistical_method')
    weather_melt = process_data_filters(weather_melt, city, year)
    weather_melt = weather_melt.groupby(pd.Grouper(key='datetime', freq=date_frequency))
    weather_melt = use_statistical_method(weather_melt, stat_method)
    return weather_melt


# Create The Main Plot
def setup_weather_plot(src, date_frequency, stat_method):
    mg_plot = figure(x_axis_type='datetime', plot_width=500,toolbar_location='right')
    mg_plot.title.text='Weather: ' + selection_data_set.value + ' {0}'.format(date_frequency)
    mg_plot.line(x='datetime', y='statistical_method', source=src, line_width=2)
    mg_plot.xaxis.axis_label='Year by: {0}'.format(date_frequency)
    mg_plot.xaxis.major_label_text_color = 'blue'
    mg_plot.yaxis.axis_label=stat_method.title() + ": " + selection_data_set.value
    mg_plot.yaxis.major_label_text_color = 'blue'
    mg_plot.axis.axis_label_text_font_style = "bold"
    return mg_plot


# update time based frequency of data: yearly, monthly, quarterly, etc.
def update_data_set(attr, old, new):
    try:
        update_criteria = new
        main_data_set = pd.DataFrame()
        plot3.title.text='Weather By {0}'.format(update_criteria)
        plot3.yaxis.axis_label = selection_statistical_method.value.title() + ": " + selection_data_set.value

        if update_criteria == 'Temperature':
            main_data_set = df
        elif update_criteria == 'Humidity':
            main_data_set = hum
        elif update_criteria == 'Pressure':
            main_data_set = pressure
        else:  # This code executes if the data set is not changing: example: frequency, or the statistical method
            if selection_data_set.value == 'Temperature':
                print("frequency or statistical method called!: Temperature")
                main_data_set = df
            elif selection_data_set.value == 'Humidity':
                print("frequency or statistical method called!: Humidity")
                main_data_set = hum
            elif selection_data_set.value == 'Pressure':
                print("frequency or statistical method called!: Pressure")
                main_data_set = pressure

        # update the data for the graph
        cds_data_set = get_stat(main_data_set, selection_frequency.value,selection_statistical_method.value)
        src = ColumnDataSource(cds_data_set)
        sourcy.data = src.data
    except Exception as ex:
        print(ex)

# set initial values for the plot
frequency = 'M'
weather_data_value = 'Temperature'
statistical_method = 'standard'

# set initial values for the dropdown
# Selection box criteria
intervals = ['Y','Q','M','W','D','H']
weather_data_options = ['Temperature','Humidity','Pressure']
statistical_options = ['average','standard','variance']

# Create the initial source for the plot
grouped = get_stat(df, frequency, statistical_method)
sourcy = ColumnDataSource(grouped)

# Create list of dropdowns
selection_frequency = Select(value=frequency,title='Time Interval',options=intervals)
selection_frequency.on_change('value', update_data_set)

selection_statistical_method = Select(value=statistical_method,title='Statistical Method',options=statistical_options)
selection_statistical_method.on_change('value', update_data_set)

selection_data_set = Select(value=weather_data_value,title='Weather Data Set',options=weather_data_options)
selection_data_set.on_change('value', update_data_set)

# instantiate the plot, the layout, and the tab
plot3 = setup_weather_plot(sourcy, frequency, statistical_method)



####################

####DIANA#####



global country_list 
global city_list
global chosenCountry
global weatherDescriptions
global weatherSource

#Create custom dataframe with windspeed max vals
def city_windSPD():
    max_ws=windSPD.max()
    df2=pd.DataFrame()
    df2['City']=countries['City']
    df2['Country'] = countries['Country']
    df2=df2.assign(Max=windSPD.iloc[:,1:].max().values)
    return df2

#Defaults
selectedCity = 'Vancouver'
#Obtain df
value= city_windSPD()
#Convert to ColumnDataSource
sourcer=ColumnDataSource(data=value)
#Make country and city lists
country_list=list(set(value['Country']))
city_list = list(value['City'])

#Create graph of windspeed
def graphWindSpeed():
    global city_list
    pl=figure(
    y_range=city_list,
    plot_width=800,
    plot_height=600,
    title='Weather play with the country',
    x_axis_label='WindSpeed Max Value',
    tools=""
    )

    pl.hbar(
        y='City',
        right='Max',
        left=0,
        height=0.4,
        color='red',
        fill_alpha=0.9,
        source=sourcer
    )

    return pl

#Get max windspeed for citites of given country
def getData(city):
    global chosenCountry
    chosenCountry = city
    max_ws=windSPD.max()
    df=pd.DataFrame()
    df['City']=countries['City']
    df['Country'] = countries['Country']
    df=df.assign(Max=windSPD.iloc[:,1:].max().values)
    return df[df['Country'] == city]

#Update method for windspeed to reflect new country chosen
def updateThePlot(attr,old,new):
    global chosenCountry
    chosenCountry = new
    plot.title.text='Weather play with the city: ' + str(chosenCountry)
    src=getData(chosenCountry)
    src=ColumnDataSource(data=src)
    sourcer.data=src.data

#Get cities of given country with given weather description
def city_weather(country,weather):
    #Gets sum values of given weatherdesc per column
    wd_clear=weatherDesc.isin([weather]).sum()
    wd_clear.drop('datetime',inplace=True)
    #Making new dataframe
    df=pd.DataFrame()
    #passing values to df
    df = countries[['City','Country']]
    df=df.assign(weather=wd_clear.values)
    #Getting cities of chosen country
    count=countries[countries['Country']==country]
    df=df[df['Country'] == country]
    return df

#Defaults
vals=city_weather('Israel','sky is clear')
weatherSource=ColumnDataSource(vals)

#Build weather description graph
def descGraph():
    global weatherSource
    global city_list
    pp=figure(
    y_range=city_list,
    plot_width=800,
    plot_height=600,
    title='Weather play with the city',
    x_axis_label='weather count',
    tools="pan,box_select,zoom_in,zoom_out,save,reset"
    )
    pp.hbar(
        y='City',
        right='weather',
        left=0,
        height=0.4,
        color='green',
        fill_alpha=0.9,
        source=weatherSource
    )
    return pp

#Update weather description
def descUpdate(attr,old,new):
    global chosenCountry
    global chosenWeather
    if(new in weatherDescriptions):
        chosenWeather = new
    else:
        chosenCountry = new
    descPlot.title.text='Weather play with the city: ' + str(chosenCountry) + " with weather description: "+str(chosenWeather)
    src=city_weather(chosenCountry,chosenWeather)
    src=ColumnDataSource(data=src)
    weatherSource.data=src.data

#Call the graphs
descPlot = descGraph()
windPlot = graphWindSpeed()
#Make a list of weather descriptions
weatherDescriptions = list(weatherDesc['Vancouver'].dropna().unique())
#Default values for selectors
chosenCountry = 'Israel'
chosenWeather = 'light rain'
#Select drop down
selected = Select(value=chosenCountry,title='Country',options=country_list)
weatherCountrySelect = Select(value=chosenCountry,title='Country',options=country_list)
weatherDescSelect = Select(value=chosenWeather,title='Weather Description',options=weatherDescriptions)


#Selection updates
weatherCountrySelect.on_change('value',descUpdate)
weatherDescSelect.on_change('value',descUpdate)
selected.on_change('value',updateThePlot)
########################


#Arranging layouts to display
inputs = column(selection,yearSlider,monthSlider)
input2 = column(sel)
input3=column(selection_data_set,selection_frequency,selection_statistical_method)
input4=column(weatherCountrySelect,weatherDescSelect)
input5=column(selected)

l1 = layout([[plot,inputs],[plot2]], sizing_mode='fixed')
l2 = layout([[plotty]],sizing_mode='fixed')
l3 = layout([[data_table],[sel]],sizing_mode='fixed')
l4 = layout([[plot3,input3]], sizing_mode='fixed')
l5= layout([[descPlot,input4]])
l6=layout([[windPlot,input5]])
#Creating tabbed layout for ease
tab1 = Panel(child=l1,title="Temperature vs Year")
tab2 = Panel(child=l2,title="Highest Heat")
tab3 = Panel(child=l3,title="Datatable")
tab4 = Panel(child=l4,title="Statistical Operations")
tab5 = Panel(child=l5,title='Weather Description Frequency')
tab6 = Panel(child=l6,title='Wind Speed')

#Adding all tabs
tabs = Tabs(tabs=[ tab1,tab2,tab3,tab4,tab5,tab6 ])
curdoc().add_root(tabs)
curdoc().title = "Weather Dataset"