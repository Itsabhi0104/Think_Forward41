from database import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    sender = db.Column(db.String(10))  # "user" or "ai"
    content = db.Column(db.Text, nullable=False)
