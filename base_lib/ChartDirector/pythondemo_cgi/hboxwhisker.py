#!/usr/bin/python
from pychartdir import *

# Sample data for the Box-Whisker chart. Represents the minimum, 1st quartile, medium, 3rd quartile
# and maximum values of some quantities
Q0Data = [40, 45, 35]
Q1Data = [55, 60, 50]
Q2Data = [62, 70, 60]
Q3Data = [70, 80, 65]
Q4Data = [80, 90, 75]

# The labels for the chart
labels = ["<*img=robot1.png*><*br*>Bipedal Type", "<*img=robot2.png*><*br*>Wolf Type",
    "<*img=robot5.png*><*br*>Bird Type"]

# Create a XYChart object of size 540 x 320 pixels
c = XYChart(540, 320)

# swap the x and y axes to create a horizontal box-whisker chart
c.swapXY()

# Set directory for loading images to current script directory
# Need when running under Microsoft IIS
c.setSearchPath(os.path.dirname(sys.argv[0]))

# Set the plotarea at (75, 25) and of size 440 x 270 pixels. Enable both horizontal and vertical
# grids by setting their colors to grey (0xc0c0c0)
c.setPlotArea(75, 25, 440, 270).setGridColor(0xc0c0c0, 0xc0c0c0)

# Add a title to the chart
c.addTitle("           Robot Shooting Accuracy Scores")

# Set the labels on the x axis and the font to Arial Bold
c.xAxis().setLabels(labels).setFontStyle("arialbd.ttf")

# Disable x axis ticks by setting the length to 0
c.xAxis().setTickLength(0)

# Set the font for the y axis labels to Arial Bold
c.yAxis().setLabelStyle("arialbd.ttf")

# Add a Box Whisker layer using light blue 0x9999ff as the fill color and blue (0xcc) as the line
# color. Set the line width to 2 pixels
c.addBoxWhiskerLayer2(Q3Data, Q1Data, Q4Data, Q0Data, Q2Data).setLineWidth(2)

# Output the chart
print("Content-type: image/png\n")
binaryPrint(c.makeChart2(PNG))

