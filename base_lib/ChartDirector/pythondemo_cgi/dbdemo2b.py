#!/usr/bin/python
from pychartdir import *
import cgi, sys

# Get HTTP query parameters
query = cgi.FieldStorage()

#
# Retrieve the data from the query parameters
#

selectedYear = query["year"].value

software = map(float, string.split(query["software"].value, ","))
hardware = map(float, string.split(query["hardware"].value, ","))
services = map(float, string.split(query["services"].value, ","))

#
# Now we obtained the data into arrays, we can draw the chart using ChartDirector
#

# Create a XYChart object of size 600 x 300 pixels, with a light grey (eeeeee) background, black
# border, 1 pixel 3D border effect and rounded corners.
c = XYChart(600, 300, 0xeeeeee, 0x000000, 1)
c.setRoundedFrame()

# Set the plotarea at (60, 60) and of size 520 x 200 pixels. Set background color to white (ffffff)
# and border and grid colors to grey (cccccc)
c.setPlotArea(60, 60, 520, 200, 0xffffff, -1, 0xcccccc, 0xccccccc)

# Add a title to the chart using 15pt Times Bold Italic font, with a dark green (006600) background
# and with glass lighting effects.
c.addTitle("Global Revenue for Year %s" % (selectedYear), "timesbi.ttf", 15, 0xffffff
    ).setBackground(0x006600, 0x000000, glassEffect(ReducedGlare))

# Add a legend box at (70, 32) (top of the plotarea) with 9pt Arial Bold font
c.addLegend(70, 32, 0, "arialbd.ttf", 9).setBackground(Transparent)

# Add a stacked area chart layer using the supplied data
layer = c.addAreaLayer2(Stack)
layer.addDataSet(software, 0x40ff0000, "Software")
layer.addDataSet(hardware, 0x4000ff00, "Hardware")
layer.addDataSet(services, 0x40ffaa00, "Services")

# Set the area border color to the same as the fill color
layer.setBorderColor(SameAsMainColor)

# Set the x axis labels. In this example, the labels must be Jan - Dec.
labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
c.xAxis().setLabels(labels)

# Set the y axis title
c.yAxis().setTitle("USD (Millions)")

# Set axes width to 2 pixels
c.xAxis().setWidth(2)
c.yAxis().setWidth(2)

# Output the chart in PNG format
print("Content-type: image/png\n")
binaryPrint(c.makeChart2(PNG))

