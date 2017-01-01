import cv2
import numpy as np

import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters

img=cv2.imread('img.png')
imgShow=img.copy()

cv2.putText(imgShow, "Please select object to detect", (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2)

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
currPoint=(0,0)
cropping = False
finished=False
 
def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping,currPoint,finished
 
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
 
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False
 
        # draw a rectangle around the region of interest
        cv2.rectangle(imgShow, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", imgShow)
        finished=True
        
    elif event == cv2. EVENT_MOUSEMOVE:
        currPoint = (x, y)


cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)


# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow("image", imgShow)
    key = cv2.waitKey(1) & 0xFF
    
    if cropping==True:
        imgShow=img.copy()
        cv2.rectangle(imgShow, refPt[0],currPoint, (0, 255, 0), 2)
        
    # if selection was made, break the loop
    elif finished==True:
        break

#template matching
imgShow=img.copy()
template = img[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]

w = template.shape[0]
h = template.shape[1]
res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)

#find local maxima
neighborhood_size = 20
threshold = 0.6
data_max = filters.maximum_filter(res, neighborhood_size)
maxima = (res == data_max)
data_min = filters.minimum_filter(res, neighborhood_size)
diff = ((data_max - data_min) > threshold)
maxima[diff == 0] = 0

labeled, numObjects = ndimage.label(maxima)
slices = ndimage.find_objects(labeled)
x, y = [], []
for dy,dx in slices:
    x_center = (dx.start + dx.stop - 1)/2
    x.append(x_center)
    y_center = (dy.start + dy.stop - 1)/2    
    y.append(y_center)

#print all objects that were found
for i in range(len(x)):
    cv2.rectangle(imgShow, (x[i],y[i]), (x[i] + w, y[i] + h), (0,0,255), 1)

cv2.putText(imgShow, "There are "+str(numObjects)+" Objects", (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2)
#cv2.imshow("ROI", template)
cv2.imshow("image", imgShow)
cv2.waitKey(0)

cv2.destroyAllWindows()
