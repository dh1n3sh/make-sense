import csv 
import cv2 
import numpy as np 
import os 

destination = './output/'
if not os.path.exists(destination): 
    os.makedirs(destination) 
# if not os.path.exists ('./reference'): 
#     os.makedirs ('./reference') 

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

# print (imageBoxes, imageSize)

for key,value in imageBoxes.items() :

    dim = imageSize[key] 
    imh, imw = dim[1], dim[0]

    #Modify masks 
    # blank_image = np.zeros((imh, imw, 4)) #For each label 
    # blank_image[:, :] = (0, 100, 0, 0) 

    reference_image = np.zeros ((imh, imw, 3))  

    labelToIndex = { 
        "Answer number": 0, "Candidate details ":1, "Para":2, "Bullets":3, "Table":4, "Figure":5, "Mathematical":6, "None":7
    } 
    colourCombination = [
        (255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255), (128,128,128), (0,0,0)
    ] 

    #Answer number: Red  
    #Candidate details: Lime
    #Para: Blue
    #Bullets: Yellow 
    #Table: Cyan
    #Figures: Magenta
    #Mathematical: Gray
    #None: Black  

    for box in value:  
        
        label = box[0] 
        topLeftX,topLeftY = box[2],box[1]  
        len,bred = box[4],box[3] 

        # print (box) 
        # blank_image[topLeftX:topLeftX+len, topLeftY:topLeftY+bred] = (100, 0, 0, 0)
        # print (label) 

        x = colourCombination[labelToIndex[label]]
        #HOW is it BGR?  
        reference_image[topLeftX:topLeftX+len, topLeftY:topLeftY+bred] = (x[2], x[1], x[0]) #colourCombination[labelToIndex[label]] 

    cv2.imwrite(destination + key, reference_image)
    # cv2.imwrite(destination + key, blank_image) 