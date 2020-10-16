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


country = []
lat = []
long = []
confirmed = []
dead = []
recovered = []
active = []

for i in range(len(covidConfirmed)) : 
  country.append(covidConfirmed.loc[i,"Country/Region"])
  confirmed.append(covidConfirmed.iloc[i, 3:].max())
  dead.append(covidDead.iloc[i, 3:].max())

for i in range(len(covidRecovered)) : 
  recovered.append(covidRecovered.iloc[i, 3:].max())

for i in range(len(confirmed)) : 
  active.append(confirmed[i] - dead[i] - recovered[i])

arabDf = pd.DataFrame({
      'Country' : country,
      'Confirmed' : confirmed,
      'Dead' : dead,
      'Recovered' : recovered,
      'Active' : active
    })    


arabLongDf = arabDf.melt(id_vars=['Country'], 
                        value_vars =['Active', 'Dead', 'Recovered'],
                        var_name="Status", 
                        value_name ="Count")

treemapFigure = px.treemap(arabLongDf, path=["Country", "Status"], 
                                  values="Count", 
                                  # color = 'Status',
                                  # color_discrete_map={'(?)':'random', 'Active':'#3498db', 'Dead':'#e74c3c', 'Recovered':'#2ecc71'},
                                  title="COVID-19 In the Arab countries", 
                                  template='plotly_dark')
treemapFigure.data[0].textinfo = 'label+text+value'

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



###Adding up all the confirmed, dead and recovered cases

totalArabDf = pd.DataFrame({
  'Confirmed' : [arabDf.iloc[:, 1].sum()],
  'Dead' : [arabDf.iloc[:, 2].sum()],
  'Recovered' : [arabDf.iloc[:, 3].sum()],
  'Active' : [arabDf.iloc[:, 4].sum()] 
})

totalArabLongDf = totalArabDf.melt(value_vars=['Active', 'Dead', 'Recovered'],
                              var_name="Status",
                              value_name="Count")

pieFigure = px.pie(totalArabLongDf, values='Count', 
                                    names='Status',
                                    title='COVID-19 In the Arab countries',
                                    template='plotly_dark')

colors = ['#3498db','#e74c3c','#2ecc71']

pieFigure.update_traces(hoverinfo='value', textinfo='percent+label', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
                  
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


plot(pieFigure, filename='pie_chart.html')



# arabConfirmedLongDf = arabDf.melt(id_vars=['Country'], 
#                         value_vars =['Lat', 'Long', 'Confirmed'],
#                         var_name="Status", 
#                         value_name ="Count")

# scatterFigure=px.scatter_geo(arabConfirmedLongDf, 
#                              lat='Lat', lon='Long', color='Country',
#                              hover_name="Country", hover_data='Confirmed',
#                              size=
#                              )