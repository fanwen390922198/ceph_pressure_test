#!/usr/bin/python
from pychartdir import *
import cgi, sys, os

# Get HTTP query parameters
query = cgi.FieldStorage()

# This script can draw different charts depending on the chartIndex
chartIndex = int(query["img"].value)

# The data for the chart
data = [85, 156, 179.5, 211, 123]
labels = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# Create a XYChart object of size 270 x 270 pixels
c = XYChart(270, 270)

# Set the plot area at (40, 32) and of size 200 x 200 pixels
plotarea = c.setPlotArea(40, 32, 200, 200)

# Set the background style based on the input parameter
if chartIndex == 0 :
    # Has wallpaper image
    c.setWallpaper(os.path.join(os.path.dirname(sys.argv[0]), "tile.gif"))
elif chartIndex == 1 :
    # Use a background image as the plot area background
    plotarea.setBackground2(os.path.join(os.path.dirname(sys.argv[0]), "bg.png"))
elif chartIndex == 2 :
    # Use white (0xffffff) and grey (0xe0e0e0) as two alternate plotarea background colors
    plotarea.setBackground(0xffffff, 0xe0e0e0)
else :
    # Use a dark background palette
    c.setColors(whiteOnBlackPalette)

# Set the labels on the x axis
c.xAxis().setLabels(labels)

# Add a color bar layer using the given data. Use a 1 pixel 3D border for the bars.
c.addBarLayer3(data).setBorderColor(-1, 1)

# Output the chart
print("Content-type: image/png\n")
binaryPrint(c.makeChart2(PNG))

