#!/usr/bin/env python

""""
# This is the server streamer code for python-gstreamer.
# It's a gstreamer TCP/IP server that listens on
# the localhost for a client to send data to it.
# It shows how to use the tcpserversrc and tcpclientsink
# elements.
# Modified by Vitor Sgobbi, ICEA 2015, Cyber Range ATN Testbed
# GStreamer Python Bindings is distributed under LGPL.

# E necessario ter as libs: python-gst0.10 
# libgstreamer-plugins-base0.10-0 gstreamer0.10-plugins-base 
# gstreamer0.10-plugins-base-apps libgstreamer-plugins-base0.10-0
# python-gst0.10 gstreamer0.10-fluendo-mp3

# Compile both python files as 'python -m py_compile pyAudioStreamerServer.py pyAudioStreamerClient.py'
"""""

import gobject, pygst, sys, logging, logging.config, signal
pygst.require("0.10")
import gst


#create a logging file and its configs
logging.basicConfig(filename='AudioStreamerLogging.log', level=logging.DEBUG,format='%(asctime)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

#create the logger
logger = logging.getLogger('Master server log')
logging.info('\n\nAudio Streamer Server has just started a process!\n')

#add log handler so it can have max of 32mb file
handler = logging.handlers.RotatingFileHandler('AudioStreamerLogging.log', maxBytes=2^15, backupCount=0)
logger.addHandler(handler)

#handling exit by user
def signal_handler_server(signal, frame):
    print '\nYou pressed Ctrl + C, quitting!'
    logging.error('The user exited the Server\n')
    sys.exit(0)

print 'Press Ctrl+C to exit'
if KeyboardInterrupt:
    #time.sleep(1)
    signal.signal(signal.SIGINT, signal_handler_server)

# Callback for the decodebin source pad
def new_decode_pad(dbin, pad, islast):
        pad.link(convert.get_pad("sink"))


# Create a pipeline and add [tcpserversrc ! decodebin ! audioconvert ! alsasink]
pipeline = gst.Pipeline("server")
logging.debug('Pipeline created on server... %s',  pipeline)
# Essa funcao faz o mesmo que o comando "gst-launch-0.10 tcpserversrc port=3000 ! fdsink fd=2
# These commands do the same as gst-launch (server command)
# Only used if you want to stream it via TCP

#tcpsrc = gst.element_factory_make("udpsrc", "source") #tcpserversrc
# set 0.0.0.0 for multicast streaming
#tcpsrc.set_property("host", "0.0.0.0")
#tcpsrc.set_property("port", 3030)
#pipeline.add(tcpsrc)

#Use this part of code if you wanna stream it via UDP
#udpsink = gst.element_factory_make("udpsink")
#udpsink.set_property("host", "0.0.0.0")
#udpsink.set_property("port", 3030)
udpsrc = gst.element_factory_make("udpsrc", "source")
udpsrc.set_property("port", 3030)
logging.info('Gst source: %s', udpsrc)
#udpsrc.set_property("host", "0.0.0.0")

#pipeline.add(udpsink)
pipeline.add(udpsrc)


decode = gst.element_factory_make("decodebin", "decode") #decodes a mp3 file into audio data #mad for .mp3 and decodebin for .ogg #dynamic pad
decode.connect("new-decoded-pad", new_decode_pad)
pipeline.add(decode)

#tcpsrc.link(decode)
udpsrc.link(decode)

#queue = gst.element_factory_make("queue", "queueaudio")

#"audioconvert" translates the decoded audio data into a format playable by the audio device.
convert = gst.element_factory_make("audioconvert", "convert")
pipeline.add(convert)

#sink = sink pads, it accepts data from the previous element in the pipeline.
#the next is a plugin, autoaudiosink automatically detects the audio sink for the audio output
#plays the audio #alsasink =/= from autoaudiosink?
sink = gst.element_factory_make("alsasink", "sink")
pipeline.add(sink)
convert.link(sink)

#equalizer = gst.element_factory_make('equalizer-3bands', 'equalizer') #change the audio bands
#equalizer.set_property('band1', -24.0)
#equalizer.set_property('band2', -24.0)
#pipeline.add(equalizer)

# Ensure all elements were created successfully.
if (not pipeline or not decode or not convert or not sink):
    print 'Server problem found... Not all elements could be created.'
    logging.error('Server problem found. Not all elements could be created, quitting.')
    exit(-1)

#change pipeline state to playing
pipeline.set_state(gst.STATE_PLAYING)
print 'Gst server is currently on!'

def gstMsg():
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    #bus.connect("message", gst.element_state_get_name(1))
    print bus

#gstMsg()

def printMsg():
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    msg = bus.timed_pop_filtered(gst.CLOCK_TIME_NONE,
                                 gst.MESSAGE_ERROR | gst.MESSAGE_EOS)
    pipeline.set_new_stream_time(1) #default set to 15

    pipeline.set_state(gst.STATE_NULL)
    print msg

    restart = pipeline.set_state(gst.STATE_PLAYING)
    #print 'Playing files...'
    if (restart == gst.STATE_CHANGE_FAILURE):
        print >> sys.stderr, ("Unable to set pipeline to playing state")
        exit (-1)
    elif (restart == gst.STATE_CHANGE_NO_PREROLL):
        pipeline.continue_state(sink)
        print >> sys.stderr, ("There is no preroll")
    elif (gst.STATE_PLAYING):
        print >> sys.stderr, ("\nSome sound file was played...")
        sink.set_state(gst.STATE_READY)

printMsg()


#pipeline.set_state(gst.EVENT_FLUSH_START)
#pipeline.get_auto_flush_bus()
#pipeline.continue_state(0)

#pipeline.set_state(gst.STATE_NULL)
pipeline.set_state(gst.STATE_CHANGE_NULL_TO_READY)
pipeline.set_state(gst.STATE_READY)

#loop = gobject.MainLoop()
#pipeline.connect("decode",loop.quit)
#loop.run()

# enter into the mainloop
loop = gobject.MainLoop()
gobject.threads_init()
context = loop.get_context()
#loop.run()

while True:
    context.iteration(True)
    pipeline.set_state(gst.STATE_PLAYING)
    #printMsg()