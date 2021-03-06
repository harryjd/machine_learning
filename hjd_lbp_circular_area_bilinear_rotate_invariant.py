# -*- coding: utf-8 -*-
import cv2
import numpy as np
import math
##############################################################
#圆形LBP算法.
#R:半径；P:参考点的数量
#按面积进行双线性插值估算
def LBP_Circle_AreaBiLinear(image, R, P):
    H, W = image.shape[:2]      #获得图像长宽
    #创建0数组,并且类型一定的是uint8,无符号8位,opencv图片的存储格式.
    res = np.zeros(shape=(H, W), dtype="uint8")

    for row in range(0, H ):     #row对应是纵坐标
        for col in range(0, W):  #col对应是横坐标
            pixels = []  #用于存储邻域像素的灰度值
            for seq in range(0, P):  # 按顺序计算参考点的坐标
                threta = 2 * math.pi * seq / P
                xi = col + R * math.cos(threta)
                yi = row - R * math.sin(threta)
                xii = int(xi)
                yii = int(yi)
                #修正计算的误差
                if(abs(xi-xii)<0.01):
                    xi = xii
                if(abs(yi-yii)<0.01):
                    yi = yii
                
                if ((xi<0)or(yi<0)or(xi>W-1)or(yi>H-1)):
                    pixels.append(0)
                    continue
                if(xii==xi): #xi是整数
                    if(yii==yi): #yi也是整数
                        #说明<yi, xi>是实际的一个像素，不用计算插值
                        pixels.append(image[yii, xii])
                    else: #xi是整数，yi不是，在y方向上插值
                        yiii = math.ceil(yi)
                        W1 = np.array([yiii-yi, yi - yii]) #(yiii - yii)必然是1，不用除1
                        Points = np.array([image[yii, xii],\
                                           image[yiii, xii]])
                        singlelinear = np.matmul(W1, Points) #计算出Y方向的线性插值
                        pixels.append(singlelinear)
                elif(yii==yi): #xi不是整数, yi是整数,在横轴方向上线性插值
                    xiii = math.ceil(xi)
                    W1 = np.array([xiii-xi, xi - xii]) #(xiii - xii)必然是1，不用除1
                    Points = np.array([image[yii, xii],\
                                       image[yiii, xii]])
                    singlelinear = np.matmul(W1, Points) #计算出Y方向的线性插值
                    pixels.append(singlelinear)
                else:
                    #xi, yi都不是整数，要执行双线性插值
                    yiii = math.ceil(yi)
                    xiii = math.ceil(xi)
                    W1 = np.array([[1-(yi-yii)*(xi-xii), 1-(yi-yii)*(xiii-xi)],\
                                   [1-(yiii-yi)*(xi-xii), 1-(yiii-yi)*(xiii-xi)]], dtype="float")
                    W1 = W1 / 3 #把区域分成了4份，所以要除以3，确保灰度值不溢出
                    Q = np.array([[image[yii,xii], image[yii,xiii]],\
                                  [image[yiii,xii], image[yiii,xiii]]], dtype="float")
                    binlinear = (Q*W1).sum()
                    pixels.append(binlinear)
            strCircularLBP = "" #拼接二进制字符串
            for m in range(0, P):
                if pixels[m] > image[row, col]: #像素比较
                    strCircularLBP = strCircularLBP + '1'
                else:
                    strCircularLBP = strCircularLBP + '0'
            #print int(temp, 2)
            nCircularLBP = Rotate_LBP_Min(strCircularLBP)
            res[row, col] = nCircularLBP   #写入结果中
    return res

