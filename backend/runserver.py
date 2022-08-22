from sys import argv, exit, stderr
from routes import app
import web_interface
import multiprocessing
from multiprocessing import Process
import workers

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
    proc1 = multiprocessing.Process(target=main)
    proc1.start()
    proc1.join()
    print("is process 1 alive? ", proc1.is_alive() == True)
    while proc1.is_alive() == True:
        mySelenium = web_interface.selenium()
        myList = mySelenium.connectSelenium()
        myUID = myList[0]
        myDriver = myList[1]
        proc2 = multiprocessing.Process(target=workers.worker1, args=[mySelenium, myUID])
        proc3 = multiprocessing.Process(target=workers.worker2)
        proc2.start()
        proc3.start()
        proc2.join()
        proc3.join()
    # mySelenium.closeSelenium(myDriver)
