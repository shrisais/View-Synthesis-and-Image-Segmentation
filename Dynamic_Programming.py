import numpy as np
import cv2


left = cv2.imread('view1.png')
right= cv2.imread('view5.png')
left_img= cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
right_img= cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)


rows=left_img.shape[0]
N=left_img.shape[1]
M=right_img.shape[1]

Disp_left=np.zeros(left_img.shape,dtype=np.uint8)
Disp_right=np.zeros(right_img.shape,dtype=np.uint8)

OcclusionCost = 20 #(You can adjust this, depending on how much threshold you want to give for noise)

for r in range (0,rows):
    print (r)
    CostMatrix=np.zeros((N,M))
    DirectionMatrix = np.zeros((N,M))  
    
    for i in range(0,N):
        CostMatrix[i,0] = i*OcclusionCost
        
    for i in range(0,M):
        CostMatrix[0,i] = i*OcclusionCost

    
    for i in range(0,N):
        for j in range (0,M):
            min1=CostMatrix[i-1,j-1]+np.abs((int(left_img[r,i])-int(right_img[r,j])))
            min2=CostMatrix[i-1,j]+OcclusionCost
            min3=CostMatrix[i,j-1]+OcclusionCost
            cmin=np.min((min1,min2,min3))
            
            CostMatrix[i,j]=cmin
            if min1==cmin:
                DirectionMatrix[i,j]=1
            if min2==cmin:
                DirectionMatrix[i,j]=2
            if min3==cmin:
                DirectionMatrix[i,j]=3
                   
        p=N-1
        q=M-1
        
    while ((p!=0) and (q!=0)):
        val=DirectionMatrix[p,q]
        if val==1:
            Disp_left[r,p]=np.abs(p-q)
            Disp_right[r,q]=np.abs(p-q)
            p-=1
            q-=1
            
        elif val==2:
            p-=1
            
        elif val==3:
            q-=1
            
cv2.imwrite('Left.png',Disp_left)
cv2.imwrite('Right.png',Disp_right)