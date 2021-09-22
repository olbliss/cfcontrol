from datetime import datetime
from flask_app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.Date, default=datetime.utcnow)
    time_posted = db.Column(db.Time, default=datetime.utcnow)
    date_closed = db.Column(db.Date)
    time_closed = db.Column(db.Time)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(100), nullable=False)
    assigned_to = db.Column(db.String(100), nullable=False)
    reported_by = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Post( '{self.id}', '{self.title}', '{self.description}', '{self.date_posted}', '{self.time_posted}', '{self.date_closed}', '{self.time_closed}', '{self.status}', '{self.priority}', '{self.assigned_to}', '{self.reported_by}')"

class Buggies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    BName = db.Column(db.String(100), nullable=False)
    BRider = db.Column(db.String(100), nullable=True)
    lastmodified = db.Column(db.DateTime, nullable=True)#, default=datetime.utcnow)

    def __repr__(self):
        return f"Buggies('{self.BName}', '{self.BRider}','{self.lastmodified}')"
