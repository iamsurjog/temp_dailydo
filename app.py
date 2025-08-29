from flask import Flask
from tasks_blueprint.routes import tasks_bp
import os

def create_app():
    app = Flask(__name__)
    app.register_blueprint(tasks_bp)

    # Create CSV if not exists
    if not os.path.exists("tasks.csv"):
        with open("tasks.csv", "w") as f:
            f.write("person,task\n")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

