import tensorflow as tf
import numpy as np
import os
import urllib
import tarfile
import sys
sys.path.insert(0, 'utils')
import signal
import functools
from PySide import QtGui, QtCore
import cv2
import label_map_util
from object_detector import ObjectDetector

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.central_widget = QtGui.QWidget(self)
        self.central_layout = QtGui.QHBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)
        self.image_widget = QtGui.QLabel(self)
        self.central_layout.addWidget(self.image_widget)

        self.camera()
        
    def imageTo(self, image, obj):
        pixmap = QtGui.QPixmap.fromImage(image)
        if obj != []:
            p = QtGui.QPainter()
            p.begin(pixmap)
            for item in obj:
                p.setPen(QtCore.Qt.red)
                print item
                x1, y1, x2, y2 = item[1:]
                w = x2-x1
                h = y2-y1
                p.drawRect(x1, y1, w, h)
            p.end ()
            print
                                    
        self.image_widget.setPixmap(pixmap);
    
    def camera(self):
        self.camera = CameraReader()
        self.camera.start()
        self.camera.signal.connect(self.imageTo)

class CameraReader(QtCore.QThread):
    signal = QtCore.Signal(QtGui.QImage, object)
    def __init__(self):
        super(CameraReader, self).__init__()
        self.cam = cv2.VideoCapture(0)
        self.width = long(self.cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
        self.height = long(self.cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
        self.objdet = ObjectDetector()

    def run(self):
        while True:
            ret, img = self.cam.read()
            expand = np.expand_dims(img, axis=0)
            result = self.objdet.detect(expand)
            image = QtGui.QImage(img.data, self.width, self.height, QtGui.QImage.Format_RGB888).rgbSwapped()
            boxes = []
            for i in range(result['num_detections']):
                if result['detection_scores'][i] > 0.5:
                    class_ = result['detection_classes'][i]
                    box = result['detection_boxes'][i]
                    y1, x1 = box[0] * self.width, box[1] * self.height
                    y2, x2 = box[2] * self.width, box[3] * self.height
                    boxes.append((class_, x1, y1, x2, y2))
                    
            self.signal.emit(image, boxes)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    app.exec_()
