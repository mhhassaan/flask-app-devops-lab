from flask import Flask, request, jsonify,  render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure SQLite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'feedback.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "message": self.message}


# Initialize DB
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")    

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200


@app.route('/feedback', methods=['POST'])
def add_feedback():
    data = request.get_json()
    if not data or 'name' not in data or 'message' not in data:
        return jsonify({"error": "Name and message are required"}), 400

    fb = Feedback(name=data['name'], message=data['message'])
    db.session.add(fb)
    db.session.commit()
    return jsonify(fb.to_dict()), 201


@app.route('/feedback', methods=['GET'])
def get_feedback():
    feedback_list = Feedback.query.all()
    return jsonify([fb.to_dict() for fb in feedback_list]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
