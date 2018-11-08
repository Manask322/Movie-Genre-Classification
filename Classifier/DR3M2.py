from __future__ import division
from scipy.spatial import distance
import featexup2 as ft2
import numpy as np
import os
import pandas as pd
import bottleneck as bn

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


for j in Num:
	minind=None
	minval=float("inf")
	print j
	vals=[0 for z in range(6)]
	if(not (os.path.exists('/home/manas/Desktop/Desktop/movie-genre-master/movie-genre-master/test_photo/'+'poster_'+str(j)+'.jpeg'))):
		continue
	cen,fac=ft2.getFeat('/home/manas/Desktop/Desktop/movie-genre-master/movie-genre-master/test_photo/'+'poster_'+str(j)+'.jpeg')
	cen.append(fac)
	for gen in lit1:
		#print gen
		df=pd.read_csv(os.path.join('../featureextraction/KMRep2',gen+'rep.csv'),header=None)
		#print len(df.index)		
		avg=0
		for i in range(len(df.index)):
			cen1=df.iloc[i]
			a=distance.euclidean(cen,cen1)
			#print nth1
			avg+=a
		dist=avg/len(df.index)
		#print avge
		#ind=lit1.index(gen)
		if(dist<minval):
			minval=dist
			minind=lit1.index(gen)
	#z=bn.argpartition(vals,3)[:3]
	string=lit1d[lit1[minind]]
	gens=string.split("|")
	for k in gens:
		if(k in genre2[j-4000]):
			NoC+=1
print (NoC)/800
print 1-(NoC)/800


