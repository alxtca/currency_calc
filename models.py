from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Currency(db.Model):
    __tablename__ = "currency"
    id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    cost_to_eur = db.Column(db.Float, nullable=False)
    date = db.Column(db.String, nullable=False)


class Counter(db.Model):
    __tablename__ = "counter"
    id = db.Column(db.Integer, primary_key=True)
    times = db.Column(db.Integer)
