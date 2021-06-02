#!/usr/bin/python
from pychartdir import *
import cgi, sys

# Get HTTP query parameters
query = cgi.FieldStorage()

#
# Displays the monthly revenue for the selected year. The selected year should be passed in as a
# query parameter called "xLabel"
#
try :
    selectedYear = int(query["xLabel"].value)
except :
    selectedYear = 2005

#
# Query the database to get monthly reveunes for software, hardware and services for
# the year. In this demo, we will use random numbers instead of a real database.
#
rantable = RanTable(selectedYear, 3, 12)
rantable.setCol(0, 30 * (selectedYear - 1990),  80 * (selectedYear - 1990))
rantable.setCol(1, 30 * (selectedYear - 1990),  80 * (selectedYear - 1990))
rantable.setCol(2, 30 * (selectedYear - 1990),  80 * (selectedYear - 1990))

software = rantable.getCol(0)
hardware = rantable.getCol(1)
services = rantable.getCol(2)

#
# Now we have read data into arrays, we can draw the chart using ChartDirector
#

# Create a XYChart object of size 600 x 360 pixels
c = XYChart(600, 360)

# Set the plotarea at (60, 50) and of size 480 x 270 pixels. Use a vertical gradient color from
# light blue (eeeeff) to deep blue (0000cc) as background. Set border and grid lines to white
# (ffffff).
c.setPlotArea(60, 50, 480, 270, c.linearGradientColor(60, 50, 60, 270, 0xeeeeff, 0x0000cc), -1,
    0xffffff, 0xffffff)

# Add a title to the chart using 15pt Times Bold Italic font
c.addTitle("Global Revenue for Year %s" % (selectedYear), "timesbi.ttf", 18)

# Add a legend box at (60, 25) (top of the plotarea) with 9pt Arial Bold font
c.addLegend(60, 25, 0, "arialbd.ttf", 9).setBackground(Transparent)

# Add a line chart layer using the supplied data
layer = c.addLineLayer2()
layer.addDataSet(software, 0xffaa00, "Software").setDataSymbol(CircleShape, 9)
layer.addDataSet(hardware, 0x00ff00, "Hardware").setDataSymbol(DiamondShape, 11)
layer.addDataSet(services, 0xff0000, "Services").setDataSymbol(Cross2Shape(), 11)

# Set the line width to 3 pixels
layer.setLineWidth(3)

# Set the x axis labels. In this example, the labels must be Jan - Dec.
labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
c.xAxis().setLabels(labels)

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

# Create the image and save it in a temporary location
chart1URL = c.makeTmpFile("/tmp/tmpcharts")

# Create an image map for the chart
imageMap = c.getHTMLImageMap("xystub.py", "", "title='{dataSetName} @ {xLabel} = USD {value|0}M'")

print("Content-type: text/html\n")
print("""
<html>
<body style="margin:5px 0px 0px 5px">
<div style="font-size:18pt; font-family:verdana; font-weight:bold">
    Database Clickable Charts
</div>
<hr style="border:solid 1px #000080" />
<div style="font-size:10pt; font-family:verdana; width:600px; margin-bottom:20px">
    You have click the bar for the year %(selectedYear)s.
    Below is the "drill-down" chart showing the monthly details.
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
    "selectedYear" : selectedYear,
    "SCRIPT_NAME" : os.environ["SCRIPT_NAME"],
    "chart1URL" : chart1URL,
    "imageMap" : imageMap
    })
