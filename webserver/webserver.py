#!/usr/bin/python

import string,cgi,time
from os import curdir, sep, system
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#import pri

riddles = {
	# Ivo Andric
	'00001.rid' : ([2], 'andric.html'),
	# Sava
	'00002.rid' : ([3, 4], 'sava.html'),
	# Bruce Lee
	'00003.rid' : ([3], 'lee.html'),
	# Felline
	'00004.rid' : ([4], 'fellini.html'),
	# Bush
	'00005.rid' : ([5], 'bush.html'),
	# Nusic
	'00006.rid' : ([], 'nusic.html')
}

ledsOn = set([])

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith(".rid"):
		page = riddles[self.path[1:]][1]
                f = open(curdir + sep + "pages" + sep + page) #self.path has /test.html
		#note that this potentially makes every file on your computer readable by the internet

		# turn off all previous LEDs
		for node in ledsOn:
			print "turn OFF :", node
			system("./leds.sh %s 0" % node)
		ledsOn.clear()
	

		# look if we need to trigger node's LED
		lednodes = riddles[self.path[1:]][0]
		if len(lednodes) != 0:
			for node in lednodes:
				system("./leds.sh %s 4" % node)
				ledsOn.add(node)


                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            if self.path.endswith(".esp"):   #our dynamic content
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write("hey, today is the" + str(time.localtime()[7]))
                self.wfile.write(" day in the year " + str(time.localtime()[0]))
                return
                
            return
                
        except IOError:
        	self.send_error(404,'File Not Found: %s' % self.path)
     

def main():
    try:
        server = HTTPServer(('', 8080), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

