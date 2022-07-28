from sys import argv, exit, stderr
from routes import app
import run_multiprocessing
import web_interface

def main():

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
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == '__main__':
    main()
    mySelenium = web_interface.selenium()
    myList = mySelenium.connectSelenium()
    myUID = myList[0]
    myDriver = myList[1]
    run_multiprocessing.interface_process()
    mySelenium.closeSelenium(myDriver)
