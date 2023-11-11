class Config():
	DEBUG = True
	#db
	SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/test_flask?unix_socket=/opt/lampp/var/mysql/mysql.sock'
	SQLALCHEMY_TRACK_MODIFICATIONS = False