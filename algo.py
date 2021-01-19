import cv2 as cv
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import numpy as np


class Algo:
    # start and end represent start and end time of sub-clip in seconds
    def __init__(self, url: str, start: int, end: int) -> None:
        self.__video = YouTube(url)

        # clears any existing mp4 files
        for fname in os.listdir('.'):
            if fname.endswith(".mp4"):
                os.remove(fname)

        if not self.__getVideoPath():
            self.__video.streams.get_by_itag(18).download()

        self.__vidFile = self.__getVideoPath()
        self.__shortenVideo(start, end)

    # shortens video file to a length of at most 10 seconds
    def __shortenVideo(self, start: int, end: int) -> None:

        if start < 0 or end > start + 10 or end > self.__video.length:
            raise ValueError
        else:
            ffmpeg_extract_subclip(self.__vidFile, start, end, targetname="video.mp4")
            os.remove(self.__vidFile)
            self.__vidFile = "video.mp4"

    # searches current directory for an mp4 file
    def __getVideoPath(self) -> str:
        for fname in os.listdir('.'):
            if fname.endswith(".mp4"):
                return fname
        return ""

    # gets the fps of the video sub-clip
    def __getFPS(self) -> int:  # maybe display this to the user
        cap = cv.VideoCapture(self.__vidFile)
        return round(cap.get(cv.CAP_PROP_FPS))

    # gets the total number of frames in the video sub-clip
    def __getFrames(self) -> int:   # maybe display this to the user
        cap = cv.VideoCapture(self.__vidFile)
        return int(cap.get(cv.CAP_PROP_FRAME_COUNT))

    # returns sum of the differences in each of the frames' rgb channels
    def __compareFrames(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        rgb1 = list(cv.mean(frame1))[0:3]
        rgb2 = list(cv.mean(frame2))[0:3]
        return abs(rgb1[0] - rgb2[0]) + abs(rgb1[1] - rgb2[1]) + abs(rgb1[2] - rgb2[2])

    # driver of the full video analysis
    def analyze(self) -> list:
        cap = cv.VideoCapture(self.__vidFile)
        frameHeap = []
        fps = self.__getFPS()
        flashesPerSecond = []   # list of numOfFlashes in each second of the video
        flashes = 0
        currentFrame = 0

        while True:
            if currentFrame % fps == 0:     # started a new second
                flashesPerSecond.append(flashes)
                flashes = 0

            ret, frame = cap.read()

            if len(frameHeap) < 2:
                frameHeap.append(frame)
            elif len(frameHeap) == 2:
                if self.__compareFrames(frameHeap[0], frameHeap[1]) > 200:
                    flashes += 1
                frameHeap.pop()
                frameHeap.append(frame)

            if frame is None:
                break

            cv.imshow('Frame', frame)

            cv.waitKey(1)
            currentFrame += 1

        cap.release()
        cv.destroyAllWindows()

        count = 0   # num of seconds with a high flash rate (above 5 flashes per seconds)
        for i in flashesPerSecond[1:]:
            if i >= 5:
                count += 1

        webOutput = [self.__getFrames(), fps, flashesPerSecond[1:]]
        if count >= 5:
            webOutput.append("High Risk")
        elif 5 > count > 1:
            webOutput.append("Medium Risk")
        else:
            webOutput.append("Low Risk")

        return webOutput

    def __del__(self):
        os.remove(self.__vidFile)
