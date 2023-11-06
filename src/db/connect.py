# connect to mysql on flask
from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# read config.yaml file for database connection details
# Load data from a YAML file using SafeLoader
with open('configs/db.yaml', 'r') as yaml_file:
    db = yaml.load(yaml_file, Loader=yaml.SafeLoader)

# configure database connection
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_PORT'] = db['mysql_port']

# initialize database connection
mysql = MySQL(app)

# create table
@app.route('/create', methods=['GET', 'POST'])
def create():
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id INT(11) AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), username VARCHAR(30), password VARCHAR(100))''')
    mysql.connection.commit()
    cur.close()
    return 'Table created successfully'

# export mysql that can use from another class 
def get_mysql():
    return mysql