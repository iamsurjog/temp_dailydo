from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import csv
import os

tasks_bp = Blueprint('tasks', __name__)

def get_themes():
    themes = []
    with open('themes.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            themes.append(row)
    return themes

def get_csv_file_path(category):
    return os.path.join('path', f"{category}.csv")

def read_tasks(category):
    tasks = {}
    csv_file = get_csv_file_path(category)
    if not os.path.exists(csv_file):
        return None
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            person = row['person']
            if person not in tasks:
                tasks[person] = []
            tasks[person].append([row['task'], row.get('complete', '')])
    return tasks

def write_tasks(category, tasks):
    csv_file = get_csv_file_path(category)
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['person', 'task', 'complete'])
        for person, task_list in tasks.items():
            for task in task_list:
                writer.writerow([person, task[0], task[1]])

@tasks_bp.route("/<category>")
def index(category):
    selected_theme = request.cookies.get('theme', 'default')
    themes = get_themes()
    theme_data = next((theme for theme in themes if theme['theme_name'] == selected_theme), themes[0])

    tasks = read_tasks(category)
    if tasks is None:
        return "Category not found", 404
    persons = list(tasks.keys())
    return render_template("index.html", tasks=tasks, persons=persons, blueprint_name=category, theme=theme_data)

@tasks_bp.route("/<category>/add", methods=["POST"])
def add_task(category):
    tasks = read_tasks(category)
    if tasks is None:
        return "Category not found", 404
    person = request.form.get("person")
    task = request.form.get("task")
    if person not in tasks:
        tasks[person] = []
    tasks[person].append([task, ""])
    write_tasks(category, tasks)
    return redirect(url_for('tasks.index', category=category))

@tasks_bp.route("/<category>/complete/<person>/<int:task_id>")
def complete_task(category, person, task_id):
    tasks = read_tasks(category)
    if tasks is None:
        return "Category not found", 404
    if person in tasks and 0 <= task_id < len(tasks[person]):
        if tasks[person][task_id][1] == "":
            tasks[person][task_id][1] = "checked"
        else:
            tasks[person][task_id][1] = ""
        write_tasks(category, tasks)
    return redirect(url_for('tasks.index', category=category))

@tasks_bp.route("/<category>/delete/<person>/<int:task_id>")
def delete_task(category, person, task_id):
    tasks = read_tasks(category)
    if tasks is None:
        return "Category not found", 404
    if person in tasks and 0 <= task_id < len(tasks[person]):
        tasks[person].pop(task_id)
        write_tasks(category, tasks)
    return redirect(url_for('tasks.index', category=category))

@tasks_bp.route('/<category>/reorder', methods=['POST'])
def reorder_tasks(category):
    data = request.get_json()
    person = data['person']
    new_order = [int(i) for i in data['newOrder']]

    tasks = read_tasks(category)
    if tasks is None:
        return jsonify({'success': False, 'message': 'Category not found'}), 404

    if person in tasks:
        original_tasks = tasks[person]
        reordered_tasks = [original_tasks[i] for i in new_order]
        tasks[person] = reordered_tasks
        write_tasks(category, tasks)
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'message': 'Person not found'}), 404
