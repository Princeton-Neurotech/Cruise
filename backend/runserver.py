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

def handle(connection, address):
    try:
        while True:
            data = connection.recv(1024)
            if data == "":
                break
            else :
                print("RECEIVE DATA : " + str(data))
                xdata = data.strip()
                xdata = data.split(" ")
                for xd in xdata :
                    print("PUT Task : " + str(xd))
                    QueueTask.put((xd), block=True, timeout=5)
                connection.sendall(data)
    except Exception as e: 
        print(e)
    finally:
        connection.close()

class Server(object):
  def __init__(self, hostname, port):
    self.hostname = hostname
    self.port = port

  def start(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind((self.hostname, self.port))
    self.socket.listen(1)
    while True:
      conn, address = self.socket.accept()
      process = multiprocessing.Process(target=handle, args=(conn, address))
      process.daemon = True
      process.start()

def f_Processor():
  time.sleep(10)
  print('PROCESSOR Starting')
  while 1:
    try :
      job = QueueTask.get(True,1)
      print("GET Task : " + str(job))
      time.sleep(5)
    except Exception as err :
      pass
  print('PROCESSOR Exiting')

ok_message = 201
nok_message = 404
ok_message = ok_message.to_bytes(4, 'big')
nok_message = nok_message.to_bytes(4, 'big')
finished = None

def process_start(s_sock):
    content = s_sock.recv(32)
    s_sock.send(ok_message)
    s_sock.close()
    # time.sleep(10)
    sys.exit(0) # kill the child process

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
    """
    server = Server("localhost", 3000)
    QueueTask = Queue()
    try:
        p = multiprocessing.Process(name='Processing', target=f_Processor)
        p.start()
        server.start()
    except:
        print("Unexpected exception")
    finally:
        for process in multiprocessing.active_children():
            process.terminate()
            process.join()
    print("All done")
    """
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((sys.argv[1], int(sys.argv[2])))
    print('listen on address %s and port %d' % (sys.argv[1], int(sys.argv[2])))
    s.listen(1)
    try:
        while True:
            try:
                s_sock, s_addr = s.accept()
                proc1 = Process(target=process_start, args=(s_sock,))
                proc1.start()
                """
    proc1 = threading.Thread(target=main)
    proc1.start()
    # main()
    url = appscript.app('Google Chrome').windows.tabs.URL()
    mySelenium = web_interface.selenium()
    myUID = mySelenium.connectSelenium(url)
    proc2 = threading.Thread(target=workers.worker1, args=[mySelenium, myUID])
    proc2.start()
    """
            except socket.error:
                # stop the client disconnect from killing us
                print('got a socket error')

    except Exception as e:
        print('an exception occurred!')
        print(e)
        sys.exit(1)
    finally:
        s.close()
    """
