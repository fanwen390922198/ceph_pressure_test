#!/usr/bin/python
import cgi, os, sys

#get HTTP query parameters
query = cgi.FieldStorage()

print("Content-type: text/html\n")
print("<html>")
print("<body>")

myFile = query["file"].value

print("<p style='font-size:14pt; font-family:verdana; font-weight:bold'>%s</p>" % myFile)
print("<p style='font-size:10pt; font-family:verdana;'><a href='javascript:history.go(-1);'>Back to Chart Graphics</a></p>")

print("<xmp>")
f = open(os.path.join(os.path.dirname(sys.argv[0]), os.path.basename(myFile)), "r")
print(f.read())
f.close()
print("</xmp>")

print("</body>")
print("</html>")
