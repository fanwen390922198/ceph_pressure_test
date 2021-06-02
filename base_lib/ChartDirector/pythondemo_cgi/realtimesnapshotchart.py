#!/usr/bin/python
from pychartdir import *
import cgi, sys, math

# Get HTTP query parameters
query = cgi.FieldStorage()

#
# Data to draw the chart. In this demo, the data buffer will be filled by a random data generator.
# In real life, the data is probably stored in a buffer (eg. a database table, a text file, or some
# global memory) and updated by other means.
#

# We use a data buffer to emulate the last 240 samples.
sampleSize = 240
dataSeries1 = [0] * sampleSize
dataSeries2 = [0] * sampleSize
dataSeries3 = [0] * sampleSize
timeStamps = [0] * sampleSize

# Our pseudo random number generator
firstDate = chartTime2(time.time()) - len(timeStamps)
for i in range(0, len(timeStamps)) :
    p = firstDate + i
    timeStamps[i] = p
    dataSeries1[i] = math.cos(p * 2.1) * 10 + 1 / (math.cos(p) * math.cos(p) + 0.01) + 20
    dataSeries2[i] = 100 * math.sin(p / 27.7) * math.sin(p / 10.1) + 150
    dataSeries3[i] = 100 * math.cos(p / 6.7) * math.cos(p / 11.9) + 150

# Create an XYChart object 600 x 320 pixels in size
c = XYChart(600, 320)

# Set the plotarea at (55, 60) and of size 520 x 235 pixels with transparent background and border.
# Enable both horizontal and vertical grids by setting their colors to grey (cccccc). Set clipping
# mode to clip the data lines to the plot area.
c.setPlotArea(55, 60, 520, 235, -1, -1, Transparent, 0xcccccc, 0xcccccc)
c.setClipping()

# Add a title to the chart using dark grey (0x333333) 20pt Arial Bold font
c.addTitle("Realtime Chart with Snapshot", "arialbd.ttf", 20, 0x333333)

# Add a legend box at the top of the plot area using horizontal layout. Use 10pt Arial Bold font,
# transparent background and border, and line style legend icon.
b = c.addLegend(55, 30, 0, "arialbd.ttf", 10)
b.setBackground(Transparent, Transparent)
b.setLineStyleKey()

# Set the x and y axis stems to transparent and the label font to 10pt Arial
c.xAxis().setColors(Transparent)
c.yAxis().setColors(Transparent)
c.xAxis().setLabelStyle("arial.ttf", 10)
c.yAxis().setLabelStyle("arial.ttf", 10)

# Add y-axis title using 12pt Arial font
c.yAxis().setTitle("Y-Axis Title Placeholder", "arial.ttf", 12)

# For the automatic x and y axis labels, set the minimum spacing to 75 and 30 pixels.
c.xAxis().setTickDensity(75)
c.yAxis().setTickDensity(30)

# Set the x-axis label format
c.xAxis().setLabelFormat("{value|hh:nn:ss}")

# Create a line layer to plot the lines
layer = c.addLineLayer2()

# The x-coordinates are the timeStamps.
layer.setXData(timeStamps)

# The 3 data series are used to draw 3 lines. Here we put the latest data values as part of the data
# set name, so you can see them updated in the legend box.
layer.addDataSet(dataSeries1, 0xff0000, c.formatValue(dataSeries1[len(dataSeries1) - 1],
    "Alpha: {value|2}"))
layer.addDataSet(dataSeries2, 0x00cc00, c.formatValue(dataSeries2[len(dataSeries2) - 1],
    "Beta: {value|2}"))
layer.addDataSet(dataSeries3, 0x0000ff, c.formatValue(dataSeries3[len(dataSeries3) - 1],
    "Gamma: {value|2}"))

# Check if is download request
downloadFormat = query.has_key("download") and query["download"].value or None
if not ((downloadFormat == None) or (downloadFormat == "")) :
    fname = "demo_%s" % (c.formatValue(timeStamps[len(timeStamps) - 1], "yyyymmddhhnnss"))
    if downloadFormat == "pdf" :
        # Output in PDF and stream as attachment
        print("Content-Disposition: attachment; filename=\"" + fname + ".pdf\"")
        print("Content-type: application/pdf\n")
        binaryPrint(c.makeChart2(PDF))
        sys.exit()
    else :
        # Output in PNG and stream as attachment
        print("Content-Disposition: attachment; filename=\"" + fname + ".png\"")
        print("Content-type: image/png\n")
        binaryPrint(c.makeChart2(PNG))
        sys.exit()

# Output the chart
print("Content-type: image/png\n")
binaryPrint(c.makeChart2(PNG))

