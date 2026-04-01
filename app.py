from flask import Flask
from config import Config
from routes.main_routes import main_routes
from database.db import db
from database.table.user import User


app = Flask(__name__)
app.config.from_object(Config)

# register blueprint
app.register_blueprint(main_routes)

db.init_app(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)