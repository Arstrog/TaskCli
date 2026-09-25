#CLI application
# store tasks in json file
# User:
#--add
# --delete
# update
#--mark task (in progress) or done
#--list all tasks
#--list all completed tasks
#--list all in protgress
#--list all not started
from datetime import datetime
import json
import os
import sys
import argparse



def add(args,database) -> None:

    id = str(max(map(int,database.keys()),default=0)+1)
    today=datetime.now().strftime("%d-%m-%Y:%H:%M:%S")
    database[id] = {
        "description": args.description,
        "status":"todo",
        "createdAt":today,
        "updatedAt":today
    }
    #for now:
    print(f"Task added successfully (Id: {id})")

def update(args,database,status=None):
    #args needed are id and description
    id = str(args.id)
    description = str(args.description)
    status = str(args.status)
    if status is not None:
        database[id]["status"]=status
    if id in database:
        database[id]["description"]=description
        database[id]["updatedAt"]=datetime.now().strftime("%d-%m-%Y:%H:%M:%S")


def delete(args,database):
    id = str(args.id)
    if int(id)<=0 or (id not in database):
        sys.exit(f"Task with id:{id} does not exist.")
    database.pop(id)

def mark_in_progress(args,database):
    update(args,database,status="in-progress")

def mark_done(args,database):
    update(args,database,status="done")

def list_task(args,database):
    #List all tasks
    if args.status is None:
        print ("{:<8} {:<30} {:<10} {:<20} {:<15}".format('Id','description','status','createdAt','updatedAt'))
        for id ,data in database.items():
            vals=data.values()
            des,stat,create,update = vals
            print(f"{id:<8} {des:<30} {stat:<10} {create:<20} {update:<15}")

    #Listing tasks based only on status
    print ("{:<8} {:<30} {:<10} {:<20} {:<15}".format('Id','description','status','createdAt','updatedAt'))
    for id ,data in database.items():
        vals=data.values()
        des,stat,create,update = vals
        if stat==str(args.status):
            print(f"{id:<8} {des:<30} {stat:<10} {create:<20} {update:<15}")


#File handling
def save(database_path,data):
    with open(database_path,"w") as f:
        json.dump(data,f)

def load(database_path):
    try:
        with open(database_path,"r") as f:
            tasks= json.load(f)
            return tasks
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {}


def _arg_parse_conf() -> argparse.ArgumentParser :
    parser = argparse.ArgumentParser(prog="tasker")
    subparsers = parser.add_subparsers(dest="commands",required=True)
    #database path
    parser.add_argument("--db",dest="filename",help="Specify database location.",default="tasker.json")
    #add method
    parse_add = subparsers.add_parser("add",help="Add a new task.")
    parse_add.add_argument("description",type=str)
    parse_add.set_defaults(func=add)

    #update
    parse_update = subparsers.add_parser("update",help="Update the description of a task.")
    parse_update.add_argument("id",type=int)
    parse_update.add_argument("description",type=str)
    # parse_update.add_argument("status",nargs="?",choices=["todo","in-progress","done"],default=None)
    parse_update.set_defaults(func=update)

    #delete
    parse_delete = subparsers.add_parser("delete",help="Delete a task with the given id.")
    parse_delete.add_argument("id",type=int)
    parse_delete.set_defaults(func=delete)

    #mark
    parent_mark = argparse.ArgumentParser(add_help=False)
    parent_mark.add_argument("id",type=int,help="Task id.")
    parse_mark_done = subparsers.add_parser("mark-done",help="Mark the status of the current task as done.",parents=[parent_mark])
    parse_mark_done.set_defaults(func=mark_done)
    parse_mark_progress = subparsers.add_parser("mark-in-progress",help="Mark the status of the current task as in-progress.",parents=[parent_mark])
    parse_mark_progress.set_defaults(func=mark_in_progress)

    #list
    parse_list=subparsers.add_parser("list",help="List all tasks.")
    parse_list.add_argument("status",nargs="?",choices=["todo","in-progress","done"],default=None)
    parse_list.set_defaults(func=list_task)

    return parser








def main():
    db = load("tests.json")
    parser = _arg_parse_conf()
    args=parser.parse_args()
    args.func(args,db)
    save("tests.json",db)





if __name__=="__main__":
    sys.exit(main())
