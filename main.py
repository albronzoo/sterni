from flask import Flask, render_template, jsonify, request, session, redirect, url_for 
from datetime import datetime
from sqlalchemy import func
import json
import hashlib
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests


# App-Config | Global Variables
app = Flask(__name__)
app.secret_key = "Aal"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:@localhost:1235/data"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# App-Routes für die Straßenabfrage und den Tournament-Pick
@app.route('/')
def startmenu():
    return render_template('streets.html')

@app.route('/ranking')
def ranking():
    return render_template('tournament.html')

@app.route('/patron')
def patron():
    return render_template('patron.html')


# Database-Tables -> Straßen und Ranking
class Straßen(db.Model):
    __tablename__ = "straßen"
    id = db.Column(db.Integer, primary_key=True)
    straße = db.Column(db.String(64), nullable=False)
    iphash = db.Column(db.String(64), nullable=False, index=True)
    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    def __repr__(self):
        return f"<Straße {self.straße}, ID {self.iphash}, Uhrzeit {self.timestamp}>"

class Ranking(db.Model):
    __tablename__ = "ranking"
    id = db.Column(db.Integer, primary_key=True)
    winner = db.Column(db.String(64), nullable=False)
    loser = db.Column(db.String(64), nullable=False)
    iphash = db.Column(db.String(64), nullable=False, index=True)
    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )


# APIs bzw. Methoden zum posten der Daten
@app.route("/api/streets", methods=["POST"])
def street():
    data = request.get_json()
    street = Straßen(
        straße=data["street"],
        iphash=iphash(),
        timestamp=datetime.utcnow()
    )
    db.session.add(street)
    db.session.commit()
    return jsonify(success=True)


@app.route("/api/vote", methods=["POST"])
def vote():
    data = request.get_json()
    vote = Ranking(
        winner=data["winner"],
        loser=data["loser"],
        iphash=iphash(),
        timestamp=datetime.utcnow()
    )
    db.session.add(vote)
    db.session.commit()
    return jsonify(success=True)


# Hilfsfunktion um User-Hash zu bekommen
def iphash():
    ip = request.remote_addr or ""
    ua = request.headers.get("User-Agent", "")
    secret = app.config["SECRET_KEY"]
    return hashlib.sha256(
        f"{ip}|{ua}|{secret}".encode()
    ).hexdigest()

