# from time import time
from flask import Flask, render_template 
from flask import Response, render_template, url_for, flash, redirect, request, jsonify, make_response
from flask_cors import CORS 
from crypt import methods
import sys
import json
# sys.path.insert(0, '/Users/leilahudson/Documents/GitHub/Startup/Cruise/backend')
import multiprocessing
from multiprocessing import Manager
import keyboard_features
import min_time_ml
import roadblock_ml

app = Flask(__name__) 
CORS(app)

def keyboard_process():
  proc1 = multiprocessing.Process(target=worker1)
  proc1.start() 

# keyboard functions
def worker1(keyboard1, namespace):
    print("starting keyboard data collection")
    keyboard1 = keyboard_features.keyboard()
    while True:
        namespace.keyboard = keyboard1.realtime(keyboard1.text) 
        print(namespace.keyboard)
        
"""
@app.route("/api/selenium/", methods=["GET","POST"])
def getSelenium():
    mgr = Manager()
    ns = mgr.Namespace()
    mySelenium = web_interface.selenium()
    myList = mySelenium.connectSelenium()
    myUID = myList[0]
    myDriver = myList[1]
    run_multiprocessing.interface_process(ns)
    mySelenium.closeSelenium(myDriver)
"""

@app.route("/api/roadblock/", methods=["GET","POST"])
def checkRoadblock():
    roadblock_buffer = open("roadblock.buf", 'r')
    roadblock = roadblock_buffer.readlines()
    return jsonify(roadblock if roadblock is not None else False)

@app.route("/api/completion/", methods=["GET","POST"])
def checkCompletion():
    completion_buffer = open("completion.buf", 'r')
    completion = completion_buffer.readlines()
    return jsonify(completion if completion is not None else False)

@app.route("/api/url/", methods=["GET","POST"])
def getURL():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        url = json['URL']
        publication_buffer=open("publication.buf", 'w')
        publication_buffer.write(url)
        return jsonify(json), 201
    else:
        return 'Content-Type not supported!'

"""
@app.route("/api/thresholds/", methods=["GET","POST"])
def getThresholds():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        wordThreshold = json['wordThr']
        pageThreshold = json['pageThr']
        publication_buffer=open("thr.buf", 'w')
        publication_buffer.write([wordThreshold, pageThreshold])
        return jsonify(json), 201
    else:
        return 'Content-Type not supported!'
"""

@app.route("/api/fonts/", methods=["GET","POST"])
def getFonts():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        fontFamily = json['FontFamily']
        fontSize = json['FontSize']
        lineSpacing = json['LineSpace']
        print("hi")
        print(json)
        publication_buffer=open("font.buf", 'w')
        publication_buffer.write(fontFamily + "\n" + fontSize + "\n" + lineSpacing)
        return jsonify(json), 201
    else:
        return 'Content-Type not supported!'

@app.route("/api/thr/", methods=["GET","POST"])
def getThresholds():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        requested_json = request.json
        wordCount = requested_json['wordCount']
        pageCount = requested_json['pageCount']
        print(requested_json)
        publication_buffer=open("thr.buf", 'w')
        publication_buffer.write(wordCount + "\n" + pageCount)
        prediction_result = min_time_ml.machine_learning(wordCount)
        return jsonify({"wordcount":prediction_result[0]}), 201
    else:
        return 'Content-Type not supported!'

@app.route("/api/time/", methods=["GET","POST"])
def getTime():
    print("hi")
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        totalTime = json['totalTime']
        print(json)
        publication_buffer=open("font.buf", 'w')
        publication_buffer.write(totalTime)
        return jsonify(json), 201
    else:
        return 'Content-Type not supported!'

@app.route("/api/ml/", methods=["GET","POST"])
def getML():
    prediction_result = roadblock_ml.rb_ml()
    return jsonify({"prediction":prediction_result[0]}), 201

if __name__ == "__main__":
    app.run(port=3000, debug=True)
	# app.run(port=3000)
