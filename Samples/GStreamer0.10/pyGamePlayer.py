#!/usr/bin/env python

__author__ = 'vs'

import pygame
import os.path
import logging
import random
import re
import sys

play_stereo = True
songNumber = 0
x = 0
SONG_END = pygame.USEREVENT + 1

pygame.display.set_caption("Pygame player")
#screen = pygame.display.set_mode((800, 800), 0, 32)
pygame.init()


#constroi lista com todos os arquivos do diretorio dado com os seguintes formatos
def build_file_list():
    file_list = []
    for root, folders, files in os.walk(folderPath):
        folders.sort()
        files.sort()
        for filename in files:
            if re.search(".(aac|mp3|wav|flac|m4a|pls|m3u)$", filename) != None: #re-compatible interface for the sre matching engine
                file_list.append(os.path.join(root, filename))
    return file_list

#tocar de modo aleatorio
def play_songs(file_list):
    random.shuffle(file_list)
    pygame.mixer.music.load(file_list[songNumber])
    pygame.mixer.music.play(1)

    for num, song in enumerate(file_list):
       if num == songNumber:
           continue # se ja estiver tocando
       pygame.mixer.music.queue(song)

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_q:
                folderPath = "/opt/crat/core/home/sounds/ATC/"
                files = build_file_list()
                play_songs(files)

            if event.key == K_w:
                folderPath = "/opt/crat/core/home/sounds/NOISE/" #playlist 2
                files = build_file_list()
                print(files)

            if event.key == K_ESCAPE:
                sys.exit()
                break



