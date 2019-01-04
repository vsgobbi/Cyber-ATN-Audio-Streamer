 #!/usr/bin/python
 import pygst
 pygst.require('0.10')
 import gst

 import pygtk
 pygtk.require('2.0')
 import gtk

 # this is very important, without this, callbacks from gstreamer thread
 # will messed our program up


 def on_new_decoded_pad(dbin, pad, islast):
     structure_name = pad.get_caps()[0].get_name()
     decode = pad.get_parent()
     pipeline = decode.get_parent()
     if structure_name.startswith("video"):
            queuev = pipeline.get_by_name('queuev')
        decode.link(queuev)
     if structure_name.startswith("audio"):
            queuea = pipeline.get_by_name('queuea')
    print queuea
        decode.link(queuea)


 def main():
     pipeline = gst.Pipeline('pipleline')

     filesrc = gst.element_factory_make("filesrc", "filesrc")
     filesrc.set_property('location', '/home/thothadri/Videos/nuclear.avi')

     decode = gst.element_factory_make("decodebin", "decode")

     queuev = gst.element_factory_make("queue", "queuev")

     sink = gst.element_factory_make("autovideosink", "sink")

     queuea = gst.element_factory_make("queue", "queuea")

     convert = gst.element_factory_make('audioconvert', 'convert')

     sink_audio = gst.element_factory_make("autoaudiosink", "sink_audio")

     pipeline.add(filesrc,decode,queuev,queuea,convert,sink,sink_audio)

     gst.element_link_many(filesrc, decode)
     gst.element_link_many(queuev,sink)
     gst.element_link_many(queuea,convert,sink_audio)

     decode.connect("new-decoded-pad", on_new_decoded_pad)

     pipeline.set_state(gst.STATE_PLAYING)



 main()
 gtk.gdk.threads_init()
 gtk.main()  
