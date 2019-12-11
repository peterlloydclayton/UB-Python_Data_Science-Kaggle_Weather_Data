import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, Select, Panel, Tabs
from bokeh.plotting import figure
from bokeh.models.tools import HoverTool

temperature_df = pd.read_csv(r'historical-hourly-weather-data/temperature.csv')
humidity_df = pd.read_csv(r'historical-hourly-weather-data/humidity.csv')
pressure_df = pd.read_csv(r'historical-hourly-weather-data/pressure.csv')


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
        plot.title.text='Weather By {0}'.format(update_criteria)
        plot.yaxis.axis_label = selection_statistical_method.value.title() + ": " + selection_data_set.value

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
        source.data = src.data
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
grouped = get_stat(temperature_df, frequency, statistical_method)
source = ColumnDataSource(grouped)

# Create list of dropdowns
selection_frequency = Select(value=frequency,title='Time Interval',options=intervals)
selection_frequency.on_change('value', update_data_set)

selection_statistical_method = Select(value=statistical_method,title='Statistical Method',options=statistical_options)
selection_statistical_method.on_change('value', update_data_set)

selection_data_set = Select(value=weather_data_value,title='Weather Data Set',options=weather_data_options)
selection_data_set.on_change('value', update_data_set)

# instantiate the plot, the layout, and the tab
plot3 = setup_weather_plot(source, frequency, statistical_method)
l4 = layout([[plot3,selection_data_set,selection_frequency,selection_statistical_method]], sizing_mode='fixed')
tab4 = Panel(child=l4,title="Statistical Operations")
tabs = Tabs(tabs=[tab1])
curdoc().add_root(tabs)
curdoc().title = "Temperature, Pressure & Humidity"
