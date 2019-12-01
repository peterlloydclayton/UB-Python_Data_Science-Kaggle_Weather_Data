#This is purely a file to contain functions

#Read in the file

#Pass the dataframe, selected city and chosen year.
def avgPerYear(df,year,city):
    avg=df[df['datetime'].str.contains(year)]
    return avg.mean()

#This grabs the years in the df.
#DatetimeIndex is really cool.
dt=list(pd.DatetimeIndex(df['datetime']).year.unique())

#Temperatures in the file are listed in Kelvin
#This converts that. Use the apply method.
def kelvinToFarenheit(data):
    data = data - 273.15
    data *= 1.8
    data += 32
    return data

#Example usage
df['Vancouver']=df['Vancouver'].apply(kelvinToFarenheit).copy()

#Potential drop method
#Just pass the dataframe
def drop(data):
    print("Before:",data.shape)
    data.dropna(how='all',thresh=35,axis=0,inplace=True)
    print("After:",data.shape)

def freqDesc(data,city):
    wc = WordCloud().generate(' '.join(data[city]))
    plt.axis('off')
    return wc

wc=freqDesc(df,'Vancouver')
#Uses matplotlib
plt.imshow(wc)

#This makes a custom dataframe
#It uses all the csvs to pull data into 
#a single dataframe for a chosen city.
#I just got tired of going through 6 different dfs...
def makeDFCity(chosencity):
    df = pd.DataFrame()
    df['Date Time'] = humid['datetime']
    df['Country'] = city['Country'][city.City == chosencity]
    df['Longitude'] = city['Longitude'][city.City == chosencity]
    df['Latitude'] = city['Latitude'][city.City == chosencity]
    df['Pressure'] = pressure[chosencity]
    df['Weather Description'] = weatherDesc[chosencity]
    df['Temp'] = temp[chosencity]
    df['Wind Speed'] = windSPD[chosencity]
    df['Wind Direction'] = windDir[chosencity]
    df['Humid'] = humid[chosencity]
    return df

