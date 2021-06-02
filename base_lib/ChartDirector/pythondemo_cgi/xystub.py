#!/usr/bin/python
import cgi, sys, os

# Get HTTP query parameters
query = cgi.FieldStorage(keep_blank_values = 1)

print("Content-type: text/html\n")
print("""
<html>
<body style="margin:5px 0px 0px 5px">
<div style="font-size:18pt; font-family:verdana; font-weight:bold">
    Simple Clickable XY Chart Handler
</div>
<hr style="border:solid 1px #000080" />
<div style="font-size:10pt; font-family:verdana; margin-bottom:20px">
    <a href="viewsource.py?file=%(SCRIPT_NAME)s">View Source Code</a>
</div>
<div style="font-size:10pt; font-family:verdana;">
<b>You have clicked on the following chart element :</b><br />
<ul>
    <li>Data Set : %(dataSetName)s</li>
    <li>X Position : %(x)s</li>
    <li>X Label : %(xLabel)s</li>
    <li>Data Value : %(value)s</li>
</ul>
</div>
</body>
</html>
""" % {
    "SCRIPT_NAME" : os.environ["SCRIPT_NAME"],
    "dataSetName" : query["dataSetName"].value,
    "x" : query["x"].value,
    "xLabel" : query["xLabel"].value,
    "value" : query["value"].value
    })
