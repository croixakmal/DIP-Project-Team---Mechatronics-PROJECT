import cv2
import numpy as np
import matplotlib.pyplot as plt
from imutils import contours
import imutils
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog

# LOAD IMAGE AND APPLY FILTERS TO IT

window = Tk()
Topframe = Frame (window)
Topframe.pack()
def path():
        global path,image,blurring,edged,thresh
        path = tkinter.filedialog.askopenfile()
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # LOADING IMAGE FROM PATH
        blurring = cv2.GaussianBlur(image, (3, 3), 0)  # FILTERING NOISE
        edged = cv2.Canny(blurring, 75, 200)  # EDGING CIRCLES AND FRAME
        thresh = cv2.threshold(edged, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        photo = PhotoImage(image)
        label = Label(window, img=photo)
        label.pack()

button1 = Button(Topframe, text='Scan your answer sheet ', fg="red", command=path)
button1.pack(side=LEFT)
window.mainloop()
# ANSWER KEY

ANSWER = {0: 1, 1: 0, 2: 0, 3: 0, 4: 0}

# DETECT CIRCLES AND CONTOURS

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# LOOP OVER CONTOURS TO FIND NO. OF QUESTIONS AND TYPE IT INSIDE IMAGE

questions = 0

for i in cnts:
    area = cv2.contourArea(i)
    if area < 150:
        questions = questions + 1
print(questions)
cv2.putText(image, "No.Of Questions ={:.0f}".format(questions), (10, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

# SORT OVER QUESTIONS TO GET CORRECT ANSWER

ques = contours.sort_contours(cnts, method="top-to-bottom")[0]
correct = 0

for (j, s) in enumerate(np.arange(0, len(ques), 6)):
    Cnts = contours.sort_contours(ques[s:s + 5])[0]
    CHOSEN = None

    for (q, b) in enumerate(Cnts):
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv2.drawContours(mask, [b], -1, 255, -1)
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        total = cv2.countNonZero(mask)
        if CHOSEN is None or total > CHOSEN[0]:
            CHOSEN = (total, q)

    color = (255, 0, 255)

    k = ANSWER[j]

    if k == CHOSEN[1]:
        color = (0, 255, 0)
        correct += 1

    cv2.drawContours(image, [Cnts[k]], -1, color, 3)
def result():
        MARKS = (correct / 5.0) * 100

window1 = Tk()
tkinter.messagebox.showinfo('Reults' ,text = 'your result', command= result)
window1.mainloop()

cv2.putText(image, ",MARKS={:.2f}%".format(MARKS), (160, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

# SHOW RESULTS

cv2.imshow("Original", image)
cv2.waitKey(0)