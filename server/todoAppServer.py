from flask import Flask, jsonify, request
import json
from flask_cors import CORS
from mongoengine import connect, StringField, Document, DateTimeField, BooleanField
from datetime import datetime

connect("todo")
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


class todoObject:

    _id = ""
    title = ""
    description = ""
    is_completed = None
    created_at = ""
    updated_at = ""

    def __init__(self, **kwargs) -> "todoObject":

        self._id = kwargs["_id"]
        self.title = kwargs["title"]
        self.description = kwargs["description"]

        self.is_completed = kwargs["is_completed"]
        self.updated_at = kwargs["updated_at"]
        self.created_at = kwargs["created_at"]


class todoList(Document):

    title = StringField()
    description = StringField()
    is_completed = BooleanField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    def create(
        self,
        title: str,
        description: str,
        is_completed: bool = False,
        created_at: datetime = None,
        updated_at: datetime = datetime.now(),
    ) -> "todoList":

        self.title = title
        self.description = description

        self.is_completed = is_completed
        self.updated_at = updated_at

        if created_at:
            self.created_at = created_at

        return self


@app.route("/todoList", methods=["GET", "POST", "PUT"])
@app.route("/todoList/<string:oid>", methods=["DELETE"])
def index(oid=None):

    if oid == None:

        if request.method == "GET":

            todo_list = todoList.objects()

            if len(todo_list) < 1:
                return ""

            all_objects = []
            for object in todo_list.order_by("-id"):

                todo = todoObject(
                    _id=str(object.id),
                    title=object.title,
                    description=object.description,
                    is_completed=object.is_completed,
                    created_at=object.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
                    updated_at=object.updated_at.strftime("%m/%d/%Y, %H:%M:%S"),
                )
                all_objects.append(todo.__dict__)

            return json.dumps(all_objects)

        elif request.method == "POST":

            data = request.get_json()

            new_todo = todoList().create(
                title=data["title"],
                description=data["description"],
                created_at=datetime.now(),
            )
            new_todo.save()

            return jsonify(success="OK")

        elif request.method == "PUT":

            data = request.get_json()
            oid = data["_id"]

            object = todoList.objects(id=oid).first()

            if not object:
                return jsonify(success="FAIL")

            object.is_completed = True
            object.updated_at = datetime.now()
            object.save()

            return jsonify(success="OK")

    else:
        if request.method == "DELETE":

            object = todoList.objects(id=oid).first()

            if not object:
                return jsonify(success="FAIL")

            object.delete()
            return jsonify(success="OK")


if __name__ == "__main__":
    app.run(port=5005, debug=True)
