import json
import os

DATA_FILE = "data/task_data.json"


class Task():
    def __init__(self):
        pass

def create_file_if_not_exists():
    if not os.path.exists(DATA_FILE):
        print("Can't find data file. Creating new.")
        with open(DATA_FILE, "w", encoding='utf-8') as file:
            pass

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("JSON file error.")
        return []

def save_data(tasks):
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

def add_new_task(task_content):
    task_list = load_data()
    if (len(task_list) == 0):
        new_id = 1
    else:
        new_id = task_list[-1]["id"] + 1
    new_task = {
        "id" : new_id,
        "category": "null",
        'content' : task_content
        }
    
    task_list.append(new_task)
    
    save_data(task_list)

def delete_task(id):
    task_list = load_data()
    index = 0
    for task in task_list:
        index += 1
        if task['id'] == id:
            task_list.pop(index-1)
    save_data(task_list)

    
