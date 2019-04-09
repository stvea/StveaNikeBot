import sqlite3

class SqliteDao:
	def initDataBase(self):
		nikeac = 'CREATE TABLE IF NOT EXISTS `nikeaccount` (`id` int(11) NOT NULL,`email` varchar(30),`password` varchar(30),`phone` varchar(30)  UNIQUE,`refreshToken` varchar(1000),`token` varchar(1000),`time` varchar(100),`accessTime` varchar(100))'
		nikeor = 'CREATE TABLE IF NOT EXISTS `nikeorder` (`id` int(11) NOT NULL,`orderid` varchar(100),`accessToken` varchar(1000),`time` varchar(100),`results` varchar(30),`accountName` varchar(100))'
		SqliteDao.cur.execute(nikeac)
		SqliteDao.cur.execute(nikeor)

	def sqliteFetch(self,sql):
		SqliteDao.cur.execute(sql)
		res = SqliteDao.cur.fetchall()
		return res

	def sqliteUpdate(self,sql):
		SqliteDao.cur.execute(sql)
		SqliteDao.conn.commit()
		
	def __init__(self,dbname='nike'):
		SqliteDao.conn = sqlite3.connect(dbname+'.db')
		SqliteDao.cur = SqliteDao.conn.cursor()
		self.initDataBase()