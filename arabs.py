import pandas as pd
import plotly.express as px
from plotly.offline import plot 

###Reading the data from the database
COVID_CONFIRMED_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
COVID_DEATHS_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
COVID_RECOVERED_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

covidConfirmed = pd.read_csv(COVID_CONFIRMED_URL)
covidDead = pd.read_csv(COVID_DEATHS_URL)
covidRecovered = pd.read_csv(COVID_RECOVERED_URL)


###Cleaning the data

#Won't be using the province/state column so I deleted them
del covidConfirmed["Province/State"]
del covidDead["Province/State"]
del covidRecovered["Province/State"]

#Getting rid of all the non-arab countries
for i in range(len(covidConfirmed)): 
  if(not(covidConfirmed.loc[i, "Country/Region"]) in ("Algeria" , "Bahrain" , "Comoros" , "Djibouti" , "Egypt" , "Iraq" , "Jordan" , "Kuwait" , "Lebanon" , "Libya" , "Mauritania" , "Morocco" , "Oman" , "Qatar" , "Saudi Arabia" , "Somalia" , "Sudan" , "Syria" , "Tunisia" , "United Arab Emirates" , "Yemen")):
    covidConfirmed = covidConfirmed.drop(index=i)
    covidDead = covidDead.drop(index=i)

for i in range(len(covidRecovered)): 
  if(not(covidRecovered.loc[i, "Country/Region"]) in ("Algeria" , "Bahrain" , "Comoros" , "Djibouti" , "Egypt" , "Iraq" , "Jordan" , "Kuwait" , "Lebanon" , "Libya" , "Mauritania" , "Morocco" , "Oman" , "Qatar" , "Saudi Arabia" , "Somalia" , "Sudan" , "Syria" , "Tunisia" , "United Arab Emirates" , "Yemen")):
    covidRecovered = covidRecovered.drop(index=i)

covidConfirmed = covidConfirmed.reset_index(drop=True)
covidDead = covidDead.reset_index(drop=True)
covidRecovered = covidRecovered.reset_index(drop=True)

#Making sure there are no empty cells by filling them with 0's
covidConfirmed.fillna(0, inplace=True)
covidDead.fillna(0, inplace = True)
covidRecovered.fillna(0, inplace = True)

###Creating a dataframe that has the total number for each country
country = []
confirmed = []
dead = []
recovered = []
active = []
mortality = []

for i in range(len(covidConfirmed)) : 
  country.append(covidConfirmed.loc[i,"Country/Region"])
  confirmed.append(covidConfirmed.iloc[i, 3:].max())
  dead.append(covidDead.iloc[i, 3:].max())

for i in range(len(covidRecovered)) : 
  recovered.append(covidRecovered.iloc[i, 3:].max())

for i in range(len(confirmed)) : 
  active.append(confirmed[i] - dead[i] - recovered[i])
  mortality.append(round(dead[i]/confirmed[i]*100,2))


arabDf = pd.DataFrame({
      'Country' : country,
      'Confirmed' : confirmed,
      'Dead' : dead,
      'Recovered' : recovered,
      'Active' : active,
      'Mortality Rate' : mortality
    })    

###Converting the data to the long version
arabLongDf = arabDf.melt(id_vars=['Country'], 
                        value_vars =['Active', 'Dead', 'Recovered'],
                        var_name="Status", 
                        value_name ="Count")
###Plotting the treemap
treemapFigure = px.treemap(arabLongDf, path=["Country", "Status"], 
                                  values="Count", 
                                  title="COVID-19 in the Arab World", 
                                  template='plotly_dark')
treemapFigure.data[0].textinfo = 'label+text+value'

#Changing the font and putting the title in the centre
treemapFigure.update_layout(
    font_family="Courier New",
    title_font_family="Times New Roman",
    font=dict(
      family = 'Times New Roman, Courier New',
      size = 15
    ),
    title={
      'y':0.95,
      'x':0.5,
      'xanchor': 'center',
      'yanchor': 'top',
    }
)

plot(treemapFigure, filename='treemap.html')


###Plotting a bar graph to show the Mortality rate in the arab world
barFigure = px.bar(arabDf.sort_values(by='Mortality Rate', ascending=True),
             x="Mortality Rate", y="Country",
             title='Mortality Rate of the Arab World per 100', text='Mortality Rate',
             template='plotly_dark', orientation='h'
             )

barFigure.update_traces(marker_color='#e74c3c', textposition='outside')

#Changing the font and putting the title in the centre
barFigure.update_layout(
    font_family="Courier New",
    title_font_family="Times New Roman",
    font=dict(
      family = 'Times New Roman, Courier New',
      size = 15
    ),
    title={
      'y':0.95,
      'x':0.5,
      'xanchor': 'center',
      'yanchor': 'top',
    }
)

plot(barFigure, filename='barChart.html')

###Adding up all the numbers of all the Arab countries combined
totalArabDf = pd.DataFrame({
  'Confirmed' : [arabDf.iloc[:, 1].sum()],
  'Dead' : [arabDf.iloc[:, 2].sum()],
  'Recovered' : [arabDf.iloc[:, 3].sum()],
  'Active' : [arabDf.iloc[:, 4].sum()] 
})
###Converting to the long version
totalArabLongDf = totalArabDf.melt(value_vars=['Active', 'Dead', 'Recovered'],
                              var_name="Status",
                              value_name="Count")
###Plotting a pie chart of the totals
pieFigure = px.pie(totalArabLongDf, values='Count', 
                                    names='Status',
                                    title='COVID-19 Cases In the Arab World',
                                    template='plotly_dark')

colors = ['#3498db','#e74c3c','#2ecc71']

pieFigure.update_traces(hoverinfo='value', textinfo='percent+label', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))

#Changing the font and putting the title in the centre                  
pieFigure.update_layout(
    font_family="Courier New",
    title_font_family="Times New Roman",
    font=dict(
      family = 'Times New Roman, Courier New',
      size = 15
    ),
    title={
      'y':0.95,
      'x':0.5,
      'xanchor': 'center',
      'yanchor': 'top',
    }
)
plot(pieFigure, filename='pieChart.html')


###Converting the confirmed cases datafram to a long version
confirmedLongDf = covidConfirmed.melt(id_vars=covidConfirmed.iloc[:,:3], 
                        var_name='date', 
                        value_vars =covidConfirmed.iloc[:,3:],
                        value_name ='Confirmed cases')

###Plotting a scatter map
scatterFigure = px.scatter_geo(confirmedLongDf,
                     lat="Lat", lon="Long", color="Country/Region",
                     hover_name="Country/Region", size="Confirmed cases",
                     size_max=50, animation_frame="date",
                     template='plotly_dark', projection="natural earth",
                     title="COVID-19 Arab World Confirmed Cases Over Time")
#Changing the font and putting the title in the centre
scatterFigure.update_layout(
    font_family="Courier New",
    title_font_family="Times New Roman",
    font=dict(
      family = 'Times New Roman, Courier New',
      size = 15
    ),
    title={
      'y':0.95,
      'x':0.5,
      'xanchor': 'center',
      'yanchor': 'top',
    }
)

plot(scatterFigure, filename='scatterMap.html')