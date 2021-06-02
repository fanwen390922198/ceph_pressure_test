#!/usr/bin/python
from pychartdir import *
import cgi, sys

# Get HTTP query parameters
query = cgi.FieldStorage()


# The currently selected year
try :
    selectedYear = int(query["year"].value)
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

# Serialize the data into a string to be used as HTTP query parameters
httpParam = "year=%s&software=%s&hardware=%s&services=%s" % (selectedYear,
    string.join(map(str, software), ","), string.join(map(str, hardware), ","),
    string.join(map(str, services), ","))

#
# The following code generates the <option> tags for the HTML select box, with the <option> tag
# representing the currently selected year marked as selected.
#

optionTags = [None] * (2005 - 1994 + 1)
for i in range(1994, 2005 + 1) :
    if i == selectedYear :
        optionTags[i - 1994] = "<option value='%s' selected>%s</option>" % (i, i)
    else :
        optionTags[i - 1994] = "<option value='%s'>%s</option>" % (i, i)
selectYearOptions = string.join(optionTags, "")

print("Content-type: text/html\n")
print("""
<html>
<body style="margin:5px 0px 0px 5px">
<div style="font-size:18pt; font-family:verdana; font-weight:bold">
    Database Integration Demo (2)
</div>
<hr style="border:solid 1px #000080" />
<div style="font-size:10pt; font-family:verdana; width:600px">
This example demonstrates creating a chart using data from a database. The database
query is performed in the containing HTML page. The data are then passed to the chart
generation pages as HTTP GET parameters.
<ul>
    <li><a href="viewsource.py?file=%(SCRIPT_NAME)s">
        View containing HTML page source code
    </a></li>
    <li><a href="viewsource.py?file=dbdemo2a.py">
        View chart generation page source code for upper chart
    </a></li>
    <li><a href="viewsource.py?file=dbdemo2b.py">
        View chart generation page source code for lower chart
    </a></li>
</ul>
<form>
    I want to obtain the revenue data for the year
    <select name="year">
        %(selectYearOptions)s
    </select>
    <input type="submit" value="OK">
</form>
</div>

<img src="dbdemo2a.py?%(httpParam)s">
<br><br>
<img src="dbdemo2b.py?%(httpParam)s">
</body>
</html>
""" % {
    "SCRIPT_NAME" : os.environ["SCRIPT_NAME"],
    "selectYearOptions" : selectYearOptions,
    "httpParam" : httpParam
    })
