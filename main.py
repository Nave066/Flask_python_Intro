from flask import Flask, render_template
from mongoengine import document, StringField, IntField, Document, connect
from datetime import datetime
# from flask_restful import Resource, Api

connect(host='mongodb://127.0.0.1:27017/flask')

app = Flask(__name__)


class Todo(Document):
    id = IntField()
    content = StringField()
    date_created = datetime.utcnow()

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
