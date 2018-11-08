'''
Other References:
[1] http://www.iiisci.org/journal/cv$/sci/pdfs/p104824.pdf
'''

import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import bottleneck as bn

#function to compute image histograms
def colhs(hsv,n,feature):

	hist_h = cv2.calcHist([hsv],[0],None,[50],[0, 180])
	#x=[i for i in range(50)]
	#plt.bar(x,hist_h)
	#plt.title('Histogram for Hue')
	#savestr='hue'+str(n)+'.png'
	#print(n,hist_h)
	#plt.savefig(savestr)
	#plt.clf()
	#hist_h=cv2.normalize(hist_h,hist_h,1,0)
	#print hist_h
	ht=[]
	for i in hist_h:
		ht.append(int(i))
	feature.extend(ht)	

	hist_s = cv2.calcHist([hsv],[1],None,[60],[0, 256])
	#x=[i for i in range(60)]
	#plt.bar(x,hist_s)
	#plt.title('Histogram for Saturation')
	#savestr='sat'+str(n)+'.png'
	##print(n,hist_s)
	st=[]
	for i in hist_s:
		st.append(int(i))
	feature.extend(st)
	#plt.savefig(savestr)
	#plt.clf()
	#plt.close()
	return feature,ht,st


def getFeat(filename):
	feature=[]
# Read BGR image and store the HSV
	img = cv2.imread(filename, 1)
	img = cv2.resize(img, (200, 300)) 
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	feature,ht,st=colhs(hsv,0,feature)
	#cv2.imshow('image',img)
	cv2.imwrite("hsv.jpg",hsv)
	#cv2.imshow('hsv_image',hsv)

	# Segment Image into 3x2 blocks and centre block
	nhsv = Image.open('hsv.jpg')
	width = nhsv.size[0]
	height = nhsv.size[1]

	block1=nhsv.crop((0,0,100,100))
	block1.save("hsvbl1.jpg")
	'''block2=nhsv.crop((0,100,100,200))
	block2.save("hsvbl2.jpg")
	block3=nhsv.crop((100,0,200,100))
	block3.save("hsvbl3.jpg")
	block4=nhsv.crop((100,100,200,200))
	block4.save("hsvbl4.jpg")'''
	block5=hsv[200:300]
	cv2.imwrite("hsvbl.jpg",block5)
	block5=Image.open('hsvbl.jpg')
	block5=block5.crop((0,0,100,100))
	block5.save("hsvbl5.jpg")
	block6=nhsv.crop((width - 100,height - 100,width,height))
	block6.save("hsvbl6.jpg")
	block7=nhsv.crop((35,50,165,250))
	block7.save("hsvbl7.jpg")

	# Read HSV blocks after saving
	#block1 = cv2.imread('hsvbl1.jpg', 1)
	#block2 = cv2.imread('hsvbl2.jpg', 1)
	#block3 = cv2.imread('hsvbl3.jpg', 1)
	#block4 = cv2.imread('hsvbl4.jpg', 1)
	block5 = cv2.imread('hsvbl5.jpg', 1)
	block6 = cv2.imread('hsvbl6.jpg', 1)
	block7 = cv2.imread('hsvbl7.jpg', 1)

	#compute histograms
	#colhs(block1,1)
	#colhs(block2,2)
	#colhs(block3,3)
	#colhs(block4,4)
	colhs(block5,5,feature)
	colhs(block6,6,feature)
	colhs(block7,7,feature)

	Z = hsv.reshape((-1,3))

	# convert to np.float32
	Z = np.float32(Z)

	# define criteria, number of clusters(K) and apply kmeans()
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
	K = 12
	ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

	# Now convert back into uint8, and make original image
	center = np.uint8(center)
	res = center[label.flatten()]
	res2 = res.reshape((hsv.shape))
	
	#cv2.imshow('res2',res2)

	# Edge Detection
	edges = cv2.Canny(hsv,100,200)

	#plt.subplot(121),plt.imshow(hsv,cmap = 'gray')
	#plt.title('Original Image'), plt.xticks([]), plt.yticks([])
	#plt.subplot(122),plt.imshow(edges,cmap = 'gray')
	#plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

	#plt.savefig("edge.png")
	#plt.clf()
	#plt.close()
	edgehist=[0 for z in range(256)]
	#edgein=[z for z in range(256)]

	# Edge based Feature extraction [1]
	#print(len(edges))
	for l in range (len(edges)):
		for b in range(200):
			if edges[l][b]==255 and l>0 and l<299 and b>0 and b<199 :
				n0 = edges[l][b+1]/255
				n4 = edges[l][b-1]/255
				n7 = edges[l+1][b+1]/255
				n5 = edges[l+1][b-1]/255
				n6 = edges[l+1][b]/255
				n1 = edges[l-1][b+1]/255
				n3 = edges[l-1][b-1]/255
				n2 = edges[l-1][b]/255
				feat = int(str(n7)+str(n6)+str(n5)+str(n4)+str(n3)+str(n2)+str(n1)+str(n0),2)
				edgehist[feat]+=1

	feature.extend(edgehist)	
	#plt.bar(edgein,edgehist)
	#plt.title('Histogram for Edge')
	#plt.savefig("edgehist.png")
	#plt.clf()
	#plt.close()
				
			
	# Viola-Jones face detector
	'''face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	imgbl = cv2.GaussianBlur(img,(3,3),0)

	gray = cv2.cvtColor(imgbl, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.04, 3)

	print("No. of Faces:",len(faces))
	for (x,y,w,h) in faces:
	    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	    roi_gray = gray[y:y+h, x:x+w]
	    roi_color = img[y:y+h, x:x+w]'''
	    

	#cv2.imshow('img',img)
	#print(center)
	center=list(center.flatten())
	#print center
	feature.extend(center)
	cv2.destroyAllWindows()
	return feature,ht,st,edgehist

if __name__=="__main__":
	feature,ht,st,et=getFeat("hsv.jpg")
	#print feature
	#print ht
	#print et

