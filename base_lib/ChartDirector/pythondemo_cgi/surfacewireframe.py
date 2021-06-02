#!/usr/bin/python
from pychartdir import *
import cgi, sys, math

# Get HTTP query parameters
query = cgi.FieldStorage()

# This script can draw different charts depending on the chartIndex
chartIndex = int(query["img"].value)

# The x and y coordinates of the grid
dataX = [-2, -1, 0, 1, 2]
dataY = [-2, -1, 0, 1, 2]

# The values at the grid points. In this example, we will compute the values using the formula z =
# square_root(15 - x * x - y * y).
dataZ = [0] * (len(dataX) * len(dataY))
for yIndex in range(0, len(dataY)) :
    y = dataY[yIndex]
    for xIndex in range(0, len(dataX)) :
        x = dataX[xIndex]
        dataZ[yIndex * len(dataX) + xIndex] = math.sqrt(15 - x * x - y * y)

# Create a SurfaceChart object of size 380 x 340 pixels, with white (ffffff) background and grey
# (888888) border.
c = SurfaceChart(380, 340, 0xffffff, 0x888888)

# Demonstrate various wireframes with and without interpolation
if chartIndex == 0 :
    # Original data without interpolation
    c.addTitle("5 x 5 Data Points\nStandard Shading", "arialbd.ttf", 12)
    c.setContourColor(0x80ffffff)
elif chartIndex == 1 :
    # Original data, spline interpolated to 40 x 40 for smoothness
    c.addTitle("5 x 5 Points - Spline Fitted to 40 x 40\nStandard Shading", "arialbd.ttf", 12)
    c.setContourColor(0x80ffffff)
    c.setInterpolation(40, 40)
elif chartIndex == 2 :
    # Rectangular wireframe of original data
    c.addTitle("5 x 5 Data Points\nRectangular Wireframe")
    c.setShadingMode(RectangularFrame)
elif chartIndex == 3 :
    # Rectangular wireframe of original data spline interpolated to 40 x 40
    c.addTitle("5 x 5 Points - Spline Fitted to 40 x 40\nRectangular Wireframe")
    c.setShadingMode(RectangularFrame)
    c.setInterpolation(40, 40)
elif chartIndex == 4 :
    # Triangular wireframe of original data
    c.addTitle("5 x 5 Data Points\nTriangular Wireframe")
    c.setShadingMode(TriangularFrame)
else :
    # Triangular wireframe of original data spline interpolated to 40 x 40
    c.addTitle("5 x 5 Points - Spline Fitted to 40 x 40\nTriangular Wireframe")
    c.setShadingMode(TriangularFrame)
    c.setInterpolation(40, 40)

# Set the center of the plot region at (200, 170), and set width x depth x height to 200 x 200 x 150
# pixels
c.setPlotRegion(200, 170, 200, 200, 150)

# Set the plot region wall thichness to 5 pixels
c.setWallThickness(5)

# Set the elevation and rotation angles to 20 and 30 degrees
c.setViewAngle(20, 30)

# Set the data to use to plot the chart
c.setData(dataX, dataY, dataZ)

# Output the chart
print("Content-type: image/jpeg\n")
binaryPrint(c.makeChart2(JPG))

