#!/usr/bin/python
import cgi, sys, string

#get HTTP query parameters
query = cgi.FieldStorage()
if (hasattr(string, "find") and string.find or (lambda a, b: a.find(b)))(query["img"].value, "cd__") == -1 :
	raise ("Filename '%s' is not a temporary file created by ChartDirector Ver 4.1 or above." % (query["img"].value))
	
f = open(query["img"].value, "rb")
print("Content-type: image/png\n")
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