##############################################################
#圆形LBP算法.
#R:半径；P:参考点的数量
#按双线性插值估算
def LBP_Circle_BiLinear(image, R, P):
    H, W = image.shape[:2]      #获得图像长宽
    #创建0数组,并且类型一定的是uint8,无符号8位,opencv图片的存储格式.
    res = np.zeros(shape=(H, W), dtype="uint8")

    for row in range(0, H ):     #row对应是纵坐标
        for col in range(0, W):  #col对应是横坐标
            pixels = []  #用于存储邻域像素的灰度值
            for seq in range(0, P):  # 按顺序计算参考点的坐标
                threta = 2 * math.pi * seq / P
                xi = col + R * math.cos(threta)
                yi = row - R * math.sin(threta)
                xii = int(xi)
                yii = int(yi)
                #修正计算的误差
                if(abs(xi-xii)<0.01):
                    xi = xii
                if(abs(yi-yii)<0.01):
                    yi = yii
                
                if ((xi<0)or(yi<0)or(xi>W-1)or(yi>H-1)):
                    pixels.append(0)
                    continue
                if(xii==xi): #xi是整数
                    if(yii==yi): #yi也是整数
                        #说明<yi, xi>是实际的一个像素，不用计算插值
                        pixels.append(image[yii, xii])
                    else: #xi是整数，yi不是，在y方向上插值
                        yiii = math.ceil(yi)
                        W1 = np.array([yiii-yi, yi - yii], dtype="float") #(yiii - yii)必然是1，不用除1
                        Points = np.array([image[yii, xii],\
                                           image[yiii, xii]])
                        singlelinear = np.matmul(W1, Points) #计算出Y方向的线性插值
                        pixels.append(singlelinear)
                elif(yii==yi): #xi不是整数, yi是整数,在横轴方向上线性插值
                    xiii = math.ceil(xi)
                    W1 = np.array([xiii-xi, xi - xii], dtype="float") #(xiii - xii)必然是1，不用除1
                    Points = np.array([image[yii, xii],\
                                       image[yiii, xii]])
                    singlelinear = np.matmul(W1, Points) #计算出Y方向的线性插值
                    pixels.append(singlelinear)
                else:
                    #xi, yi都不是整数，要执行双线性插值
                    yiii = math.ceil(yi)
                    xiii = math.ceil(xi)
                    W1 = np.array([xiii - xi, xi - xii], dtype="float")
                    Q = np.array([[image[yii,xii], image[yiii,xii]],\
                                  [image[yii,xiii], image[yiii,xiii]]])
                    W2 = np.array([[yiii-yi], [yi - yii]], dtype="float")
                    binlinear = np.matmul(np.matmul(W1, Q), W2)
                    pixels.append(binlinear)
            strCircularLBP = "" #拼接二进制字符串
            for m in range(0, P):
                if pixels[m] > image[row, col]: #像素比较
                    strCircularLBP = strCircularLBP + '1'
                else:
                    strCircularLBP = strCircularLBP + '0'
            #print int(temp, 2)
            nCircularLBP = Rotate_LBP_Min(strCircularLBP)
            res[row, col] = nCircularLBP   #写入结果中
    return res

##############################################################
#最朴素的LBP算法
def LBP_Basic(image):
    H, W = image.shape[:2]      #获得图像长宽
    xx = [-1,  0,  1, 1, 1, 0, -1, -1]
    yy = [-1, -1, -1, 0, 1, 1,  1,  0]    #xx, yy 主要作用对应顺时针旋转时,相对中点的相对值.
    
    #创建0数组,显而易见维度原始图像的长宽分别减去2，并且类型一定的是uint8,无符号8位,opencv图片的存储格式.
    res = np.zeros(shape=(H-2, W-2), dtype="uint8")
    
    for row in range(1, H - 1):
        for col in range(1, W - 1):
            temp = "" #拼接二进制字符串
            for m in range(0, 8):
                Xtemp = xx[m] + col   
                Ytemp = yy[m] + row    #分别获得对应坐标点
                #print("Ytemp, Xtemp", Ytemp, Xtemp)
                if image[Ytemp, Xtemp] > image[row, col]: #像素比较
                    temp = temp + '1'
                else:
                    temp = temp + '0'
            #print int(temp, 2)
            res[row - 1][col - 1] =int(temp, 2)   #写入结果中
            #print("res[i][j]: i, j=", row - 1, col - 1)
            #print("res[row - 1][col - 1]", res[row - 1][col - 1])
    # print("res.shape=", res.shape[:2])
    return res
