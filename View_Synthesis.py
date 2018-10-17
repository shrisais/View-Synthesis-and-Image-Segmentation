import numpy as np
import cv2

left = cv2.imread('view1.png');
right = cv2.imread('view5.png');
left_disp = cv2.imread('disp1.png',0);
right_disp = cv2.imread('disp5.png',0);

rows= left.shape[0]
cols= right.shape[1]

image=np.zeros([rows,cols,3],dtype = np.uint8)

#From view1 and disp1
for i in range (0,rows):
    for j in range (0,cols):
        h = j-int(left_disp[i][j]/2)
        if h >= 0:
            image[i][h]=left[i][j]
        else:
            continue
                                 
#From view5 and disp5
for i in range (0,rows):
    for j in range (0,cols):
        h=j+int(right_disp[i][j]/2)
        if h < cols:
            if (image[i][h].all()==0):
                image[i][h]=right[i][j]
        else:
            continue
                
cv2.imwrite("VS.png",image)                         
