from sklearn.neighbors import KDTree
import numpy as np
from random import randint

storeAmount = 10
userAmount = 1000
#Load in data added later
#UserToStore = loadindata()
UserToStore = np.array([[randint(0,5) for i in xrange(storeAmount)] for j in xrange(userAmount)])
#print UserToStore

kdt = KDTree(UserToStore, leaf_size=30, metric='euclidean')
ans = kdt.query(UserToStore, k=10, return_distance=False)    

count = 0
for line in ans:
	count += 1
	if count > 10:
		break
	
	print 'The similar person to %d' % line[0],
	print 'is',
	print line[1:]

	recommand = []
	for person in line[1:]:
		
		#print person
		tmp = [[i ,UserToStore[person][i]] for i in xrange(storeAmount)]
		#print tmp
		tmp = sorted(tmp,key=lambda each:each[1],reverse=True)
		#print 'tmp after sorted'
		#print tmp
		highRank = [each[0] for each in tmp[:5]]
		#print highRank
				#print tmp
		
		#print highRank
		for store in highRank[:10]:
			if store not in recommand:
				recommand.append(store)

	print 'recommandation:',
	print recommand
	print 

	print 
