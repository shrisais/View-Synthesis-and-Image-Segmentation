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

#For 9x9 - left image 
for i in range(4,rows-4):
    for j in range(4,cols-4):
        block_l=left[i-4:i+5,j-4:j+5]             
        bestdist=65535
        best=-1
        
        for k in range(j-73,j):
            if(k<4):
                k=4
            block_r=right[i-4:i+5,k-4:k+5]
            dist=np.sum(np.square(block_l-block_r))
            if (dist<bestdist):
                bestdist=dist
                best=k
            
        dleft[i][j] = j-best;
      
    
dleft_norm = cv2.normalize(dleft,  dleft_norm, 0, 255, cv2.NORM_MINMAX)
cv2.imwrite('Left_9x9.png',dleft_norm)
mse_left = np.mean((disp_left-dleft)**2)
print(mse_left)


#For 9x9 - right image 
for i in range(4,rows-4):
    for j in range(4,cols-4):
        block_r=right[i-4:i+5,j-4:j+5]             
        bestdist=65535
        best=-1
        
        for k in range(j+72,j,-1):
            if(k>cols-5):
                k=cols-5
            block_l=left[i-4:i+5,k-4:k+5]
            dist=np.sum(np.square(block_r-block_l))
            if (dist<bestdist):
                bestdist=dist
                best=k
            
        dright[i][j] = best-j;
      
    
dright_norm = cv2.normalize(dright,  dright_norm, 0, 255, cv2.NORM_MINMAX)
cv2.imwrite('Right_9x9.png',dright_norm)
mse_right = np.mean((disp_right-dright)**2)
print(mse_right)






