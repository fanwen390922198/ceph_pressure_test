#!/usr/bin/python
import os, sys, cgi, string

query = cgi.FieldStorage()
filename = os.path.basename(query["file"].value)

extPos = (hasattr(string, "rfind") and string.rfind or (lambda a, b: a.rfind(b)))(filename, ".")
mimeType = None
if extPos != -1 :
	ext = (hasattr(string, "lower") and string.lower or (lambda a: a.lower()))(filename[extPos + 1:])
	if ext == "js" :
		mimeType = "application/x-javascript"
	elif ext == "png" :
		mimeType = "image/png"
	elif ext == "gif" :
		mimeType = "image/gif"
	elif ext == "jpg" or ext == "jpeg" :
		mimeType = "image/jpeg"
	elif ext == "cur" :
		mimeType = "application/octet-stream"
	
if mimeType is None :
	raise 'Invalid file extension for "%s"' % filename

print("Cache-Control: max-age=43200");
print("Content-type: %s\n" % mimeType)
f = open(os.path.join(os.path.dirname(sys.argv[0]), filename), "rb")
try :
    import msvcrt
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
except :
    pass
if sys.version[:3] >= "3.0" :
	sys.stdout.flush()
	sys.stdout.buffer.write(f.read())
else :
	sys.stdout.write(f.read())
f.close()
