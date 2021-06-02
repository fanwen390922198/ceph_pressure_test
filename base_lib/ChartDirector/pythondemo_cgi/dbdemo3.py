#!/usr/bin/python
from pychartdir import *

#
# Query the database to get the for the 12 years from 1994 to 2005. In this demo,
# we will just dynamically generate some numbers instead of a real database.
#
revenue = []
timestamp = []

seed = 700
for i in range(1994, 2006) :
    revenue.append(seed)
    timestamp.append(str(i))
    seed = seed * 1.2

#
# Now we have read data into arrays, we can draw the chart using ChartDirector
#

# Create a XYChart object of size 600 x 360 pixels
c = XYChart(600, 360)

# Set the plotarea at (60, 40) and of size 480 x 280 pixels. Use a vertical gradient color from
# light blue (eeeeff) to deep blue (0000cc) as background. Set border and grid lines to white
# (ffffff).
c.setPlotArea(60, 40, 480, 280, c.linearGradientColor(60, 40, 60, 280, 0xeeeeff, 0x0000cc), -1,
    0xffffff, 0xffffff)

# Add a title to the chart using 18pt Times Bold Italic font
c.addTitle("Annual Revenue for Star Tech", "timesbi.ttf", 18)

# Add a multi-color bar chart layer using the supplied data
layer = c.addBarLayer3(revenue)

# Use glass lighting effect with light direction from the left
layer.setBorderColor(Transparent, glassEffect(NormalGlare, Left))

# Set the x axis labels
c.xAxis().setLabels(timestamp)

# Set y-axis tick density to 30 pixels. ChartDirector auto-scaling will use this as the guideline
# when putting ticks on the y-axis.
c.yAxis().setTickDensity(30)

# Synchronize the left and right y-axes
c.syncYAxis()

# Set the y axes titles with 10pt Arial Bold font
c.yAxis().setTitle("USD (Millions)", "arialbd.ttf", 10)
c.yAxis2().setTitle("USD (Millions)", "arialbd.ttf", 10)

# Set all axes to transparent
c.xAxis().setColors(Transparent)
c.yAxis().setColors(Transparent)
c.yAxis2().setColors(Transparent)

# Set the label styles of all axes to 8pt Arial Bold font
c.xAxis().setLabelStyle("arialbd.ttf", 8)
c.yAxis().setLabelStyle("arialbd.ttf", 8)
c.yAxis2().setLabelStyle("arialbd.ttf", 8)

# Create the image
chart1URL = c.makeTmpFile("/tmp/tmpcharts")

# Create an image map for the chart
imageMap = c.getHTMLImageMap("dbdemo3a.py", "", "title='{xLabel}: US$ {value|0}M'")

print("Content-type: text/html\n")
print("""
<html>
<body style="margin:5px 0px 0px 5px">
<div style="font-size:18pt; font-family:verdana; font-weight:bold">
    Database Clickable Charts
</div>
<hr style="border:solid 1px #000080" />
<div style="font-size:10pt; font-family:verdana; width:600px; margin-bottom:20px">
    The example demonstrates creating a clickable chart using data from a database.
    Click on a bar below to "drill down" onto a particular year.
<br /><br />
<a href='viewsource.py?file=%(SCRIPT_NAME)s'>
    View source code
</a>
</div>

<img src="getchart.py?img=/tmp/tmpcharts/%(chart1URL)s" border="0" usemap="#map1">
<map name="map1">
%(imageMap)s
</map>

</body>
</html>
""" % {
    "SCRIPT_NAME" : os.environ["SCRIPT_NAME"],
    "chart1URL" : chart1URL,
    "imageMap" : imageMap
    })
