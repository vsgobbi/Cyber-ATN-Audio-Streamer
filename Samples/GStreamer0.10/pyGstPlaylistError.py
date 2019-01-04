import pygst, gobject, time, sys
pygst.require("0.10")
import gst

class AudioPlayer:
         def __init__(self):
                 self.songs = ['Holy Diver.mp3','Paranoid.mp3','Fast as a Shark.mp3']

                 # create a new gstreamer pipeline
                 self.pipeline = gst.Pipeline("mypipeline")

                 # add a file source to the pipeline
                 self.filesrc = gst.element_factory_make("filesrc","source")
                 self.pipeline.add(self.filesrc)

                 # add a generic decoder to the pipeline and link it to thesource
                 self.decode = gst.element_factory_make("decodebin","decode")
                 self.decode.connect("new-decoded-pad", self.decode_link)
                 self.pipeline.add(self.decode)
                 self.filesrc.link(self.decode)

                 # add a convertor to the pipeline
                 self.convert = gst.element_factory_make("audioconvert","convert")
                 self.pipeline.add(self.convert)

                 # add an alsa sink to the pipeline and link it to theconvertor
                 self.sink = gst.element_factory_make("alsasink", "sink")
                 self.pipeline.add(self.sink)
                 self.convert.link(self.sink)

                 # start playing
                 self.filesrc.set_property("location", self.songs.pop(0))
                 self.pipeline.set_state(gst.STATE_PLAYING)

         def decode_link(self, dbin, pad, islast):
                 pad.link(self.convert.get_pad("sink"))

         def next(self):
                 self.convert.unlink(self.sink)
                 self.filesrc.set_state(gst.STATE_NULL)
                 self.filesrc.set_property("location", self.songs.pop(0))
                 self.convert.link(self.sink)
                 self.pipeline.set_state(gst.STATE_PLAYING)
                 return True

player = AudioPlayer()
loop = gobject.MainLoop()
gobject.threads_init()
context = loop.get_context()

while 1:
         value = sys.stdin.readline()
         if value == "next\n":
                 player.next()
         context.iteration(True)
