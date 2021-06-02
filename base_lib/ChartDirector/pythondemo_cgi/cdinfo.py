#!/usr/bin/python
from pychartdir import *
import string

description = getDescription()
version = "%s.%s.%s" % (((getVersion() >> 24) & 0xff), ((getVersion() >> 16) & 0xff), getVersion() & 0xffff)
copyright = getCopyright()
bootlog = string.replace(getBootLog(), "\n", "<li>")
libTTFtest = string.replace(libgTTFTest(), "\n", "<li>")

print("Content-type: text/html\n")
print("""
<html>
<body topmargin="0" leftmargin="0" rightmargin="0" marginwidth="0" marginheight="0">
<div style="margin:5;">
<div style="font-family:verdana; font-weight:bold; font-size:18pt;">
ChartDirector Information
</div>
<hr color="#000080">
<div style="font-family:verdana; font-size:10pt;">
<ul style="margin-top:0; list-style:square; font-family:verdana; font-size:10pt;">
<li>Description : %(description)s<br><br>
<li>Version : %(version)s<br><br>
<li>Copyright : %(copyright)s<br><br>
<li>Boot Log : <br><ul><li>%(bootlog)s</ul><br>
<li>Font Loading Test : <br><ul><li>%(libTTFtest)s</ul>
</ul>
</div>
</body>
</html>
""" % vars())
