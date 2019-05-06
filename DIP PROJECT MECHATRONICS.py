#!/usr/bin/env python
# coding: utf-8

# In[27]:


import cv2
import numpy as np
import matplotlib.pyplot as plt
from imutils import contours 
import imutils

#LOAD IMAGE AND APPLY FILTERS TO IT

image = cv2.imread ('test_02.png' , cv2.IMREAD_GRAYSCALE) #LOADING IMAGE FROM PATH

blurring = cv2.GaussianBlur(image, (3, 3), 0) #FILTERING NOISE 

edged = cv2.Canny(blurring, 75, 200) # EDGING CIRCLES AND FRAME

thresh = cv2.threshold(edged, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1] #BINARY INVERSION

#ANSWER KEY

ANSWER = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

#DETECT CIRCLES AND CONTOURS  

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #CONTOUR FINDING
cnts = imutils.grab_contours(cnts)

#LOOP OVER CONTOURS TO FIND NO. OF QUESTIONS AND TYPE IT INSIDE IMAGE

questions = 0

for i in cnts:
    area = cv2.contourArea(i) # to get contours areas
    if area < 150  :
        questions = questions + 1

#to put no.of questions on image

cv2.putText(image, "No.Of Questions ={:.0f}".format(questions), (10, 12),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
        
#SORT OVER QUESTIONS TO GET CORRECT ANSWER

ques = contours.sort_contours(cnts,method="top-to-bottom")[0] #SORTING CONTOURS FROM TOP TO BOTTOM
correct = 0

for (j, s) in enumerate(np.arange(0, len(ques), 6)): #LOOP OVER QUESTION THROUGH BATCH OF 5
    Cnts = contours.sort_contours(ques[s:s + 5])[0]
    chosen = None
    
    
    for (q, b) in enumerate(Cnts):
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv2.drawContours(mask, [b], -1, 255, -1)
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        total = cv2.countNonZero(mask)       
        if chosen is None or total > chosen[0]:
            chosen = (total, q)
            
            
    color = (255, 0, 255)
    
    k = ANSWER[j]
    
    if k == chosen[1]:
        color = (0, 255, 0)
        correct += 1
        
        
    cv2.drawContours(image, [Cnts[k]], -1, color, 3) #TO SHOW BUBBLED ANSWER AND CORRECT IN BLACK CIRCLE

MARKS =  (correct / 5.0) * 100

#TO PUT MARKS ON IMAGE RESULT

cv2.putText(image, ",MARKS={:.2f}%".format(MARKS), (160, 12),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

#SHOW RESULTS 

cv2.imshow("Original", image)
cv2.waitKey(0)


# In[ ]:




