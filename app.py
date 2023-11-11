from flask import Flask
# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand
from src.utils.db import db
# Import controllers
from src.controllers.recommendation import Recommendation

app = Flask(__name__)
app.config.from_object('src.utils.setting.Config')

# initialization
db.init_app(app)

# adding routes
app.add_url_rule('/', view_func=Recommendation.HelloWord, methods=['GET',])

#run
if __name__ == '__main__':
	app.run(host='localhost')