import numpy as np
import cv2


img = cv2.imread('Butterfly.jpg')
rows = img.shape[0]
cols = img.shape[1]
#print(img.shape[2])
total_pixels = rows*cols
FV = np.zeros((total_pixels,5))
image = np.zeros((rows,cols,3),dtype=np.uint8)
size=0
h=200
iters=20
res=False

for i in range(0,rows):
    for j in range(0,cols):  
        FV[size,0],FV[size,1],FV[size,2]=img[i,j,0],img[i,j,1],img[i,j,2]
        FV[size,3],FV[size,4]=i,j
        size=size+1
        

import random
while(size>0):
    i = random.randint(0,size-1)    
    if(res==False):
        r,g,b,x,y = FV[i]
    cluster=[]
    dist=0
    for p in range(0,size):
        dist=np.sqrt((r-FV[p,0])**2+(g-FV[p,1])**2+(b-FV[p,2])**2+(x-FV[p,3])**2+(y-FV[p,4])**2)
        if dist<h:
            cluster.append(p)
              
    cluster_size=len(cluster) 
    
    if(cluster_size>0):
        mean_r=mean_g=mean_b=mean_x=mean_y=0
        for q in range (0,cluster_size):
            a=cluster[q]
            mean_r += FV[a][0]
            mean_g += FV[a][1]
            mean_b += FV[a][2]
            mean_x += FV[a][3]
            mean_y += FV[a][4] 
            
        mean_r/=cluster_size
        mean_g/=cluster_size
        mean_b/=cluster_size    
        mean_x/=cluster_size
        mean_y/=cluster_size               
        new_dist= np.sqrt((mean_r-r)**2+(mean_g-g)**2+(mean_b-b)**2+(mean_x-x)**2+(mean_y-y)**2)       
        if(new_dist<iters):
            for s in range(0,cluster_size):
                t=cluster[s]
                x,y=int(FV[t][3]),int(FV[t][4])
                image[x][y][0] = mean_r
                image[x][y][1] = mean_g
                image[x][y][2] = mean_b
            FV=np.delete(FV,cluster,0)
            size=len(FV)
            res=False
        
        else:
            r,g,b,x,y=mean_r,mean_g,mean_b,mean_x,mean_y
            res=True           

cv2.imwrite('Image.png',image)