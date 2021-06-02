#!/usr/bin/python
from pychartdir import *
import cgi, sys

# Get HTTP query parameters
query = cgi.FieldStorage()

# This script can draw different charts depending on the chartIndex
chartIndex = int(query["img"].value)

# The data for the pie chart
data = [18, 30, 20, 15]

# The colors to use for the sectors
colors = [0x66aaee, 0xeebb22, 0xbbbbbb, 0x8844ff]

# Create a PieChart object of size 200 x 200 pixels. Use a vertical gradient color from blue
# (0000cc) to deep blue (000044) as background. Use rounded corners of 16 pixels radius.
c = PieChart(200, 200)
c.setBackground(c.linearGradientColor(0, 0, 0, c.getHeight(), 0x0000cc, 0x000044))
c.setRoundedFrame(0xffffff, 16)

# Set the center of the pie at (100, 100) and the radius to 80 pixels
c.setPieSize(100, 100, 80)

# Set the pie data
c.setData(data)

# Set the sector colors
c.setColors2(DataColor, colors)

# Draw the pie in 3D with a pie thickness of 20 pixels
c.set3D(20)

# Demonstrates various shading modes
if chartIndex == 0 :
    c.addTitle("Default Shading", "bold", 12, 0xffffff)
elif chartIndex == 1 :
    c.addTitle("Flat Gradient", "bold", 12, 0xffffff)
    c.setSectorStyle(FlatShading)
elif chartIndex == 2 :
    c.addTitle("Local Gradient", "bold", 12, 0xffffff)
    c.setSectorStyle(LocalGradientShading)
elif chartIndex == 3 :
    c.addTitle("Global Gradient", "bold", 12, 0xffffff)
    c.setSectorStyle(GlobalGradientShading)
elif chartIndex == 4 :
    c.addTitle("Concave Shading", "bold", 12, 0xffffff)
    c.setSectorStyle(ConcaveShading)
elif chartIndex == 5 :
    c.addTitle("Rounded Edge", "bold", 12, 0xffffff)
    c.setSectorStyle(RoundedEdgeShading)
elif chartIndex == 6 :
    c.addTitle("Radial Gradient", "bold", 12, 0xffffff)
    c.setSectorStyle(RadialShading)

# Disable the sector labels by setting the color to Transparent
c.setLabelStyle("", 8, Transparent)

# Output the chart
print("Content-type: image/png\n")
binaryPrint(c.makeChart2(PNG))

