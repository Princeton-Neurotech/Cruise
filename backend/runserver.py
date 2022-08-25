from sys import argv, exit, stderr
from routes import app
import web_interface
import multiprocessing
from multiprocessing import Process, Queue
import workers
import socket
import sys
import time
import appscript
import threading

def main():
    global finished
    if len(argv) != 3:
        print(len(argv))
        # print('Usage: ' + argv[1] + ' port', file=stderr)
        exit(1)

    try:
        port = int(argv[2])
    except:
        print('Port must be an integer.', file=stderr)
        exit(1)

    try:
        finished = 1
        app.run(host='0.0.0.0', port=port, debug=True, threaded=False, processes=2, use_reloader=False)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == '__main__':
    proc1 = threading.Thread(target=main)
    proc1.start()
    url = appscript.app('Google Chrome').windows.tabs.URL()
    mySelenium = web_interface.selenium()
    myUID = mySelenium.connectSelenium(url)
    proc2 = threading.Thread(target=workers.worker1, args=[mySelenium, myUID])
    proc2.start()