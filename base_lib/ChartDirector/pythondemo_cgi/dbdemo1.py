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
    Database Integration Demo (1)
</div>
<hr style="border:solid 1px #000080" />
<div style="font-size:10pt; font-family:verdana; margin-bottom:20px">
&#8226; <a href="viewsource.py?file=%(SCRIPT_NAME)s">
    View containing HTML page source code
</a>
<br />
&#8226; <a href="viewsource.py?file=dbdemo1a.py">
    View chart generation page source code
</a>
<br />
<br />
<form>
    I want to obtain the revenue data for the year
    <select name="year">
        %(selectYearOptions)s
    </select>
    <input type="submit" value="OK">
</form>
</div>

<img src="dbdemo1a.py?year=%(selectedYear)s">

</body>
</html>
""" % {
    "SCRIPT_NAME" : os.environ["SCRIPT_NAME"],
    "selectYearOptions" : selectYearOptions,
    "selectedYear" : selectedYear
    })
