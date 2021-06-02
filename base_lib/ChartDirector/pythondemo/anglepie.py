#!/usr/bin/python
from pychartdir import *

def createChart(chartIndex) :

    # The data for the pie chart
    data = [25, 18, 15, 12, 8, 30, 35]

    # The labels for the pie chart
    labels = ["Labor", "Licenses", "Taxes", "Legal", "Insurance", "Facilities", "Production"]

    # Create a PieChart object of size 280 x 240 pixels
    c = PieChart(280, 240)

    # Set the center of the pie at (140, 130) and the radius to 80 pixels
    c.setPieSize(140, 130, 80)

    # Add a title to the pie to show the start angle and direction
    if chartIndex == 0 :
        c.addTitle("Start Angle = 0 degrees\nDirection = Clockwise")
    else :
        c.addTitle("Start Angle = 90 degrees\nDirection = AntiClockwise")
        c.setStartAngle(90, 0)

    # Draw the pie in 3D
    c.set3D()

    # Set the pie data and the pie labels
    c.setData(data, labels)

    # Explode the 1st sector (index = 0)
    c.setExplode(0)

    # Output the chart
    c.makeChart("anglepie%s.png" % chartIndex)


createChart(0)
createChart(1)

