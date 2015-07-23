from app import db
from sqlalchemy.orm import relationship
class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    projectleader = db.Column(db.String(35))    
    goals = db.relationship('Goals', lazy='dynamic', backref='proj',cascade="all, delete-orphan"
                               )
    def __repr__(self):
        return '<Project %r>' % (self.name)

class Goals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(200))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    strategies = db.relationship('Strategies',lazy='dynamic',order_by="Strategies.order", backref='goa',cascade="all, delete-orphan")
    order = db.Column(db.Integer)                                     

    def __repr__(self):
        return '<Goals %r>' % (self.goal)

class Strategies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strategy = db.Column(db.String(200))
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'))
    tasks = db.relationship('Tasks', lazy='dynamic',order_by="Tasks.order",backref='strat',cascade="all, delete-orphan")
    order = db.Column(db.Integer)                            
    def __repr__(self):
        return '<Strategy %r>' % (self.strategy)

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    note = db.Column(db.String(400))  
    complete = db.Column(db.Boolean())
    staff = db.Column(db.String(50))
    deadline = db.Column(db.Date)
    completeDate = db.Column(db.Date)
    created = db.Column(db.Date)
    strategy_id = db.Column(db.Integer, db.ForeignKey('strategies.id'))
    order = db.Column(db.Integer)
    def __repr__(self):
        return '<Tasks %r>' % (self.task)

class FileUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50))
    note = db.Column(db.String(400))  
    def __repr__(self):
        return '<sender %r>' % (self.strategy)

# class User(db.Model):
#     """An admin user capable of viewing reports.

#     :param str email: email address of user
#     :param str password: encrypted password for the user

#     """
#     __tablename__ = 'user'
#     __bind_key__ = 'request'
#     name=db.Column(db.String)
#     email = db.Column(db.String, primary_key=True)
#     authenticated = db.Column(db.Boolean, default=True)

#     def is_active(self):
#         """True, as all users are active."""
#         return True

#     def get_id(self):
#         """Return the email address to satisfy Flask-Login's requirements."""
#         return self.email

#     def is_authenticated(self):
#         """Return True if the user is authenticated."""
#         return self.authenticated

#     def is_anonymous(self):
#         """False, as anonymous users aren't supported."""
#         return False




# class Request(db.Model):
#     __bind_key__ = 'request'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True)
#     email = db.Column(db.String(120), index=True)
#     emanio= db.Column(db.Integer)
#     MHorSUD= db.Column(db.String(64), index=True)
#     keyQuestions= db.Column(db.String(64), index=True)
#     problem= db.Column(db.String(64), index=True)
#     specialFacts= db.Column(db.String(64), index=True)
#     requestDate= db.Column(db.DateTime, index=True)
#     requestDeadlineLapse= db.Column(db.Integer)
#     requestedBy= db.Column(db.String(64), index=True)
#     deadlinedate= db.Column(db.Date)
#     priority= db.Column(db.String(64), index=True)
#     deliveryFormat= db.Column(db.String(64), index=True)
#     timeframe= db.Column(db.String(64), index=True)
#     timeBreakdown= db.Column(db.String(64), index=True)
#     specialPop= db.Column(db.String(64), index=True)
#     agency= db.Column(db.String(64), index=True)
#     ru = db.Column(db.String(64), index=True)
#     typeOfService= db.Column(db.String(64), index=True)
#     jobTitle= db.Column(db.String(64), unique=True)
#     longDescription= db.Column(db.String(64), index=True)
#     specialInstructions= db.Column(db.String(64), index=True)
#     audience= db.Column(db.String(64), index=True)
#     columnsRequired= db.Column(db.String(64), index=True)
#     assinged= db.Column(db.String(64), index=True)
#     completeDate= db.Column(db.Date)
#     reviewed= db.Column(db.String(64), index=True)
#     userCategory= db.Column(db.String(64), index=True)
#     deadlinetime =db.Column(db.Integer)
#     deadlineWhy =  db.Column(db.String(64), index=True)
#     timeframestart =db.Column(db.Date)
#     timeframeend= db.Column(db.Date)
#     note= db.Column(db.String(120), index=True)
#     Response= db.Column(db.String(120), index=True)

#     def __repr__(self):
#         return '<%r>' % (self.jobTitle)
