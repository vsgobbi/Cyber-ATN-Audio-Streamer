__author__ = 'vitor'
#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import sys
import gst
import gobject

songs = [line.strip().split(" | ") for line in open("/opt/crat/core/home/sounds/ATC/ATC.m3u")]
ordered = songs[:]
shuffle = False
current = 0
repeat = False
bin = gst.element_factory_make("playbin")
bin.set_property("uri", "file:///opt/crat/core/home/sounds/ATC/313.mp3")
bus = bin.get_bus()

def on_eos(bus, msg):
    print 'EOS'
    quit()

def nowPlayingP(current):
    global playstring
    try:
        playstring = "Playing: %s | %s" % (songs[current][2], songs[current][0])
        bus.add_signal_watch()
        bus.connect('message::eos', on_eos)
        bin.set_state(gst.STATE_PLAYING)
        main = gobject.MainLoop()
        main.run()
    except:
        print "The number passed was not valid, please use a lower number"
        #return
        print playstring

def nowPlaying():
    global playstring
    playstring = "Now playing: %s | %s" % (songs[current][2], songs[current][0])
    print playstring

def help():
    global current
    print "Play \t\tStart playing"
    print "Next \t\tPlay next track"
    print "Next [num]\t\tGo forward [num] amount of tracks"
    print "Prev \t\tPlay previous track"
    print "Prev [num]\t\tGo back [num] amount of tracks"
    print "Repeat \t\tEnable repeats"
    print "Shuffle \t\tEnable shuffle"
    print "Status \t\tPrint currently playing track & weather shuffle & repeat are enabled"
    print "List \t\tList the songs in playlist"
    print "&& \t\tUsed to join commands together (see examples)"
    print "Help \t\tPrint this message out"
    print
    print "Eg:"
    print "play && next 10 && list"
    print "status"
    print "play && shuffle && repeat"
help()

while True:
        try:
            command = raw_input("Enter command: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print
        #exit()
        if command == "play":
            nowPlaying()
        elif command == "pause":
            print "Paused"
        elif command == "next":
            if not repeat:
                current += 1
            nowPlaying()
        if command == "prev":
            if not repeat:
                current -= 1
            nowPlaying()
        if command.split(" ")[0] == "next":
            oldcurrent = current
            current += int(command.split(" ")[1])
        if current > len(songs):
            print "The number you entered is more thant the number of songs!"
            print "Just doing 'next' ('next 1') instead"
            current = oldcurrent + 1
            nowPlaying()
        elif command.split(" ")[0] == "prev":
            oldcurrent = current
            current -= int(command.split(" ")[1])
        if current > len(songs):
            print "The number you entered is invalid!"
            print "Just doing 'prev' ('prev 1') instead"
            current = oldcurrent - 1
        elif current < 0:
            print "The number you entered is invalid!"
            current = 0
            nowPlayingP(current)
        elif command == "shuffle":
            shuffle = not shuffle
        if shuffle:
            random.shuffle(songs)
            print "Shuffle: on"
        else:
            songs = ordered[:]
            print "Shuffle: off"
        if command == "repeat":
            repeat = not repeat
        if repeat:
            print "Repeat: on"
        else:
            print "Repeat: off"
        if command == "status":
            print playstring
        if shuffle:
            print "Shuffle: on"
        else:
            print "Shuffle: off"
        if repeat:
            print "Repeat: on"
        else:
            print "Repeat: off"
        if command == "list":
            for l in songs:
                print l

        elif command == "help": help()

        elif len(command.split(" && ")) > 0:
            for i in command.split(" && "):
                if i == "play":
                    nowPlaying()
        elif i == "pause":
            print "Paused"
        elif i == "next":
            if not repeat:
                current += 1
                nowPlaying()
        elif command == "prev":
            if not repeat:
                current -= 1
                nowPlaying()
        if i.split(" ")[0] == "next":
            oldcurrent = current
            current += int(i.split(" ")[1])
        if current > len(songs):
            print "The number you entered is more thant the number of songs!"
            print "Just doing 'next' ('next 1') instead"
            current = oldcurrent + 1
            nowPlaying()
        elif i.split(" ")[0] == "prev":
            current -= int(i.split(" ")[1])
            nowPlayingP(current)
        elif i == "shuffle":
            shuffle = not shuffle
        if shuffle:
            random.shuffle(songs)
            print "Shuffle: on"
        else:
            songs = ordered[:]
            print "Shuffle: off"
        if i == "repeat":
            repeat = not repeat
        if repeat:
            print "Repeat: on"
        else:
            print "Repeat: off"

        if i == "status":
            print playstring
        if shuffle:
            print "Shuffle: on"
        else:
            print "Shuffle: off"
        if repeat:
            print "Repeat: on"
        else:
            print "Repeat: off"

        if i == "list":
            for l in songs:
                print l

        if i == "help": help()
        else:
            print "Please enter a valid command"
        #else:
        #    print "Please enter a valid command"