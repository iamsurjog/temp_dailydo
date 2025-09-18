from flask import Blueprint, render_template, request, redirect, url_for
import csv

def create_tasks_blueprint(blueprint_name, csv_file):
    tasks_bp = Blueprint(blueprint_name, __name__)

    def read_tasks(fname):
        tasks = {}
        with open(fname, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                person = row['person']
                if person not in tasks:
                    tasks[person] = []
                tasks[person].append([row['task'], row.get('complete', '')])
        return tasks

    def write_tasks(fname, tasks):
        with open(fname, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['person', 'task', 'complete'])
            for person, task_list in tasks.items():
                for task in task_list:
                    writer.writerow([person, task[0], task[1]])

    @tasks_bp.route("/")
    def index():
        tasks = read_tasks(csv_file)
        persons = list(tasks.keys())
        return render_template("index.html", tasks=tasks, persons=persons, blueprint_name=blueprint_name)

    @tasks_bp.route("/add", methods=["POST"])
    def add_task():
        tasks = read_tasks(csv_file)
        person = request.form.get("person")
        task = request.form.get("task")
        if person not in tasks:
            tasks[person] = []
        tasks[person].append([task, ""])
        write_tasks(csv_file, tasks)
        return redirect(url_for(f'{blueprint_name}.index'))

    @tasks_bp.route("/complete/<person>/<int:task_id>")
    def complete_task(person, task_id):
        tasks = read_tasks(csv_file)
        if person in tasks and 0 <= task_id < len(tasks[person]):
            if tasks[person][task_id][1] == "":
                tasks[person][task_id][1] = "checked"
            else:
                tasks[person][task_id][1] = ""
            write_tasks(csv_file, tasks)
        return redirect(url_for(f'{blueprint_name}.index'))

    @tasks_bp.route("/delete/<person>/<int:task_id>")
    def delete_task(person, task_id):
        tasks = read_tasks(csv_file)
        if person in tasks and 0 <= task_id < len(tasks[person]):
            tasks[person].pop(task_id)
            write_tasks(csv_file, tasks)
        return redirect(url_for(f'{blueprint_name}.index'))

    return tasks_bp