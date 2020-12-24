import csv 
import cv2 
import numpy as np 
import os 
import glob 

destination = './output/'

imageBoxes = dict()
imageSize = dict()  

csvName = input() 
with open(csvName) as csv_file: 

    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader: 

        name = row[5] 
        imageLen,imageB = int(row[6]),int(row[7])  
        
        label = row[0] 
        topLeftX,topLeftY = int(row[1]),int(row[2]) 
        boxLen,boxB = int(row[3]),int(row[4]) 

        if name not in imageBoxes:
            imageBoxes[name] = list() 
            imageSize[name] = [imageLen, imageB] 
        
        imageBoxes[name].append ([label, topLeftX, topLeftY, boxLen, boxB]) 

# Question id: 0
# Answer: 1  
# Bullets: 2  
# None: 3 

print (imageBoxes, imageSize)
for key,value in imageBoxes.items() :

    dim = imageSize[key] 
    imh, imw = dim[0], dim[1]

    test_image = np.zeros((imh, imw, 3)) 
    test_image[138:200, 183:250] = (255, 0, 0) 
    cv2.imwrite (destination + "ground.png", test_image)  

    #Modify masks 
    blank_image = np.zeros((imh, imw, 4)) #For each label 
    blank_image[:, :] = (0, 255, 0, 0) 

    reference_image = np.zeros ((imh, imw, 3))  
    reference_image[:, :] = (255, 255, 0)   

    for box in value:  
        
        label = box[0] 
        topLeftX,topLeftY = box[1],box[2] 
        len,bred = box[3],box[4] 

        if (label == "question identifier"): 
            blank_image[topLeftX:topLeftX+len, topLeftY:topLeftY+bred] = (255, 0, 0, 0)
            reference_image[topLeftX:topLeftX+len, topLeftY:topLeftY+bred] = (255, 0, 0)  #RED

        elif (label == "answer"):  
            blank_image[topLeftX:topLeftX+len, topLeftY:topLeftY+bred] = (0, 255, 0, 0)
            reference_image[topLeftX:topLeftX+len, topLeftY:topLeftY+bred] = (0, 255, 0) 
 
        elif (label == "bullet"): 
            reference_image[topLeftX:topLeftX+len, topLeftY:topLeftY+bred] = (0, 0, 255) #BLUE 
            blank_image[topLeftX:topLeftX+len, topLeftY:topLeftY+bred] = (0, 0, 255, 0)

        else:
            blank_image[topLeftX:topLeftX+len, topLeftY:topLeftY+bred] = (0, 0, 0, 255)  
            reference_image[topLeftX:topLeftX+len, topLeftY:topLeftY+bred] = (0, 0, 0) #BLACK
    
    cv2.imwrite(destination + key, reference_image)
    # cv2.imshow('Color image', reference_image)
    # cv2.imshow('Color image', b)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()