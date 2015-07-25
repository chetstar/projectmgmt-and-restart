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
