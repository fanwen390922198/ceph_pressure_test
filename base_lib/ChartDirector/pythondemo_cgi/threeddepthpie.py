#!/usr/bin/python
from pychartdir import *
import cgi, sys

# Get HTTP query parameters
query = cgi.FieldStorage()

# This script can draw different charts depending on the chartIndex
chartIndex = int(query["img"].value)

# the tilt angle of the pie
depth = chartIndex * 5 + 5

# The data for the pie chart
data = [25, 18, 15, 12, 8, 30, 35]

# Create a PieChart object of size 100 x 110 pixels
c = PieChart(100, 110)

# Set the center of the pie at (50, 55) and the radius to 38 pixels
c.setPieSize(50, 55, 38)

# Set the depth of the 3D pie
c.set3D(depth)

# Add a title showing the depth
c.addTitle("Depth = %s pixels" % (depth), "arial.ttf", 8)

# Set the pie data
c.setData(data)

# Disable the sector labels by setting the color to Transparent
c.setLabelStyle("", 8, Transparent)

# Output the chart
print("Content-type: image/png\n")
binaryPrint(c.makeChart2(PNG))

