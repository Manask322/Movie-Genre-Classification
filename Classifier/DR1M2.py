from __future__ import division
import cv2
import featexup as ft
import numpy as np
import pandas as pd	
import os
'''feature1,ht1,st1,et1=ft.getFeat("../featureextraction/TestPost/tfg.jpg")
feature2,ht2,st2,et2=ft.getFeat("../featureextraction/TestPost/jw.jpg")
'''
df0=pd.read_csv("temp.csv")
Num=list(df0.Num)
genre2=list(df0.Genre2)
lit1=['AcD',
'DN',
'AnN',
'AnD',
'AnC',
'AcN',
'AcH',
'AcAn',
'AcC',
'DW',
'CD',
'AcW',
'CW'
]
lit1d={'AcD':"Action|Drama",
'DN':"Drama|NULL",
'AnN':"Animation|NULL",
'AnD':"Animation|Drama",
'AnC':"Animation|Comedy",
'AcN':"Action|NULL",
'AcH':"Action|Horror",
'AcAn':"Action|Animatiom",
'AcC':"Action|Comedy",
'DW':"Drama|War",
'CD':"Comedy|Drama",
'AcW':"Action|War",
'CW':"Comedy|War"
}
NoC=0
NoW=0
for j in Num:
	minind=None
	minval=float("inf")
	print j
	if(not (os.path.exists('/home/manas/Desktop/Desktop/movie-genre-master/movie-genre-master/test_photo/'+'poster_'+str(j)+'.jpeg'))):
		continue
	feature1,ht1,st1,et1=ft.getFeat('/home/manas/Desktop/Desktop/movie-genre-master/movie-genre-master/test_photo/'+'poster_'+str(j)+'.jpeg')
	#print len(et1)
	ht1=np.float32(ht1)
	nth1=np.ones(shape=(1,50))
	nth1 = cv2.normalize(ht1,nth1,alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
	st1=np.float32(st1)
	nts1=np.ones(shape=(1,60))
	nts1 = cv2.normalize(st1,nts1,alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
	et1=np.float32(et1)
	nte1=np.ones(shape=(1,256))
	nte1 = cv2.normalize(et1,nte1,alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
	for gen in lit1:
		#print gen
		df=pd.read_csv(os.path.join('../featureextraction/KMRep',gen+'hrep.csv'),header=None)
		#print len(df.index)		
		avgh=0
		for i in range(len(df.index)):
			ht2=list(df.iloc[i])		
			ht2=np.float32(ht2)
		
			nth2=np.ones(shape=(1,50))
			#print nth1
		
			nth2 = cv2.normalize(ht2,nth2,alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
			#print nth1
			a=cv2.compareHist(nth1,nth2,cv2.HISTCMP_CHISQR)
			avgh+=a
		avgh=avgh/len(df.index)
		#print avgh
		df=pd.read_csv(os.path.join('../featureextraction/KMRep',gen+'srep.csv'),header=None)		
		avgs=0
		for i in range(len(df.index)):
			st2=list(df.iloc[i])		
			st2=np.float32(st2)
			nts2=np.ones(shape=(1,60))
			#print nts1
			nts2 = cv2.normalize(st2,nts2,alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
			#print nts1
			b=cv2.compareHist(nts1,nts2,cv2.HISTCMP_CHISQR)
			avgs+=b
		avgs=avgs/len(df.index)
		#print avgs
		df=pd.read_csv(os.path.join('../featureextraction/KMRep',gen+'erep.csv'),header=None)		
		avge=0
		for i in range(len(df.index)):
			et2=list(df.iloc[i])		
			et2=np.float32(et2)
			nte2=np.ones(shape=(1,256))
			#print nte1
			nte2 = cv2.normalize(et2,nte2,alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
			#print nte1
			c=cv2.compareHist(nte1,nte2,cv2.HISTCMP_CHISQR)
			avge+=c
		avge=avge/len(df.index)
		#print avge
		dist=avgh+avgs+avge
		if(dist<minval):
			minval=dist
			minind=lit1.index(gen)
	string=lit1d[lit1[minind]]
	gens=string.split("|")
	for k in gens:
		if(k in genre2[j-4000]):
			NoC+=1
			break
print (NoC)/800
print 1-(NoC)/800







