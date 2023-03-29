python2

1)
python -m SimpleHTTPServer 80

2)
import SimpleHTTPServer
import SocketServer

PORT = 80
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("192.168.0.107",PORT),Handler)
print "serving at port", PORT
httpd.serve_forever()

参考:
https://docs.python.org/2/library/simplehttpserver.html

python3(等待更新)
