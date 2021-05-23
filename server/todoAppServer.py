from flask import Flask,jsonify, request
import json
from flask_cors import CORS
from mongoengine import connect, StringField, Document, DateTimeField, BooleanField
from datetime import datetime
connect("todo")
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


class todoObject():
    _id = ""
    title = ""
    description = ""
    is_completed = None
    created_at = ""
    updated_at = ""

class todos(Document):
    title = StringField()
    description = StringField()
    is_completed = BooleanField()
    created_at = DateTimeField()
    updated_at = DateTimeField()


@app.route('/todos', methods=['GET', 'POST', 'PUT'])
@app.route('/todos/<string:oid>', methods=['DELETE'])
def index(oid=None):
    if oid == None:
        if request.method == "GET":
            all_todos = todos.objects()
            if len(all_todos) < 1:
                return ""
            else:
                all_objects = []
                for object in todos.objects().order_by('-id'):
                    new_todoObject = todoObject()
                    new_todoObject._id = str(object.id)
                    new_todoObject.title = object.title
                    new_todoObject.description = object.description
                    new_todoObject.is_completed = object.is_completed
                    new_todoObject.created_at = object.created_at.strftime("%m/%d/%Y, %H:%M:%S")
                    new_todoObject.updated_at = object.updated_at.strftime("%m/%d/%Y, %H:%M:%S")
                    all_objects.append(new_todoObject.__dict__)
                return json.dumps(all_objects)

        elif request.method == "POST":
            data = request.get_json()
            new_todos = todos()
            new_todos.title = data['title']
            new_todos.description = data['description']
            new_todos.is_completed = False
            new_todos.created_at = datetime.now()
            new_todos.updated_at = datetime.now()
            new_todos.save()
            return jsonify(success = "OK")

        elif request.method == "PUT":
            data = request.get_json()
            oid = data['_id']
            object = todos.objects(id = oid).first()
            if object:
                object.is_completed = True
                object.save()
                return jsonify(success = "OK")
            else:
                return jsonify(success = "FAIL")


    else:
        if request.method == "DELETE":
            object = todos.objects(id = oid).first()
            if object:
                object.delete()
                return jsonify(success = "OK")
            else:
                return jsonify(success = "FAIL")

if __name__ == '__main__':
    app.run(port=5005, debug=True)
