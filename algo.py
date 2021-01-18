import cv2 as cv
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import matplotlib.pyplot as plt
import time
from PIL import Image, ImageCms
import numpy as np
import math


class Algo:
    def __init__(self, url: str, start: int, end: int) -> None:
        self.__video = YouTube(url)
        # if self.__video.length <= 600:
        if not self.__getVideoPath():
            self.__video.streams.get_by_itag(160).download()
        self.__vidFile = self.__getVideoPath()

        self.__shortenVideo(start, end)
        print(self.__video.streams.filter(file_extension='mp4'))

        print(self.__getFPS())
        print(self.__getFrames())

    # shortens video file to a length of at most 10 seconds
    def __shortenVideo(self, start, end) -> None:

        if start < 0 or end > start + 10 or end > self.__video.length:
            raise ValueError
        else:
            ffmpeg_extract_subclip(self.__vidFile, start, end, targetname="video.mp4")
            os.remove(self.__vidFile)
            self.__vidFile = "video.mp4"

    def __getVideoPath(self) -> str:
        for fname in os.listdir('.'):
            if fname.endswith(".mp4"):
                return fname
        return ""

    def __getFPS(self) -> int:  # maybe display this to the user
        cap = cv.VideoCapture(self.__vidFile)
        return math.floor(cap.get(cv.CAP_PROP_FPS))

    def __getFrames(self) -> int:   # maybe display this to the user
        cap = cv.VideoCapture(self.__vidFile)
        return int(cap.get(cv.CAP_PROP_FRAME_COUNT))

    def analyze(self) -> None:
        fps = self.__getFPS()
        frames = self.__getFrames()
        flashes = 0

        for frame in range(frames):
            if frame % fps == 0:
                flashes = 0
            flashes += 1

    def __compareFrames(self, frame1: np.ndarray, frame2: np.ndarray, frameHeap: list) -> None:
        # srgb = ImageCms.createProfile("sRGB")
        # lab = ImageCms.createProfile("LAB")
        # rgb2lab = ImageCms.buildTransformFromOpenProfiles(srgb, lab, "RGB", "LAB")
        print(cv.mean(frame1))
        print(cv.mean(frame2))
        # frame1Lab = ImageCms.applyTransform(Image.fromarray(frame1), rgb2lab)
        # frame2Lab = ImageCms.applyTransform(Image.fromarray(frame2), rgb2lab)

    def showFrames(self) -> None:
        cap = cv.VideoCapture(self.__vidFile)
        frameHeap = []
        fps = self.__getFPS()
        totalFrames = self.__getFrames()
        flashes = 0
        currentFrame = 0

        # backSub = cv.createBackgroundSubtractorKNN()

        while True:
            if currentFrame % fps == 0:
                flashes = 0
            ret, frame = cap.read()

            if len(frameHeap) < 2:
                frameHeap.append(frame)
            elif len(frameHeap) == 2:
                self.__compareFrames(frameHeap[0], frameHeap[1], frameHeap)
                frameHeap.pop()
                frameHeap.append(frame)

            # frame is of type numpy.ndarray (3D)

            if frame is None:
                break

            # 172,800 pixels per frame
            # print(cv)

            cv.imshow('Frame', frame)
            keyboard = cv.waitKey(0)
            if keyboard == 'q' or keyboard == 27:
                break
            currentFrame += 1

        cap.release()
        cv.destroyAllWindows()

    def __del__(self):
        os.remove(self.__vidFile)

    # have to figure out what a flash is in the video


test = Algo("https://www.youtube.com/watch?v=AjbrmfjJRk0", 0, 10)
test.showFrames()
