__author__ = 'vitor'

#!/usr/bin/env python

""""
 This is the client code for python-gstreamer.
 The gstreamer TCP/IP client sends a file
 through a tcpclientsink to a server on localhost
 The default location to our Cyber Range ATN Testbed sounds is "/opt/crat/core/home/sounds/"
 Created at ICEA (Brazilian Airspace Control Institute)
 Vitor Sgobbi, 2015
"""""


""""
# NOTES:
# After a long time testing the codecs missing and searching for it.
# To consider playing .mp3 files, check if 'mad' element plugin is installed with gst0.10, install it with:
# apt-get install gstreamer0.10-fluendo-mp3


# Example of how to test with gst-launch-0.10 terminal command:
# gst-launch-0.10 tcpserversrc host=localhost port=3000 ! decodebin ! audioconvert ! alsasink
# gst-launch-0.10 filesrc location=/home/vitor/Music/Gorillaz_Feel_Good_Inc.mp3 ! tcpclientsink host=localhost port=3000
"""""



import gobject, pygst
pygst.require("0.10")

import os, sys, random, fnmatch, glob, time, signal, logging, logging.config, logging.handlers
from os.path import expanduser
#import threading, getopt, Queue #unused

# Setting GST_DEBUG_DUMP_DOT_DIR environment variable enables us to have a dotfile generated
os.environ["GST_DEBUG_DUMP_DOT_DIR"] = "/tmp"
os.putenv('GST_DEBUG_DUMP_DIR_DIR', '/tmp')
try:
    import gi
except:
    pass
try:
    import pygst
    pygst.require("0.10")
    import gst
except:
    pass

