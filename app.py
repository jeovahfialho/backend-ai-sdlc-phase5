
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
    opt_out = db.Column(db.Boolean, default=False)

@app.route('/notify', methods=['POST'])
def notify():
    user_id = request.json['user_id']
    title = "Slot Showdown Promotion"
    message = request.json['message'] + "\n\nthe opportunity to win exciting prizes while playing your favorite slots\nJoin the competition and start playing your favorite slots now!\nIf you do not wish to receive these notifications, you can opt-out."
    notification = Notification(user_id=user_id, title=title, message=message)
    db.session.add(notification)
    db.session.commit()
    return jsonify({'message': 'Notification sent'}), 201

@app.route('/opt-out', methods=['POST'])
def opt_out():
    user_id = request.json['user_id']
    notifications = Notification.query.filter_by(user_id=user_id).all()
    for notification in notifications:
        notification.opt_out = True
    db.session.commit()
    return jsonify({'message': 'You have successfully opted out of notifications.'}), 200

def send_notification():
    notifications = Notification.query.filter_by(opt_out=False).all()
    for notification in notifications:
        print(f"Sending {notification.title} to user {notification.user_id}")

scheduler = BackgroundScheduler()
scheduler.add_job(send_notification, 'interval', hours=1)
scheduler.start()

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
