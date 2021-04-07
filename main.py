import json
from random import randrange, choice
from typing import Optional

import requests

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from random_word import RandomWords
from settings import KEY, TOKEN, ID_BOARD, ID_LIST


app = FastAPI()


class Task(BaseModel):
    type: str
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None


@app.post("/")
def create_task(task: Task):
    if task.type == 'issue':
        return create_issue_card(task)
    if task.type == 'bug':
        return create_bug_card(task)
    if task.type == 'task':
        return create_task_card(task)
    raise HTTPException(status_code=400, detail="The task type is not valid or is missing")


def create_issue_card(task):
    if task.title and task.description:
        return add_card_to_list(task)
    raise HTTPException(status_code=400, detail="The issue should have a title and a description")


def create_bug_card(task):
    if not task.description:
        raise HTTPException(status_code=400, detail="The bug should have a description")
    task.title = get_bug_title()
    members_list = get_board_members()
    member_id = get_random_board_member_id(members_list)
    label_id = get_or_create_label(task.type)['id']
    return add_card_to_list(task, member_id, label_id)


def create_task_card(task):
    if not task.title or not task.category:
        raise HTTPException(status_code=400, detail="The task should have a title and a category")
    label_id = get_or_create_label(task.category)['id']
    return add_card_to_list(task, label_id=label_id)


def get_bug_title():
    word = RandomWords().get_random_word()
    number = str(randrange(10000))
    return 'bug-' + word + '-' + number


def get_or_create_label(name):
    labels = get_board_labels()
    for label in labels:
        if label['name'] == name:
            return label
    return create_board_label(name)


def get_random_board_member_id(members_list):
    return choice(members_list)['id']


def get_board_members():
    url = "https://api.trello.com/1/boards/" + ID_BOARD + "/members"
    response = requests.request(
        "GET",
        url,
        params={
            'key': KEY,
            'token': TOKEN
        }
    )
    return json.loads(response.text)


def get_board_labels():
    url = "https://api.trello.com/1/boards/" + ID_BOARD + "/labels"
    response = requests.request(
        "GET",
        url,
        params={
            'key': KEY,
            'token': TOKEN
        }
    )
    return json.loads(response.text)


def create_board_label(name):
    url = "https://api.trello.com/1/boards/" + ID_BOARD + "/labels"
    response = requests.request(
        "POST",
        url,
        params={
            'key': KEY,
            'token': TOKEN,
            'name': name,
            'color': None
        }
    )
    return json.loads(response.text)


def add_card_to_list(task, member_id=None, label_id=None):
    url = "https://api.trello.com/1/cards/"
    response = requests.request(
        "POST",
        url,
        params={
            'key': KEY,
            'token': TOKEN,
            'idList': ID_LIST,
            'name': task.title,
            'desc': task.description,
            'idMembers': [member_id],
            'idLabels': [label_id]
        }
    )
    return json.loads(response.text)
