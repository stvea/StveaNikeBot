import sqlite3
def createDataBase():
	nikedb = sqlite3.connect('nike.db')
	nikedbCursor = nikedb.cursor()
	nikeac = 'CREATE TABLE `nikeaccount` (`id` int(11) NOT NULL,`email` varchar(30),`password` varchar(30),`phone` varchar(30)  UNIQUE,`refreshToken` varchar(1000),`token` varchar(1000),`time` varchar(100),`accessTime` varchar(100))'
	nikeor = 'CREATE TABLE `nikeorder` (`id` int(11) NOT NULL,`orderid` varchar(100),`accessToken` varchar(1000),`time` varchar(100),`results` varchar(30),`accountName` varchar(100))'
	# nikedbCursor.execute(nikeor)
if __name__ == '__main__':
	createDataBase()