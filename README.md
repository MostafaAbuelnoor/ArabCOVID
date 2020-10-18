# ArabCOVID
The Arab World's COVID-19 stats on graphs and maps using Python and Plotly.

I wrote this project as a learning experience and it is not to be trusted as an official source for COVID-19 metrics.

Please checkout the [blog post](https://blog.rmotr.com/learn-data-science-by-analyzing-covid-19-27a063d7f442) that I followed and took inspiration from.

## The Data
I used an open source [dataset](https://github.com/CSSEGISandData/COVID-19) and extracted the Arab Countries information. I cross checked some of the countries numbers with local media numbers and the dataset seems reliable and up to date.    

## Installation 
I used [Python 3.8.0](https://www.python.org/downloads/) on this project. However, I do not think using an older version will be an issue.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Plotly.

```bash
$ pip install plotly==4.11.0
```
## Usage
The dataset updates daily so provided you installed python and plotly correctly you can run the file and get the different updated visuals.

You should expect 4 visuals:
1. A **_Treemap_** with active, recovered and dead cases in each Arab country.
2. A **_Pie Chart_** that shows the percentage of active, recovered and dead cases in the Arab World as a whole.
3. A **_Bar Graph_** that shows the mortality rate per 100 cases in each country. 
4. A **_Scatter Map_** that shows confirmed cases in the arab world over a time period from february to date.

## Treemap

## Pie Chart

## Bar Graph

## Scatter Map

## License
[MIT](https://choosealicense.com/licenses/mit/)