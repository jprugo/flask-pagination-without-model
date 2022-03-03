from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from handlers.routes import configure_routes

from utils import get_connection_data

app = Flask(__name__)
conn_data = get_connection_data("secreto")

# dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{user}:{password}@{host}:{port}/{database}"\
    .format(*conn_data, **conn_data)

db = SQLAlchemy(app)

configure_routes(app, db)

if __name__ == '__main__':
    app.run(debug=True)