#!/usr/bin/env python
import gae2django
# Use gae2django.install(server_software='Dev') to enable a link to the
# admin frontend at the top of each page. By default this link is hidden.
gae2django.install(server_software='Django')

from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

def monkey_patch_for_multi_threaded():
    # This monkey-patches BaseHTTPServer to create a base HTTPServer class that 
    # supports multithreading 
    import BaseHTTPServer, SocketServer  
    OriginalHTTPServer = BaseHTTPServer.HTTPServer

    class ThreadedHTTPServer(SocketServer.ThreadingMixIn, OriginalHTTPServer):  
        def __init__(self, server_address, RequestHandlerClass=None):  
            OriginalHTTPServer.__init__(self, server_address, RequestHandlerClass)  

    BaseHTTPServer.HTTPServer = ThreadedHTTPServer

if __name__ == "__main__":
    monkey_patch_for_multi_threaded()
    execute_manager(settings)
