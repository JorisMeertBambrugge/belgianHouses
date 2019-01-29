
# coding: utf-8

# # Bokeh server example 2, more elaborate
# 
# To make this script work:
# 
# 1. save the file as a .py file (File>Download as>..)
# 2. open a cmd in the directory where you saved it
# 3. run "bokeh serve bokehServer.py --show"

# In[1]:


from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import Figure
from bokeh.io import curdoc,show

power=1#the starting value of the slider

#create the plot
def createGraph(): 
    x = [x*0.005 for x in range(0, 200)]
    y = [i**power for i in x ]
    source = ColumnDataSource(data=dict(x=x, y=y))
    
    plot = Figure(plot_width=400, plot_height=400)
    plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6,color="red")
    plot.circle([0,0.2,0.4,0.6,0.8,1],[0,0.01,0.08,0.2,0.45,0.98])
    
    return plot

#create the slide and the effect of changing it
def sliderChange(attr, old, new):
    global power
    print("the slider have been changed. It's new value is now "+str(new))
    power=float(new)
    updatePlot()
slider = Slider(start=0.1, end=4, value=power, step=.1, title="power")
slider.on_change("value", sliderChange)

#update the plot in the layout
def updatePlot():
    plot=createGraph()
    layout.children[1]=plot

plot=createGraph()#create the starting plot

layout = column(slider, plot)
curdoc().add_root(layout)
show(layout)


# # Excersize: add a text input widget that changes the color of the line.
# Place it togheter with the slider in a widgetbox (container)
# 
# 
# from bokeh.models.widgets import Select<br>
# from bokeh.layouts import widgetbox
# 
# select = Select(title="Choose your color", value="red", options=["red", "green", "blue", "orange"])
# 
# layout=column(widgetbox(slider,select), plot)
