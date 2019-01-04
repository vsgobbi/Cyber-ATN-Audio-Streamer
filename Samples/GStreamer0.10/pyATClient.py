#!/usr/bin/env python

__author__ = 'vitor'


# This is the client code for python-gstreamer.
# The gstreamer TCP/IP client sends a file
# through a tcpclientsink to a server on localhost


import gobject, pygst
#from audioStreamPlayer import controller
import os, random

pygst.require("0.10")


try:
    import pygst
    pygst.require("0.10")
    import gst
except:
    pass


def on_eos(bus, msg):
    print "Everything ok"
    main.quit()



def play(f):
    print "Playing %s" %(f.rstrip())
    bin = gst.element_factory_make("playbin")
    bin.set_property("uri", "file://" + f.rstrip())
    bin.set_state(gst.STATE_PLAYING)
    bus = bin.get_bus()
    bus.add_signal_watch()
    bus.connect('message::eos', on_eos)
    #set client properties and create pipeline
    client = gst.element_factory_make("tcpclientsink", "client")
    bin.add(client)
    client.set_property("host", "0.0.0.0")
    client.set_property("port", 3030)
    bin.link(client)
    global main
    main = gobject.MainLoop()
    main.run()
    print "running"




file = open("/opt/crat/core/home/sounds/ATC/ATC.m3u", "r")
countOne = 1
count = 1
files = []

for line in file.readlines():
    if countOne > 2:
        if count >= 2:
            files.append(os.path.abspath(line))
    count = 0
    count += 1
    countOne += 1

random.shuffle(files)
for audio in files:
    #on_eos()
    play(audio)


