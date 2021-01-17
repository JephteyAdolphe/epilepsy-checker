import cv2
from pytube import YouTube
import os
import matplotlib.pyplot as plt
import math
import datetime
import shutil


class Algo:
    def __init__(self, url: str) -> None:
        self.__video = YouTube(url)
        if self.__video.length <= 600:
            if not self.__getVideoPath():
                self.__vid = self.__video.streams.get_by_itag(18).download()
            self.__vidFile = self.__getVideoPath()
        else:
            print("Video is too long")

    def __getVideoPath(self) -> str:
        for fname in os.listdir('.'):
            if fname.endswith(".mp4"):
                return fname
        return None

    def __getFPS(self) -> int: # maybe display this to the user
        cap = cv2.VideoCapture(self.__vidFile)
        return math.floor(cap.get(cv2.CAP_PROP_FPS))

    def __getFrames(self) -> int: # maybe display this to the user
        cap = cv2.VideoCapture(self.__vidFile)
        return int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def analyze(self):
        fps = self.__getFPS()
        frames = self.__getFrames()
        flashes = 0

        for frame in range(frames):
            if frame % fps == 0:
                flashes = 0


    # have to figure out what a flash is in the video



test = Algo("https://www.youtube.com/watch?v=1EEakkh4ZG4")
