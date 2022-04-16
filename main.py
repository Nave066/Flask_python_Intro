from pytz import timezone
from datetime import datetime
import bson
import pymongo
from bson import json_util
from flask import Flask, jsonify, request, redirect, url_for, render_template

app = Flask(__name__)
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["task_details"]
mycol = mydb["task"]


@app.route('/', methods=['GET'])
def retrieveAll():
    global getting_details
    for i in mycol.find():
        getting_details = mycol.find()
    return render_template('index.html', send=getting_details)


# @app.route('/<id>', methods=['GET'])
# def retrieveByName(id):
#     display = mycol.find_one({'_id': bson.ObjectId(oid=str(id))})
#     return jsonify({'Task': display['content'], 'Date': display['date_created']})


@app.route('/insertdata', methods=['POST'])
def insertData():
    content = request.form.get('task')
    date = datetime.now(timezone("Asia/Kolkata"))
    mycol.insert_one({'content': content, 'date_created': str(date)})
    return redirect(url_for('retrieveAll'))


@app.route('/deletepage/<id>', methods=['DELETE', 'POST', 'GET'])
def deletePage(id):
    mycol.delete_one({'_id': bson.ObjectId(oid=str(id))})
    return redirect(url_for('retrieveAll'))


@app.route('/updatepage/<id>', methods=['PUT', 'POST', 'GET'])
def updatePage(id):
    if request.method == 'POST':
        content = request.form.get('task')
        date = str(datetime.now(timezone("Asia/Kolkata")))
        mycol.update_one({'_id': bson.ObjectId(oid=str(id))}, {"$set": {'content': content, 'date_created': date}})
        return redirect(url_for('retrieveAll'))
    get_details = mycol.find_one({'_id': bson.ObjectId(oid=str(id))})
    return render_template('update.html', send_data=get_details)


if __name__ == '__main__':
    app.run(debug=True)
