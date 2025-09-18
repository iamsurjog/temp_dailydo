from flask import Flask, render_template
from tasks_blueprint.routes import create_tasks_blueprint
import os

app = Flask(__name__)

path_dir = 'path'
if not os.path.exists(path_dir):
    os.makedirs(path_dir)

for csv_file in os.listdir(path_dir):
    if csv_file.endswith('.csv'):
        blueprint_name = os.path.splitext(csv_file)[0]
        tasks_bp = create_tasks_blueprint(blueprint_name, os.path.join(path_dir, csv_file))
        app.register_blueprint(tasks_bp, url_prefix=f'/{blueprint_name}')

@app.route('/')
def home():
    path_dir = 'path'
    csv_files = [f for f in os.listdir(path_dir) if f.endswith('.csv')]
    return render_template('home.html', csv_files=csv_files)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)