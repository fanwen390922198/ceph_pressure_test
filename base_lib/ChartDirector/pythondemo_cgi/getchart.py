#!/usr/bin/python
import cgi, sys, string

query = cgi.FieldStorage()
filename = query["img"].value
if (hasattr(string, "find") and string.find or (lambda a, b: a.find(b)))(filename, "cd__") == -1 :
	raise ('Filename "%s" does not seem created by ChartDirector' % filename)
extPos = (hasattr(string, "rfind") and string.rfind or (lambda a, b: a.rfind(b)))(filename, ".")
if extPos == -1 :
	ext = "png"
else :
	ext = (hasattr(string, "lower") and string.lower or (lambda a: a.lower()))(filename[extPos + 1:])

contentType = "image/png"	
if ext == "gif" :
	contentType = "image/gif"
elif ext == "jpg" or ext == "jpeg" :
	contentType = "image/jpeg"
elif ext == "bmp" :
	contentType = "image/bmp"
elif ext == "wmp" or ext == "wbmp" :
	contentType = "image/vnd.wap.wbmp"
elif ext == "svg" or ext == "svgz" :
	contentType = "image/svg+xml"
elif ext == "pdf" :
	contentType = "application/pdf"
elif ext == "map" or ext == "gz" :
	contentType = "text/html; charset=utf-8"

print("Content-type: %s" % contentType)
if ext == "gz" or ext == "svgz" :
	print("Content-Encoding: gzip")
if (hasattr(query, "has_key") and query.has_key or (lambda a, b = query: a in b))("filename") :
	print("Content-Disposition: inline; filename=%s" % query["filename"].value)
print("")

f = open(filename, "rb")
try :
    import msvcrt, os
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
except :
    pass
if sys.version[:3] >= "3.0" :
	sys.stdout.flush()
	sys.stdout.buffer.write(f.read())
else :
	sys.stdout.write(f.read())
f.close()
