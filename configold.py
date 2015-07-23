CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

import os
basedir = os.path.abspath(os.path.dirname(__file__))


# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# from sqlalchemy import create_engine
# SQLALCHEMY_DATABASE_URI = create_engine("mssql+pyodbc://dashboarddatadev", encoding='windows-1255', convert_unicode=True)
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:3Machine@localhost/postgres'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


# MAIL_SERVER = "allsmtp.acgov.org"
# MAIL_PORT = 25
# MAIL_USE_TLS = False
# MAIL_USE_SSL = False
# MAIL_USERNAME = 'you'
# MAIL_PASSWORD = 'your-password'

# # administrator list
# ADMINS = ['Chet@acbhcs.org']