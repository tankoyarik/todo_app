import json

from flask import Flask, request, jsonify, render_template
from marshmallow import ValidationError

from utils.db_helper import (
    add_todo,
    delete_todo,
    check_todo_exist,
    get_all_todos,
    update_todo_completed,
)
from utils.validators import Todo

app = Flask(__name__)

from datetime import datetime


@app.route("/")
def get_todos():
    todos = get_all_todos()
    return render_template("index.html", todos=enumerate(todos))


# endpoint to add todo item
@app.route("/add-todo", methods=["POST"])
def addTodo():
    data = json.loads(request.data)
    try:
        result = Todo().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    new_todo = add_todo(**result, created=datetime.now())
    return jsonify(new_todo), 201


# endpoint for deleting todo item
@app.route("/delete-todo/<int:item_id>", methods=["DELETE"])
def removeTodo(item_id):
    if not check_todo_exist(item_id):
        return jsonify("Doesn't exist"), 404
    delete_todo(item_id)
    return jsonify("Item removed"), 204


# endpoint for updating todo item
@app.route("/update-todo/<int:item_id>", methods=["PATCH"])
def updateTodo(item_id):
    payload = json.loads(request.data)
    if not check_todo_exist(item_id):
        return jsonify("Doesn't exist"), 404
    update_todo_completed(todo_id=item_id, done=payload.get("completed"))
    return jsonify(item_id), 200


if __name__ == "__main__":
    app.run()
