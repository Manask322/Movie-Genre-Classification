import pandas as pd
import tmdbpy as tb
import os

df=pd.read_csv("FormattedMovieData2.csv")
ID=list(df.ID)
Num=list(df.Num)
print 
for i,num in zip(ID,Num):
	if(os.path.exists("./Posters/p_"+str(num)+".jpeg")):
		continue
	else:
		print num
		tb.tmdb_posters(str(i),num,1)
	
