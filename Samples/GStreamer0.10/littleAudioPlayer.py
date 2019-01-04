#!/usr/bin/env python
import os, random

def rndmp3 ():
   randomfile = random.choice(os.listdir("/home/vitor/Music/"))
   file = '/home/vitor/Music/'+ randomfile
   os.system ('omxplayer -o local' + file)

rndmp3 ()
