import cv2
from pytube import YouTube
import os
import matplotlib.pyplot as plt
import math
import datetime
import shutil


class Algo:
    def __init__(self, url):
        self.__video = YouTube(url)
        self.__vid = self.__video.streams.get_by_itag(18).download()


# test = Algo("https://www.youtube.com/watch?v=1EEakkh4ZG4")
yt = YouTube("https://www.youtube.com/watch?v=1EEakkh4ZG4")
print(yt.title)