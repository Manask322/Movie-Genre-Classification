import numpy as np
import operator

def Gen(g):
	spgn=["Action","Animation","Comedy","Drama","Horror","War"] 
	supergen=[0]*6
	if("Action" in g):
		supergen[0]+=1
	if("Animation" in g):
		supergen[1]+=100
	if("Adventure" in g):
		supergen[0]+=1
		supergen[3]+=2
	if("Comedy" in g):	
		supergen[2]+=1
	if("Crime" in g):
		supergen[0]+=3
		supergen[3]+=1
	if("Disaster" in g):
		supergen[4]+=1
		supergen[0]+=1
	if("Drama" in g):
		supergen[3]+=1
	if("Fantasy" in g):
		supergen[0]+=1
	if("History" in g):
		supergen[5]+=1
	if("Horror" in g):
		supergen[4]+=100
		supergen[0]+=10
	if("Romance" in g):
		supergen[3]+=1
	if("Science Fiction" in g):
		supergen[0]+=2
		supergen[3]+=1
	if("War" in g):
		supergen[5]+=1
	if("Thriller" in g):
		supergen[3]+=1
	if("Western" in g):
		supergen[0]+=1
	ind=np.array(supergen)
	ind=np.argpartition(ind,-2)[-2:]
	ind=np.sort(ind)
	if(supergen[ind[1]]==0):
		Genre=spgn[ind[0]]+"|"+"NULL"
	else:
		Genre=spgn[ind[0]]+"|"+spgn[ind[1]]
	max_index, max_value = max(enumerate(supergen), key=operator.itemgetter(1))
	m1=spgn[max_index]
	return Genre,m1
