import json
from datetime import datetime
import bson
import pymongo
from bson import json_util
from flask import Flask, jsonify, request, redirect, url_for

app = Flask(__name__)
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["task_details"]
mycol = mydb["task"]


@app.route('/')
def retrieveAll():
    holder = list()
    for i in mycol.find():
        idlist = json.loads(json_util.dumps(i['_id']))
        holder.append({'id': idlist, 'content': i['content'], 'date': i['date_created']})
    return jsonify(holder)


@app.route('/<id>', methods=['GET'])
def retrieveByName(id):
    display = mycol.find_one({'_id': bson.ObjectId(oid=str(id))})
    return jsonify({'Task': display['content'], 'Date': display['date_created']})


@app.route('/insertdata', methods=['POST'])
def insertData():
    content = request.json['content']
    date = datetime.utcnow()
    mycol.insert_one({'content': content, 'date_created': date})
    return jsonify({'Task': content, 'date': date})


@app.route('/deletepage/<id>', methods=['DELETE'])
def deletePage(id):
    mycol.delete_one({'_id': bson.ObjectId(oid=str(id))})
    return redirect(url_for('retrieveAll'))


@app.route('/updatepage/<id>', methods=['PUT'])
def updatePage(id):
    update = request.json['content']
    mycol.update_one({'_id': bson.ObjectId(oid=str(id))}, {"$set": {'content': update}})
    return redirect(url_for('retrieveAll'))


if __name__ == '__main__':
    app.run(debug=True)


