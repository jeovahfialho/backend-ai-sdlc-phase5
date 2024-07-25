
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notifications.db'
db = SQLAlchemy(app)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=db.func.current_timestamp())

@app.route('/notify', methods=['POST'])
def notify():
    user_id = request.json['user_id']
    title = request.json['title']
    message = request.json['message']
    notification = Notification(user_id=user_id, title=title, message=message)
    db.session.add(notification)
    db.session.commit()
    return jsonify({'message': 'Notification sent'}), 201

def send_notification():
    print("Sending Slot Showdown notification to registered players")

scheduler = BackgroundScheduler()
scheduler.add_job(send_notification, 'interval', hours=1)
scheduler.start()

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
