from flask import Flask, render_template, request, redirect, url_for
from tasks_blueprint.routes import tasks_bp
import os
import csv

app = Flask(__name__)

path_dir = 'path'
if not os.path.exists(path_dir):
    os.makedirs(path_dir)

app.register_blueprint(tasks_bp, url_prefix='/tasks')

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        category = request.form.get("category")
        f = open("./path/" + category + ".csv", 'w')
        writer = csv.writer(f)
        writer.writerow(['person', 'task', 'complete'])
        f.close()
        return redirect(url_for('tasks.index', category=category))
        
    path_dir = 'path'
    csv_files = [f for f in os.listdir(path_dir) if f.endswith('.csv')]
    return render_template('home.html', csv_files=csv_files)

@app.route('/remove_category/<category>')
def remove_category(category):
    os.remove(os.path.join(path_dir, f'{category}.csv'))
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)