import cv2 as cv
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import random
import string
import numpy as np

'''
Playground file is used strictly for testing and demonstration purposes.
'''


class Algo:
    # start and end represent start and end time of sub-clip in seconds
    def __init__(self, url: str, start: int, end: int) -> None:
        if url == "https://www.youtube.com/watch?v=Qohb8la00XU":
            self.__vidFile = "lowrisk.mp4"
        elif url == "https://www.youtube.com/watch?v=AjbrmfjJRk0":
            self.__vidFile = "highrisk.mp4"
        else:
            raise NameError

    # shortens video file to a length of at most 10 seconds
    def __shortenVideo(self, start: int, end: int) -> None:

        if start < 0 or end > start + 10 or end > self.__video.length:
            raise ValueError
        else:
            newFilename = self.__generateFileName()
            ffmpeg_extract_subclip(self.__vidFile, start, end, targetname=newFilename)
            os.remove(self.__vidFile)
            self.__vidFile = newFilename

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
    def analyzeWithout(self) -> list:
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
                if self.__compareFrames(frameHeap[0], frameHeap[1]) > 600:
                    flashes += 1
                frameHeap.pop()
                frameHeap.append(frame)

            if frame is None:
                break

            currentFrame += 1
            cv.waitKey(1)

        cap.release()

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

    def __clearVideos(self) -> None:
        for fname in os.listdir('.'):
            if fname == "lowrisk.mp4":
                continue
            elif fname == "highrisk.mp4":
                continue
            elif fname.endswith(".mp4"):
                os.remove(fname)

    def __generateFileName(self) -> str:
        file = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        return file + ".mp4"

    # def __del__(self) -> None:
    #     self.__clearVideos()

    # driver of the full video analysis
    def analyzeWith(self) -> list:
        cap = cv.VideoCapture(self.__vidFile)
        frameHeap = []
        fps = self.__getFPS()
        flashesPerSecond = []  # list of numOfFlashes in each second of the video
        flashes = 0
        currentFrame = 0

        while True:
            if currentFrame % fps == 0:  # started a new second
                flashesPerSecond.append(flashes)
                flashes = 0

            ret, frame = cap.read()
            cv.imshow('Frame', frame)

            if len(frameHeap) < 2:
                frameHeap.append(frame)
            elif len(frameHeap) == 2:
                if self.__compareFrames(frameHeap[0], frameHeap[1]) > 600:
                    flashes += 1
                frameHeap.pop()
                frameHeap.append(frame)

            if frame is None:
                break

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

            currentFrame += 1

        cap.release()
        cv.destroyAllWindows()

        count = 0  # num of seconds with a high flash rate (above 5 flashes per seconds)
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


# lowrisk = Algo("https://www.youtube.com/watch?v=Qohb8la00XU", 0, 10)
# print(lowrisk.analyzeWithout())

# highrisk = Algo("https://www.youtube.com/watch?v=AjbrmfjJRk0", 0, 10)
# print(highrisk.analyzeWithout())

# lowurl = "https://www.youtube.com/watch?v=Qohb8la00XU"
# highurl = "https://www.youtube.com/watch?v=AjbrmfjJRk0"

# vid = YouTube(lowurl)
# vid = YouTube(highurl)
# vid.streams.get_by_itag(18).download()

# ffmpeg_extract_subclip(vid.title + ".mp4", 0, 10, targetname="lowrisk.mp4")
# ffmpeg_extract_subclip(vid.title + ".mp4", 0, 10, targetname="highrisk.mp4")
