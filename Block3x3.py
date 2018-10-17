import numpy as np
import cv2


left_img = cv2.imread('view1.png',0);
right_img = cv2.imread('view5.png',0);
left = cv2.copyMakeBorder(left_img, 1, 1, 1, 1,cv2.BORDER_REFLECT)
right = cv2.copyMakeBorder(right_img, 1, 1, 1, 1,cv2.BORDER_REFLECT)

disp_left_img=cv2.imread('disp1.png',0);
disp_right_img=cv2.imread('disp5.png',0);
disp_left=cv2.copyMakeBorder(disp_left_img, 1, 1, 1, 1,cv2.BORDER_REFLECT)
disp_right=cv2.copyMakeBorder(disp_right_img, 1, 1, 1, 1,cv2.BORDER_REFLECT)

rows=left.shape[0]
cols=left.shape[1]

dleft=np.zeros((rows,cols))
dleft_norm=np.zeros((rows,cols))
dright=np.zeros((rows,cols))
dright_norm=np.zeros((rows,cols))

#For 3x3 - left image 
for i in range(1,rows-1):
    for j in range(1,cols-1):
        block_l=left[i-1:i+2,j-1:j+2]             
        bestdist=65535
        best=-1
        
        for k in range(j-73,j):
            if(k<1):
                k=1
            block_r=right[i-1:i+2,k-1:k+2]
            dist=np.sum(np.square(block_l-block_r))
            if (dist<bestdist):
                bestdist=dist
                best=k
            
        dleft[i][j] = j-best;

        
dleft_norm = cv2.normalize(dleft,  dleft_norm, 0, 255, cv2.NORM_MINMAX)
cv2.imwrite('Left_3x3.png',dleft_norm)

mse_left = np.mean((disp_left-dleft)**2)
print(mse_left)



#For 3x3 - right image 
for i in range(1,rows-1):
    for j in range(1,cols-1):
        block_r=right[i-1:i+2,j-1:j+2]             
        bestdist=65535
        best=-1
        
        for k in range(j+73,j,-1):
            if(k>cols-2):
                k=cols-2
            block_l=left[i-1:i+2,k-1:k+2]
            dist=np.sum(np.square(block_r-block_l))
            if (dist<bestdist):
                bestdist=dist
                best=k
            
        dright[i][j] = best-j;
      
    
dright_norm = cv2.normalize(dright,  dright_norm, 0, 255, cv2.NORM_MINMAX)
cv2.imwrite('Right_3x3.png',dright_norm)
mse_right = np.mean((disp_right-dright)**2)
print(mse_right)


#Left - Consistency
cleft=np.zeros((rows,cols))
for i in range (0,rows):
    for j in range (0, cols):
        l=int(dleft[i,j])
        if j-l>cols:
            r=dright[i,j]
        else:
            r=dright[i,j-l]
            
        if(l==r):
            cleft[i,j]=l
        else:
            cleft[i,j]=0

cleft = cv2.normalize(cleft,  cleft, 0, 255, cv2.NORM_MINMAX)
cv2.imwrite('CLeft.png',cleft)

#Right - Consistency
cright=np.zeros((rows,cols))
for i in range (0,rows):
    for j in range (0, cols):
        r=int(dright[i,j])
        if j+r>cols:
            l=dleft[i,j]
        else:
            l=dleft[i,j+r]
                
        if(l==r):
            cright[i,j]=r
        else:
            cright[i,j]=0

cright = cv2.normalize(cright,  cright, 0, 255, cv2.NORM_MINMAX)
cv2.imwrite('CRight.png',cright)
