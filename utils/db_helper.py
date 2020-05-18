import datetime
import os
from typing import Dict, Union, List

from google.cloud import datastore
from google.cloud.datastore import Entity

if os.environ.get("GAE_INSTANCE", None):
    datastore_client = datastore.Client()
else:
    datastore_client = datastore.Client.from_service_account_json(
        "todo-project-1537205581143-7425ee1309dd.json"
    )


DATASTORE_KIND = "Todo"


def get_all_todos() -> List[Dict]:
    """
    Function helper to retrieve all `todo` records from datastore
    Returns:
        List of dictionaries (Entities objects)

    """
    query = datastore_client.query(kind=DATASTORE_KIND).fetch()
    todos_with_ids = [{**dict(todo), "id": todo.id} for todo in query]
    return todos_with_ids


def add_todo(title: str, done: bool, created: datetime) -> Dict:
    """
    Function allows to add new todo to the database
    Args:
        title: entity title
        done: boolean indicator (completed/not completed)
        created: datetime of todo creation

    Returns:
        Added object as dict

    """
    data = dict(title=title, done=done, created=created)
    key = datastore_client.key(DATASTORE_KIND)
    entity = datastore.Entity(key)
    entity.update(data)
    datastore_client.put(entity)
    new_object = {**dict(entity), "id": entity.id}
    return new_object


def update_todo_completed(todo_id: int, done: bool) -> Dict:
    """
    Function allows to update status of todo
    Args:
        todo_id: target todo id
        done: boolean indicator (completed/not completed)

    Returns:
        Updated object as dict

    """
    key = datastore_client.key(DATASTORE_KIND, todo_id)
    existing_todo = datastore_client.get(key)
    existing_todo["done"] = done
    datastore_client.put(existing_todo)
    return dict(existing_todo)


def delete_todo(todo_id: int) -> None:
    """
    Function to remove todo entity from database
    Args:
        todo_id: target todo id

    Returns:
        None

    """

    key = datastore_client.key(DATASTORE_KIND, todo_id)
    datastore_client.delete(key)
    return


def check_todo_exist(todo_id: int) -> Union[None, Dict]:
    """
    Function allows to check if entity exists in database
    Args:
        todo_id: target todo id

    Returns:
        Entity object as dict or None

    """
    key = datastore_client.key(DATASTORE_KIND, todo_id)
    existing_todo = datastore_client.get(key)
    return dict(**existing_todo) if existing_todo else None
