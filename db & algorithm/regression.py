#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import numpy as np
import random
import math
import mysql.connector
import json

config = {
	'user' : 'orz',
	'password' : '123456',
	'host' : '127.0.0.1',
	'database' : 'eat',
	'raise_on_warnings': True
}

db = mysql.connector.connect(**config)
cursor = db.cursor()

def LoadInData():
	global db
	_storeAmount = 100
	_userAmount = 20
	_UserToStore =  np.array([[random.randint(-5,5) for i in xrange(_storeAmount)] for j in xrange(_userAmount)])
	
	storeAmount = 0
	userAmount = 0

	query = ('select count(*) from user')
	cursor.execute(query)

	for each in cursor:
		userAmount = each[0]
		break

	query = ('select count(*) from restaurant')
	cursor.execute(query)

	for each in cursor:
		storeAmount = each[0]
		break

	query = ('select * from evaluate')
	cursor.execute(query)

	inMatrix = [[0 for i in xrange(storeAmount+1)] for j in xrange(userAmount+1)]
	for each in cursor:
		inMatrix[each[1]][each[2]] = each[3]

	UserToStore = np.array(inMatrix)
	

		
	return storeAmount, userAmount, UserToStore

def SaveInData(EatWhat):
	global db
	print EatWhat
	res = {}	
	for each in xrange(len(EatWhat)):
		#print EatWhat[each]
		res[each] = EatWhat[each]

	with open('recommend.json','w') as outfile:
		json.dump(res,outfile,indent=4)

	return 

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
		#if axisX > 5:
			#break
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

			#power =  math.sqrt((1 / (1 + dis[person][others]))	 * 100) / 10

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
	#LoadInData()
	UserCollaborativeFiltering()

if __name__ == '__main__':
	main()
