#!flask/bin/python
from app import app, db
# app.run(host='0.0.0.0',debug=True)
# app.run(debug = True)
# app.run(host='0.0.0.0',port=5000,debug=True)


#!flask/bin/python
# from app import app

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
# from flask.ext.login import LoginManager, UserMixin, login_required

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()