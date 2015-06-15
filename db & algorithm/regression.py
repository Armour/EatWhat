import numpy as np
import random
import math
import mysql.connector

config = {
	'user' : 'root',
	'password' : '',
	'host' : '127.0.0.1',
	'database' : 'eat',
	'raise_on_warnings': True
}

db = mysql.connector.connect(**config)
cursor = db.cursor()

def LoadInData():
	global db
	storeAmount = 100
	userAmount = 10
	UserToStore =  np.array([[random.randint(-5,5) for i in xrange(storeAmount)] for j in xrange(userAmount)])
	
	query = ('SELECT * FROM user')
	print cursor.execute(query)
	print ':) '

	return storeAmount, userAmount, UserToStore

def SaveInData(EatWhat):
	global db
	print len(EatWhat)
	print EatWhat
	return 
	add_user = ("INSERT INTO user "
               "(id, username, password) "
               "VALUES (%s, %s, %s)")
	info_user = (str(10),'kael','123123')
	cursor.execute(add_user,info_user)
	db.commit()
	print 'XD'
	pass


def UserCollaborativeFiltering():
	from sklearn.neighbors import KDTree

	storeAmount, userAmount, UserToStore = LoadInData()
	kdRange = 10
	
	kdt = KDTree(UserToStore, leaf_size=30, metric='euclidean')
	dis, ans = kdt.query(UserToStore, k=kdRange, return_distance=True)    

	EatWhat = []
	axisX = -1

	for line in ans:
		axisX += 1
		if axisX > 5:
			break
		person = line[0]

		print 'The similar person to %d' % person,
		print 'is',
		print line[1:]
		'''
		print dis
		'''
		recommand = []
		#continue
		for _y in xrange(kdRange - 1):
			axisY = _y + 1
			others = line[axisY]

			'''
			print person, others, axisX, axisY
			print dis[axisX]
			print dis[axisX][axisY]
			'''
			
			power =  math.sqrt((1 / (1 + dis[person][others]))	 * 100) / 10

			tmp = [[i ,UserToStore[others][i]] for i in xrange(storeAmount)]
			
			tmp = sorted(tmp,key=lambda each:each[1],reverse=True)

			highRank = [each[0] for each in tmp[:5]]

			for store in highRank[:10]:
				if store not in recommand:
					recommand.append(store)

		recommand = random.sample(recommand,5)

		print 'recommanded store',
		print recommand
		
		EatWhat.append(recommand)

		print 

	SaveInData(EatWhat)


def main():
	#UserCollaborativeFiltering()
	UserCollaborativeFiltering()

if __name__ == '__main__':
	main()