class Config():
	DEBUG = True
	#db
	SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/smarteng_smartengtest?unix_socket=/opt/lampp/var/mysql/mysql.sock'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# ?unix_socket=/opt/lampp/var/mysql/mysql.sock

	#'mysql:@Smartengtest123//smarteng_smarteng@smartengtest.com/smarteng_smartengtest'
