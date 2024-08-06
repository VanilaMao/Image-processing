# https://www.aranacorp.com/en/displaying-an-opencv-image-in-a-pyqt-interface/
# https://encord.com/blog/image-segmentation-for-computer-vision-best-practice-guide/
# https://www.youtube.com/watch?v=f6VgWTD_7kc
# https://answers.opencv.org/question/50025/what-exactly-is-a-blob-in-opencv/
# https://stackoverflow.com/questions/65169869/detecting-and-counting-blobs-connected-objects-with-opencv
# https://www.scaler.com/topics/blob-detection-opencv/
# https://www.scaler.com/topics/blob-detection-opencv/
# https://github.com/VanilaMao/LabDrivers/blob/master/LabImage/LabImage.cs
# https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html
# https://stackoverflow.com/questions/54316588/get-the-average-color-inside-a-contour-with-open-cv
import math
import sys
from typing import Union
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from cv2.typing import MatLike
from qtpy.QtGui import QPixmap, QImage
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QApplication,QMainWindow,QLabel
)
from models.location import *
from models.worm import *

class ImageProcessing:
    def __init__(self) -> None:
        pass

    @staticmethod
    def cv_to_qimage(cv_img: MatLike, format='uint16') -> QImage:
        qimage = None
        if format =='uint8' or format=="uint16":
            height, width = cv_img.shape
            img = ImageProcessing.convert_uint16_to_uint8(cv_img) if format == 'uint16' else cv_img
            qimage = QImage(
                img.data, width, height, width, QImage.Format.Format_Grayscale8
            )
        elif format == "bgr":
            height, width, ch = cv_img.shape
            qimage = QImage(
                cv_img.data, width, height, width*ch, QImage.Format.Format_BGR888
            )
        return qimage

    @staticmethod
    def load_file(name, format="uint16"):
        if format == "uint16":
            return cv.imread(name, cv.IMREAD_ANYCOLOR | cv.IMREAD_ANYDEPTH)
        return None
    
    @staticmethod
    def convert_uint16_to_uint8(cv_img): #norm = cv.normalize(gray, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv.CV_8U)
        height, width = cv_img.shape
        ratio = np.amax(cv_img) / 256 ;       
        img = (cv_img/ratio).astype('uint8')
        return img

    @staticmethod
    def convert_uint8_to_binary(cv_img, min, max):
        # thresh= cv.threshold(cv_img,min, max,cv.THRESH_BINARY)[1]
        thresh = cv.inRange(cv_img,min, max)
        # thresh = cv.bitwise_not(thresh)
        return thresh
    
    @staticmethod
    def multiply(left,right):
        return cv.multiply(left,right)

    @staticmethod
    def split_image(img):
        _, width = img.shape
        half = width//2
        return img[:,:half], img[:,half:]
    
    @staticmethod
    def combine_img_to_bgr(left, right):
        height, width = left.shape
        image = np.zeros((height, width, 3), np.uint8)
        image[:,:,2] = left
        image[:,:,1] = right
        return image
    
    # https://pyimagesearch.com/2021/02/03/opencv-image-translation/
    @staticmethod
    def shift_img(img, down=0, right=0): # right>0 move right, bottom>0 move doen
        m = np.float32([
                [1, 0, right],
                [0, 1, down]
            ])
        shifted = cv.warpAffine(img, m, (img.shape[1], img.shape[0]))
        return shifted


    @staticmethod
    def detect_blob(img,max_area,min_area, use_second = False): 
        contours,_ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        biggest_area = 0
        second_area =0 
        biggest_contour =None
        second_contour = None
        for contour in contours:
            area = cv.contourArea(contour)
            if area < min_area or area >max_area:
                continue
            print(f"area {area}")
            if area> biggest_area:
                second_area = biggest_area
                second_contour = biggest_contour
                biggest_area = area          
                biggest_contour = contour
            elif area>second_area:
                second_area = area
                second_contour = contour
        target_contour = second_contour if use_second else  biggest_contour
        if target_contour is not None:
            moment = cv.moments(target_contour)
            cx = int(moment['m10']/moment['m00'])
            cy = int(moment['m01']/moment['m00'])
            rect = cv.boundingRect(target_contour)
            return Point(cx,cy), Rect(rect[0], rect[1],rect[2],rect[3])
        else:
            return None,None
    
    @staticmethod
    def cal_ratios(left, right, binary, rect:Rect):
        mask= np.zeros(binary.shape, np.uint8)
        cv.rectangle(mask,(rect.x,rect.y),(rect.x+rect.width,rect.y+rect.height),1,-1)

        copy_binary = np.copy(binary)
        copy_binary[copy_binary>0]=1

        left_mean = cv.mean(left,mask=mask)[0]
        right_mean = cv.mean(right,mask=mask)[0]
        binary_mean = cv.mean(copy_binary,mask=mask)[0]

        if math.isclose(binary_mean, 0.0):
            binary_mean =1
        return left_mean/binary_mean, right_mean/binary_mean, binary_mean
    
    @staticmethod
    def read_carbin_file(file):
        total_frames = 0
        with open(file,"r") as file:
            index = 0
            data = None
            for line in file.readlines():
                if index ==0 :
                    np0 = np.fromstring(line, sep="|")
                    data = np.array(np0[1:])
                    total_frames = np0[0]
                else:
                    values = np.array(np.fromstring(line, sep="|"))
                    data = np.vstack((data,values))
                index+=1
        return total_frames, data
    
    @staticmethod
    def subtract(img, value):
        img[img<value]=value
        img-=value
    