#create a logging file and its configs
logging.basicConfig(filename='AudioStreamerLogging.log', level=logging.DEBUG,format='%(asctime)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

#create the logger
logger = logging.getLogger('Noise Client log') #__name__
logging.info('\n\nNoise client has just connected...\n')

#add log handler so it can have max of 32mb file
handler = logging.handlers.RotatingFileHandler('AudioStreamerLogging.log', maxBytes=2^15, backupCount=0)
logger.addHandler(handler)

# create the pipeline and add client [ filesrc ! tcpclientsink ]
pipeline = gst.Pipeline("client")

#player = gst.element_factory_make("playbin", "player")
src = gst.element_factory_make("filesrc", "source")
logger.debug('Debug msg: %s' % src + ' created')


pipeline = gst.Pipeline("client")
src = gst.element_factory_make("filesrc", "source")


files = []
poppedfiles = []
path = os.path.join("/opt/crat/core/home/sounds/NOISE/")


def getFiles(path):
    if os.path.isdir(path) == False:
        print "\nThe required folder %s" % path + " doesn't exist\n" + "Please extract all NOISE songs or contact the admin\n"
        logging.error('The user has no path: %s', path)
        exit(-1)
    #make it even more randomly :D
    random.seed()
    for f in sorted(os.listdir(path), key=lambda k: random.random()):
        f = os.path.join(path, f)
        if os.path.isdir(f): getFiles(f)
        if len(files) > 398: break
        if fnmatch.fnmatch(f, '*.mp3'):
            files.append(f)
        f.rstrip().split('\n')
        random.shuffle(files) #return none, just rand again

        #rand.append(files)s
        #print rand

        if len(files) < 1:
            print "Hey, we must have at least one playable sound file!"
            logging.error('The path: %s', path + 'seems to be empty!')
            return

getFiles(os.path.expanduser(path))
logging.info('Total of %s' % len(files) + ' files found for NOISE.')

def signal_handler(signal, frame):
    print '\nYou pressed Ctrl + C, quitting!'
    logging.warn('The user exited the NOISE client streamer.')
    sys.exit(0)

print 'Press Ctrl+C to exit'
if KeyboardInterrupt:
    #time.sleep(1)
    signal.signal(signal.SIGINT, signal_handler)

#add all elements to pipeline
pipeline.add(src)

#pipeline.add(player)

#set client properties for TCP usage and create pipeline #uncomment it if you wish to receive streaming data via TCP
#client = gst.element_factory_make("tcpclientsink", "client")

#set client properties for UDP usage and create pipeline
client = gst.element_factory_make("udpsink", "client")

pipeline.add(client)
client.set_property("host", "0.0.0.0")
client.set_property("port", 3030)
src.link(client)
logging.debug(src)
logging.debug('%s' % client)
logging.info("Client UDP sink configured at host: 0.0.0.0 and UDP port usage at: 3030")


#check if pipeline and sources are okay
if (not pipeline or not src or not files):
    print 'Client problem found... Not all elements could be created.'
    exit(-1)


def statePlay():
    i = 1
    for n in files:
        #gst.StateChangeReturn
        #pipeline.set_state(gst.STATE_PLAYING)
        #pipeline.continue_state(gst.BUFFERING_STREAM)

        while True:
            print "\nI'm in..." #just for testing because I'm a newbie guy
            #i=range(0,len(files))
            #poppedfiles = files.pop(-1) # -1 get the item at end #if want to remove a specific value use : indexList.remove()
            poppedfiles = random.choice(files)
            #pipeline.set_state(gst.BUFFER_LIST_CONTINUE)
            #statePlay()
            src.set_property("location", poppedfiles)
            print 'Playing file: %s' % poppedfiles
            logging.debug('Noise iteration: %s' % i + ', currently playing file: %s' % poppedfiles)
            pipeline.set_state(gst.STATE_PLAYING)
            #pipeline.set_state(gst.STATE_CHANGE_SUCCESS) #not handling buffer, making audio sink every time
            random.seed() #seed again
            gammapdf = random.gammavariate(1, 1) #noise gamma distribution statistics where alpha = 1 and beta = 1
            print "The random gamma probability distribution function has generated: %s" % round(gammapdf, 1) + " seconds of interarrival time \n"

            time.sleep(gammapdf) # get the length of file and add to time sleep!

            if i >=len(files):
                i = 0 #come back to index zero
                print >> sys.stderr, "Reached the end of files, returning..."
                logging.debug('Reached the end of NOISE files! %s' % len(files))
            if n <=i:
                #n = 0
                print >> sys.stderr, "Reached the bottom!", n
                pipeline.set_state(gst.StateChangeReturn(1))

            #pipeline.set_state(gst.StateChangeReturn(1))
            pipeline.set_state(gst.STATE_CHANGE_SUCCESS) #this is making it to play the same audio file!
            i+=1

        #n+=1
        #i+=1
    logger.debug(gst.STATE_PLAYING)
    logger.info("Did I reach the end?")


def printMsgs():
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    #msg = bus.timed_pop_filtered(gst.CLOCK_TIME_NONE, gst.MESSAGE_ERROR | gst.MESSAGE_EOS)
    msg = bus.timed_pop_filtered(gst.MESSAGE_ERROR, gst.MESSAGE_EOS)
    pipeline.set_new_stream_time(1) #default was 15

    restart = pipeline.set_state(gst.STATE_PLAYING)
    #print 'Playing files...'
    if (restart == gst.STATE_CHANGE_FAILURE):
        print >> sys.stderr, ("Unable to set pipeline to playing state, pulling over!")
        exit (-1)
    elif (restart == gst.STATE_CHANGE_NO_PREROLL):
        print >> sys.stderr, ("There is no preroll")
        pipeline.continue_state(src)
    pipeline.set_state(gst.STATE_NULL)
    logging.info("Get status: %s", restart)
    logger.debug(restart)
    print msg



loop = gobject.MainLoop()
gobject.threads_init()
context = loop.get_context()
statePlay()
printMsgs()

while 1:
    #pipeline.set_state(gst.STATE_PLAYING)
    #print "state playing in the while loop"
    context.iteration(True)

