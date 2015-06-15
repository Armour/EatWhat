import json
import mysql.connector
import re
config = {
	'user' : 'root',
	'password' : '',
	'host' : '127.0.0.1',
	'database' : 'eat',
	'raise_on_warnings': True
}

db = mysql.connector.connect(**config)
cursor = db.cursor()

data = json.load(file('meituan.json'))

count = -1
for each in data:
	count += 1
	re_num = re.compile(r'[0-9]+')
	info_restaurant = ()
	each['total'] = re_num.search(each['total']).group(0)
	try:	
		each['score'] = re.search(r'\d.\d',each['score']).group(0)
	except AttributeError:
		each['score'] = '0'
	

	print 'name:',
	print each['name'],
	print 'score:',
	print each['score'],
	print 'total:'
	print each['total']
	print 'url:',
	print each['img_url']
	
	add_restaurant = ("INSERT INTO restaurant "
               "(id, name, score, total, picture) "
               "VALUES (%s, %s, %s, %s, %s)")
	info_restaurant = (count,each['name'].encode('utf-8'),each['score'], each['total'],each['img_url'])
	cursor.execute(add_restaurant,info_restaurant)

db.commit()