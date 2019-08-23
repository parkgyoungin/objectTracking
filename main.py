import cv2
import numpy as np

class MultiTracker():
    # [method]
    # append_object prams = [name]
    # play
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        _, self.first_img = self.cap.read()
        self.object_rect = {}
        self.tracker = {}
        self.w=int(self.cap.get(3))
        self.h=int(self.cap.get(4))

    def resize(self, w,h):
        self.w = w
        self.h = h

    def append_object(self, name):
        img = cv2.resize(self.first_img, (self.w, self.h))
        cv2.namedWindow('select window')
        cv2.imshow('select window', img)

        self.object_rect[name] = (cv2.selectROI('select window', img, fromCenter=False, showCrosshair=True))
        self.tracker[name] = cv2.TrackerCSRT_create()
        self.tracker[name].init(img, self.object_rect[name])

        cv2.destroyWindow('select window')

    def play(self):
        while True:
            ret, img = self.cap.read()
            img = cv2.resize(img, (self.w, self.h))

            if not ret:
                exit()

            box = {}
            for name,tracker in self.tracker.items():
                _, box[name] = tracker.update(img)

            for name, rect in box.items():
                left, top, w, h = [int(v) for v in rect]
                cv2.rectangle(img, pt1=(left, top), pt2=(left + w, top + h), color=(255, 0, 0), thickness=1)
                cv2.putText(img, name, (left,top), cv2.FONT_HERSHEY_SIMPLEX,1, (255,0,0),2)

            cv2.imshow('img', img)
            if cv2.waitKey(40) is ord('q'):
                break

        cv2.destroyWindow('img')

video_path = './media/traffic.mp4'
multi_tracker = MultiTracker(video_path)
#multi_tracker.resize(640,360)
for i in range(1):
    multi_tracker.append_object(name="car_{}".format(i))

multi_tracker.play()

