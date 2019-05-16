from webapp.db import db


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), index=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return F'<Tasks {self.title} {self.text}>'
