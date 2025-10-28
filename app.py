from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from tasks_blueprint.routes import tasks_bp
import os
import csv

app = Flask(__name__)

path_dir = 'path'
if not os.path.exists(path_dir):
    os.makedirs(path_dir)


CATEGORY_ORDER_FILE = 'category_order.txt'

def get_themes():
    themes = []
    with open('themes.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            themes.append(row)
    return themes

def get_category_order():
    if not os.path.exists(CATEGORY_ORDER_FILE):
        csv_files = [f.replace('.csv', '') for f in os.listdir(path_dir) if f.endswith('.csv')]
        with open(CATEGORY_ORDER_FILE, 'w') as f:
            for category in csv_files:
                f.write(f'{category}\n')
        return csv_files
    with open(CATEGORY_ORDER_FILE, 'r') as f:
        return [line.strip() for line in f.readlines()]

def set_category_order(order):
    with open(CATEGORY_ORDER_FILE, 'w') as f:
        for category in order:
            f.write(f'{category}\n')

app.register_blueprint(tasks_bp, url_prefix='/tasks')

@app.route('/', methods=["GET", "POST"])
def home():
    selected_theme = request.cookies.get('theme', 'default')
    themes = get_themes()
    theme_data = next((theme for theme in themes if theme['theme_name'] == selected_theme), themes[0])

    if request.method == "POST":
        category = request.form.get("category")
        f = open("./path/" + category + ".csv", 'w')
        writer = csv.writer(f)
        writer.writerow(['person', 'task', 'complete'])
        f.close()
        order = get_category_order()
        order.append(category)
        set_category_order(order)
        return redirect(url_for('tasks.index', category=category))
        
    ordered_categories = get_category_order()
    csv_files = [f'{c}.csv' for c in ordered_categories]
    return render_template('home.html', csv_files=csv_files, theme=theme_data)

@app.route('/remove_category/<category>')
def remove_category(category):
    os.remove(os.path.join(path_dir, f'{category}.csv'))
    order = get_category_order()
    if category in order:
        order.remove(category)
        set_category_order(order)
    return redirect(url_for('home'))

@app.route('/reorder_categories', methods=['POST'])
def reorder_categories():
    data = request.get_json()
    new_order = data['newOrder']
    set_category_order(new_order)
    return jsonify({'success': True})

@app.route('/settings', methods=["GET", "POST"])
def settings():
    themes = get_themes()
    selected_theme = request.cookies.get('theme', 'default')

    if request.method == "POST":
        selected_theme = request.form.get('theme')
        resp = make_response(redirect(url_for('settings')))
        resp.set_cookie('theme', selected_theme)
        return resp

    theme_data = next((theme for theme in themes if theme['theme_name'] == selected_theme), themes[0])
    return render_template('settings.html', themes=themes, selected_theme=selected_theme, theme=theme_data)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
