from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from datetime import date

db = SQLAlchemy()
DB_NAME = "scoreboard.db"

def application():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hello there'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db = SQLAlchemy(app)

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(150))
        pid = db.Column(db.Integer)
        score = db.Column(db.Integer)
        date_added = db.Column(db.DateTime, default=datetime.utcnow)

    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            name = request.form.get('fname')
            id = request.form.get('fid')
            points = request.form.get('points')
            new_user = User(name=name,pid=id,score=points)
            db.session.add(new_user)
            db.session.commit()
        return render_template("webpage.html")
    
    @app.route('/database.html')
    def database():
        our_users = User.query.order_by(User.name)
        return render_template("database.html",our_users=our_users)

    @app.route('/search.html', methods=['GET', 'POST'])
    def search():
        if request.method == 'POST':
            name = request.form.get('fname')
            user = User.query.filter_by(name=name).first()
            if user:
                flash("Name: " + user.name + "  ID: " + str(user.pid) + " Points: " + str(user.score))
                return redirect(url_for('search'))
            else:
                flash("User does not exist")
                return redirect(url_for('search'))
            
        return render_template("search.html")
    
    @app.route('/remove.html', methods=['GET', 'POST'])
    def remove():
        if request.method == 'POST':
            name = request.form.get('fname')
            user = User.query.filter_by(name=name).first()

            try:
                db.session.delete(user)
                db.session.commit()
                flash("User deleted!")
                return redirect(url_for('remove'))
            except:
                flash("User does not exist, try again")
                return redirect(url_for('remove'))
            
        return render_template("remove.html")

    with app.app_context():
        db.create_all()

    return app





