from sys import argv, exit, stderr
from routes import app
import run_multiprocessing
import web_interface
from multiprocessing import Process
import threading


finished = None
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
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == '__main__':
    print("process 3")
    # main()
    proc1 = threading.Thread(target=main)
  # p = multiprocessing.Process(target=selenium)
  # p.start()
    proc1.start()
    while finished is None:
        print("stuck")
        pass
    proc1.join()
    print("amir&leila")
    run_multiprocessing.main()
    # mySelenium.closeSelenium(myDriver)
