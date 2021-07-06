from app.main import db, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

Base = declarative_base()
metadata = MetaData(bind = engine)


class EPIROC(db.Model):
    #__table__ = Table('EPIROC', metadata, Column('Time', String, primary_key = True), autoload= True)
    __tablename__ = 'EPIROC'
    index = db.Column(db.Integer, primary_key=True)
    PenetrRate = db.Column(db.Float)
    PercPressure = db.Column(db.Float)
    FeedPressure = db.Column(db.Float)
    RotPressure = db.Column(db.Float)
    InstRotPressure = db.Column(db.Float)
    holeID = db.Column(db.String(32))
    depth = db.Column(db.Float)
    Time = db.Column(db.String(50))




class BlastCluster(db.Model):
    __tablename__ = 'BlastCluster'
    holeID = db.Column(db.String(32), primary_key = True)
    depth = db.Column(db.Float, primary_key = True) ## holeID + Depth combination as the primary keys
    CID = db.Column(db.Integer)
    x = db.Column(db.Float) ## MDS Coordinate
    y = db.Column(db.Float) ## MDS Coordinate

    def __init__(self, holeID, depth, CID, x, y):
        self.holeID = holeID
        self.depth = depth
        self.CID = CID
        self.x = x
        self.y = y

    def serialize(self):
        return {'holeID': self.holeID, 'depth': self.depth, 'CID': self.CID, 'x': self.x, 'y': self.y}

class BlastReport(db.Model):
    __tablename__ = 'BlastReport'
    holeID = db.Column(db.String(32), primary_key = True)
    depth = db.Column(db.Float)
    report = db.Column(db.String(255))
    score = db.Column(db.Integer)

    def __init__(self, holeID, depth, report, score):
        self.holeID = holeID
        self.depth = depth
        self.report = report
        self.score = score

    def serialize(self):
        return {'holeID': self.holeID, 'depth': self.depth, 'report': self.report, 'score': self.score}

    def __repr__(self):
        return f"Report(holeID = {self.holeID}, depth = {self.depth}, report = {self.report}, score = {self.score})"


