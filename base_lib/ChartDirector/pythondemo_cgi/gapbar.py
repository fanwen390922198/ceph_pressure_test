#!/usr/bin/python
from pychartdir import *
import cgi, sys

# Get HTTP query parameters
query = cgi.FieldStorage()

# This script can draw different charts depending on the chartIndex
chartIndex = int(query["img"].value)

bargap = chartIndex * 0.25 - 0.25

# The data for the bar chart
data = [100, 125, 245, 147, 67]

# The labels for the bar chart
labels = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# Create a XYChart object of size 150 x 150 pixels
c = XYChart(150, 150)

# Set the plotarea at (27, 20) and of size 120 x 100 pixels
c.setPlotArea(27, 20, 120, 100)

# Set the labels on the x axis
c.xAxis().setLabels(labels)

if bargap >= 0 :
    # Add a title to display to bar gap using 8pt Arial font
    c.addTitle("      Bar Gap = %s" % (bargap), "arial.ttf", 8)
else :
    # Use negative value to mean TouchBar
    c.addTitle("      Bar Gap = TouchBar", "arial.ttf", 8)
    bargap = TouchBar

# Add a bar chart layer using the given data and set the bar gap
c.addBarLayer(data).setBarGap(bargap)

# Output the chart
print("Content-type: image/png\n")
binaryPrint(c.makeChart2(PNG))

