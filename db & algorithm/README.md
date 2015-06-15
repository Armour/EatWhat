# 关于算法的食用说明
1. 爬虫程序附在这里，有需要自己再趴会儿。
2. db_init.py 可以把meituan.json数据批量塞入mysql
3. regression.py 为算法程序，需要安装numpy,scipy和sklearn。
4. 运行regression.py以后，会返回每个用户推荐表单（大小可定制）到json里面

	~~~json
	{
	    "0": [
	        49, 
	        14, 
	        10, 
	        4, 
	        40, 
	        24, 
	        5, 
	        21, 
	        34, 
	        45
	    ], 
	    "1": [
	        38, 
	        25, 
	        19, 
	        0, 
	        40, 
	        33, 
	        5, 
	        4, 
	        2, 
	        8
	    ], 
    ...
	~~~
	
	* 单人模式： record['uid'] 即可获得推荐餐馆的list
	* 多人模式： record['uid1'] & record['uid2'] & record['uid3'] ..  即可获得推荐的餐馆list

PS: 由于数据库里还没有数据，所以现在暂时采用的是随即生成喜好，要改成从数据库里读，到LoadInData里，把return里变量前的下划线去掉就好。

PSS: 记得弄