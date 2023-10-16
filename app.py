from flask import Flask
# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand
# from inc.db import db
from src.routes.route import routes  # Import your routes

app = Flask(__name__)
# app.config.from_object('settings.Config')

# Initialization
# db.init_app(app)

# Migration
# migrate = Migrate(app, db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

# Register the Blueprint for your routes
app.register_blueprint(routes)

# Run the application
if __name__ == '__main__':
    app.run(host='localhost')
    # manager.run()