def test_files():
    total, carbin_infos= ImageProcessing.read_carbin_file("C:\\Users\\work\\Downloads\\20230126 0.5mm 1mm-28\\20230126 0.5mm 1mm-28\\20230126 0.5mm 1mm-28.ftd")
    print(total)

def test_images():
    app = QApplication(sys.argv)
    img = ImageProcessing.load_file("lab/src/icons/0000.tif")
    left,right = ImageProcessing.split_image(img)
    left[left<100]=100
    left-=100
    right[right<100]=100
    right-=100

    left_unit8 = ImageProcessing.convert_uint16_to_uint8(left)
    right_unit8 = ImageProcessing.convert_uint16_to_uint8(right)
    print(np.max(left_unit8))
    shifted_right_unit8= ImageProcessing.shift_img(right_unit8,50,50)

    right_binary = cv.threshold(right_unit8,100, 255,cv.THRESH_BINARY)[1]
    left_binary = cv.threshold(left_unit8,0, 255,cv.THRESH_BINARY)[1]

    mutiply_binary = cv.multiply(right_binary,left_binary)


    contours,_ = cv.findContours(right_binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    result_bgr= cv.cvtColor(mutiply_binary,cv.COLOR_GRAY2RGB)

    bigest_contour = None
    biggest_area = 0
    biggest_rect =None
    for contour in contours:
        area = cv.contourArea(contour)
        if area < 10 or area >500:
            continue
        print(f"area {area}")
        moment = cv.moments(contour)
        cx = int(moment['m10']/moment['m00'])
        cy = int(moment['m01']/moment['m00'])
        rect = cv.boundingRect(contour)
        # cv.drawContours(result_bgr,[contour],0,(0,0,255),1)
        cv.rectangle(result_bgr,(rect[0],rect[1]),(rect[0]+rect[2],rect[1]+rect[3]),(0,0,255),2)
        print(area)
        if area> biggest_area:
            biggest_area= area
            bigest_contour = contour
            biggest_rect = rect


    cv.rectangle(result_bgr,(biggest_rect[0],biggest_rect[1]),(biggest_rect[0]+biggest_rect[2],biggest_rect[1]+biggest_rect[3]),(0,0,255),2)
    print(biggest_rect)

    # mask = np.zeros(right_unit8.shape, np.uint8)
    # cv.drawContours(mask, bigest_contour, 0, 1, -1)

    height,width = right.shape
    mask1= np.zeros((height,width,1), np.uint8)
    print(right.shape)
    cv.rectangle(mask1,(biggest_rect[0],biggest_rect[1]),(biggest_rect[0]+biggest_rect[2],biggest_rect[1]+biggest_rect[3]),1,-1)


    copy_binary = np.copy(mutiply_binary)
    copy_binary[copy_binary>0]=1

    
    
    
    mean = cv.mean(left,mask=mask1)

    mean1 = cv.mean(right,mask=mask1)

    mean3=cv.mean(copy_binary,mask=mask1)

    print(mean)
    print(mean1)
    print(mean3)
    # print(f"{mean3}|{np.max(mask1)}|{np.max(mask)}")

    cv.imshow("16 binary", left_unit8)
    cv.waitKey(10000)
    cv.destroyAllWindows()
    

if __name__ == "__main__":
    # test_files()

    test_images()



    # app = QApplication(sys.argv)
    # img = ImageProcessing.load_file("lab/src/icons/0000.tif")
    # left,right = ImageProcessing.split_image(img)

    # right_uint8 = ImageProcessing.convert_uint16_to_uint8(right)

    # qimage = ImageProcessing.cv_to_qimage(right,'uint16')

    # window = QMainWindow()
    # label = QLabel()
    # label.setPixmap(QPixmap.fromImage(qimage))
    # window.setCentralWidget(label)
    # window.resize(600,400)
    # window.show()
    # sys.exit(app.exec_())
