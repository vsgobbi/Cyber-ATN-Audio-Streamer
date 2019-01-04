import os
import gst
import gobject
import random

files = []
file = open("/opt/crat/core/home/sounds/ATC/ATC.m3u", "r")

def on_eos(bus, msg):
	print "hi"
	main.quit()


def play(f):
	print "Playing %s" % (f.rstrip())
	bin = gst.element_factory_make("playbin")
	bin.set_property("uri", "file://" + f.rstrip())
	bin.set_state(gst.STATE_PLAYING)
	bus = bin.get_bus()
	bus.add_signal_watch()
	bus.connect('message::eos', on_eos)
	global main
	main = gobject.MainLoop()
	main.run()
	print "g"


count1 = 1
count = 1

for line in file.readlines():
	if count1 > 2:
	   if count >= 2:
			files.append(os.path.abspath(line))
			count = 0
			count += 1
			count1 += 1

random.shuffle(files)
for audio in files:
	play(audio)
