from flask import Blueprint, render_template, request, redirect, url_for, Flask
import csv
import os


l = [i.split('.')[0] for i in os.listdir("./data")]
tasks_bp = Blueprint('tasks', __name__)


def read_tasks(fname):
    tasks_Suki = []
    tasks_Suj = []
    with open(fname, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['person'] == 'Suki':
                tasks_Suki.append([row['task'], row['complete']])
            elif row['person'] == 'Suj':
                tasks_Suj.append([row['task'], row['complete']])
    return tasks_Suki, tasks_Suj

def write_tasks(fname, tasks_Suki, tasks_Suj):
    with open(fname, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['person', 'task', 'complete'])
        for task in tasks_Suki:
            writer.writerow(['Suki', task[0], task[1]])
        for task in tasks_Suj:
            writer.writerow(['Suj', task[0], task[1]])

@tasks_bp.route("/", methods=["GET", "POST"])
def index():
    tasks_Suki, tasks_Suj = read_tasks("tasks.csv")

    # Adding a task
    if request.method == "POST":
        person = request.form.get("person")
        task = request.form.get("task")
        if person == "Suki":
            tasks_Suki.append([task, ""])
        elif person == "Suj":
            tasks_Suj.append([task, ""])
        write_tasks("tasks.csv", tasks_Suki, tasks_Suj)
        return redirect(url_for('tasks.index'))

    return render_template("index.html",
                           tasks_Suki=tasks_Suki,
                           tasks_Suj=tasks_Suj)

# @tasks_bp.route("/hellothere", methods=["GET", "POST"])
# def wat():
#     if request.method == "POST":
#         print(request.form.get("wat"))
#     return "hello"

@tasks_bp.route("/complete/<person>/<int:task_id>")
def complete_task(person, task_id):
    tasks_Suki, tasks_Suj = read_tasks("tasks.csv")

    if person == "Suki":
        if 0 <= task_id < len(tasks_Suki):
            if tasks_Suki[task_id][1] == "":
                tasks_Suki[task_id][1] = "checked"
            elif tasks_Suki[task_id][1] == "checked":
                tasks_Suki[task_id][1] = ""
    elif person == "Suj":
        if 0 <= task_id < len(tasks_Suj):
            if tasks_Suj[task_id][1] == "":
                tasks_Suj[task_id][1] = "checked"
            elif tasks_Suj[task_id][1] == "checked":
                tasks_Suj[task_id][1] = ""

    write_tasks("tasks.csv", tasks_Suki, tasks_Suj)
    return redirect(url_for('tasks.index'))

@tasks_bp.route("/delete/<person>/<int:task_id>")
def delete_task(person, task_id):
    tasks_Suki, tasks_Suj = read_tasks("tasks.csv")

    if person == "Suki":
        if 0 <= task_id < len(tasks_Suki):
            tasks_Suki.pop(task_id)
    elif person == "Suj":
        if 0 <= task_id < len(tasks_Suj):
            tasks_Suj.pop(task_id)

    write_tasks("tasks.csv", tasks_Suki, tasks_Suj)
    return redirect(url_for('tasks.index'))

