#####################RUN THE SCRIPT VIA OPENING A CMD CMD IN THE SAME DIRECTORY
##RUN THE COMMAND: bokeh serve belgianHouses_final.py --show --port 5010 --allow-websocket-origin=*########
####MAKE SURE THE FILES Belgium_withHousePrice.json and belgianHousesClean.csv ARE IN THE SAME FOLDER#####

import pandas as pd
import json
import numpy as np

from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource,Column,NumeralTickFormatter,Range1d,Row,GeoJSONDataSource,HoverTool,LinearColorMapper,Label,ColorBar
from bokeh.models.widgets import Select,Slider,Button,Div
from bokeh.palettes import RdYlGn11

def filterDB(place="Aalst",houseType="houses"):
    dataAalst=df.loc[(df['Commune'] == place) & (df['Type'] == houseType)]
    return dataAalst

#set the color value of the geoDict per feature
def setGeoDictColor(geoDict,dataTypeFilter,propertyFilter,year):
    for i in geoDict['features']:
        i['properties']['color']=i['properties'][dataTypeFilter][propertyFilter][year-1973]       
    return geoDict

df=pd.read_csv('belgianHousesClean.csv',encoding='utf-8',index_col=0)
communeList=list(df['Commune'])
communeList=sorted(list(set(communeList)))#only unique values
commune1='Aalst'
commune2='Leuven'
typeList=list(set(list(df['Type'])))
print(typeList)
Yaxis='Price/m2'
propertyType='houses'
year=2017

#create the map graph
#read the json file
with open(r'Belgium_withHousePrice.json', 'r',encoding='utf-8') as f:
    geojson=f.read()#string file
geoDict=eval(geojson)

#get the min and max for the map color range
def setMapColorRange():
    global minMap,maxMap
    colorRangeDF=list(df.loc[df['Type'] == propertyType][Yaxis])
    colorRangeDF=[x for x in colorRangeDF if str(x) != 'nan']
    minMap=np.percentile(np.array(colorRangeDF),5)
    maxMap=np.percentile(np.array(colorRangeDF),99)
    print(minMap,maxMap)

def createMap():
    geoDictColored=setGeoDictColor(geoDict,dataTypeFilter=Yaxis,propertyFilter=propertyType,year=year)
    geo_source = GeoJSONDataSource(geojson=json.dumps(geoDictColored))#bokeh source
    
    tools = "pan,wheel_zoom,tap,reset"
    countryMap = figure(title='Belgian real estate transactions: average in euros by commune',tools=tools,width=1000, height=700,x_axis_location=None, y_axis_location=None)
    countryMap.xgrid.grid_line_color = None
    countryMap.ygrid.grid_line_color = None
    
    color_mapper = LinearColorMapper(palette=RdYlGn11,low=minMap,high=maxMap,nan_color='grey')
    countryMap.patches('xs', 'ys',source=geo_source,line_color='black',fill_color={'field': 'color', 'transform': color_mapper})
    countryMap.add_tools(HoverTool(tooltips = [("name", "@name"),( Yaxis,'@color{int}')]))
    
    yearLabel = Label(x=20, y=10, x_units='screen', y_units='screen',text=str(year), render_mode='css',text_font_size='100pt')
    countryMap.add_layout(yearLabel)

    color_bar = ColorBar(color_mapper=color_mapper, width=20,  location=(0,0))
    countryMap.add_layout(color_bar, 'right')
    
    return countryMap
setMapColorRange()
countryMap=createMap()

#create a button to animate the graph
def animate_update():
    year = slider.value + 1
    if year > 2017:
        year = 1973
    slider.value = year

callback_id='0'#declare a variable like this
def animate():
    global callback_id
    if button.label == 'Play':
        button.label = 'Pause'
        callback_id = curdoc().add_periodic_callback(animate_update, 500)
    else:
        button.label = 'Play'
        curdoc().remove_periodic_callback(callback_id)
button = Button(label='Play', width=60)
button.on_click(animate)


def plotAvgTrend():   
    source1 = ColumnDataSource(data=filterDB(place=commune1,houseType=propertyType))
    source2 = ColumnDataSource(data=filterDB(place=commune2,houseType=propertyType))
    
    fig=figure(width=700,title='Belgian real estate transactions 1973-2017: average trend in euros by commune and type')
    fig.line(x="CD_YEAR", y=Yaxis,color='blue',source=source1,legend=commune1)
    fig.line(x="CD_YEAR", y=Yaxis,color='red',source=source2,legend=commune2)
    fig.xaxis.axis_label = 'Year'
    fig.x_range = Range1d(1973,2017)
    fig.yaxis.formatter = NumeralTickFormatter(format="{}0")
    
    if Yaxis=='Mean Price':
        fig.y_range = Range1d(start=0,end=maxMap*1.02)       
        fig.yaxis.axis_label = 'Average price (euro)'
    elif Yaxis=='Price/m2':
        fig.y_range = Range1d(start=0,end=maxMap*1.02)
        fig.yaxis.axis_label = 'Average price/m2 (euro)'
    
    fig.legend.location = "top_left"
    fig.legend.click_policy="hide"
    
    return fig

fig=plotAvgTrend()

#the first dropdown with choice of commune
def commune1Change(attr,old,new):
    global commune1
    print(new)
    commune1=new
    updatePlot()
selectCommune1 = Select(title="Commune 1:", value=commune1, options=communeList)
selectCommune1.on_change("value",commune1Change)

#the second dropdown with choice of commune
def commune2Change(attr,old,new):
    global commune2
    print(new)
    commune2=new
    updatePlot()
selectCommune2 = Select(title="Commune 2:", value=commune2, options=communeList)
selectCommune2.on_change("value",commune2Change)


#set the Y-axis
def YaxisChange(attr,old,new):
    global Yaxis
    print(new)
    Yaxis=new
    updatePlot()
selectYaxis = Select(title="Y-axis:", value='Price/m2', options=['Mean Price','Price/m2'])
selectYaxis.on_change("value",YaxisChange)

#set the type of property
def typeChange(attr,old,new):
    global propertyType
    print(new)
    propertyType=new
    updatePlot()
selectType = Select(title="type of property:", value='houses', options=typeList)
selectType.on_change("value",typeChange)

def updatePlot():
    setMapColorRange()
    newfig=plotAvgTrend()
    graphColumn.children[2]=newfig
    new_countryMap=createMap()
    mapColum.children[0]=new_countryMap

def slider_update(attrname, old, new):
    global year
    year=new
    new_countryMap=createMap()
    mapColum.children[0]=new_countryMap
    
slider = Slider(start=1973, end=2017, value=2017, step=1, title="Year")
slider.on_change('value', slider_update)
  
div = Div(text="""
<p>All source data is from the Begian governement at <a href=https://statbel.fgov.be/en target="_blank">https://statbel.fgov.be/en</a>.</br>
All data are averages.</br>
For communes where no data was available at all the average was set at 0.</br>
For years where no data was available the average was set to the same value as the year before.</br>
<b>The interactive graph was made by <a href=mailto:JorisMeertBambrugge@gmail.com >Joris Meert</a> for educational purpose.</b></p>
""",width=700, height=100)
 
graphColumn=Column(selectType,Row(selectCommune1,selectCommune2),fig,selectYaxis,div)
mapColum=Column(countryMap,Row(slider,button))
layout=Row(graphColumn,mapColum)
curdoc().add_root(layout)
curdoc().title="Belgian house market"