#CLI application
# store tasks in json file
# User:
#--add
#--mark task (in progress) or done
#--list all tasks
#--list all completed tasks
#--list all in protgress
#--list all not started
from datetime import datetime
import json
from os import path
import sys
import argparse





def add(database, description) -> None:

    id = str(max(map(int,database.keys()),default=0)+1)
    today=datetime.now().strftime("%d %m %Y %H %M %S")
    database[id] = {
        "description": description,
        "status":"todo",
        "createdAt":today,
        "updatedAt":today
    }

    return list_task(id,database[id])

def list_task(id,data):
    #prepei na einai se morphy pinaka, pio meta omws
    print(f"id:{id} | {data}")

def mark():
    pass

def list_all_tasks():
    pass

def list_all_completed_tasks():
    pass

def list_in_progress():
    pass

def list_not_completed():
    pass

#for the json file
def save(database_path,data):
    with open("database_path","w") as f:
        json.dump(data,f)

def load(database_path):
    try:
        with open("database_path","r") as f:
            tasks= json.load(f)
            return tasks
    except FileNotFoundError:
        return {}


# def _arg_parse_conf() -> argparse.ArgumentParser :
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-db", default="~/tasker.json",help="Database path.")
#     parser.add_argument("add",help="Adds an item to the database")
#


def main():

    pass



if __name__=="__main__":
    main()
