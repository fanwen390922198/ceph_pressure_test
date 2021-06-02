#!/usr/bin/python
from pychartdir import *
import cgi, sys

# Get HTTP query parameters
query = cgi.FieldStorage()

# Get the selected year and month
selectedYear = int(query["year"].value)
selectedMonth = int(query["x"].value) + 1

#
# In real life, the data may come from a database based on selectedYear. In this example, we just
# use a random number generator.
#
seed = (selectedYear - 1992) * (100 + 3 * selectedMonth)
rantable = RanTable(seed, 1, 4)
rantable.setCol(0, seed * 0.003, seed * 0.017)

data = rantable.getCol(0)

# The labels for the pie chart
labels = ["Services", "Hardware", "Software", "Others"]

# Create a PieChart object of size 600 x 240 pixels
c = PieChart(600, 280)

# Set the center of the pie at (300, 140) and the radius to 120 pixels
c.setPieSize(300, 140, 120)

# Add a title to the pie chart using 18pt Times Bold Italic font
c.addTitle("Revenue Breakdown for %s/%s" % (selectedMonth, selectedYear), "timesbi.ttf", 18)

# Draw the pie in 3D with 20 pixels 3D depth
c.set3D(20)

# Set label format to display sector label, value and percentage in two lines
c.setLabelFormat("{label}<*br*>${value|2}M ({percent}%)")

# Set label style to 10pt Arial Bold Italic font. Set background color to the same as the sector
# color, with reduced-glare glass effect and rounded corners.
t = c.setLabelStyle("arialbi.ttf", 10)
t.setBackground(SameAsMainColor, Transparent, glassEffect(ReducedGlare))
t.setRoundedCorners()

# Use side label layout method
c.setLabelLayout(SideLayout)

# Set the pie data and the pie labels
c.setData(data, labels)

# Create the image and save it in a temporary location
chart1URL = c.makeTmpFile("/tmp/tmpcharts")

# Create an image map for the chart
imageMap = c.getHTMLImageMap("piestub.py", "", "title='{label}:US$ {value|2}M'")

print("Content-type: text/html\n")
print("""
<html>
<body style="margin:5px 0px 0px 5px">
<div style="font-size:18pt; font-family:verdana; font-weight:bold">
    Simple Clickable Pie Chart
</div>
<hr style="border:solid 1px #000080" />
<div style="font-size:10pt; font-family:verdana; margin-bottom:20">
    <a href="viewsource.py?file=%(SCRIPT_NAME)s">View Source Code</a>
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
