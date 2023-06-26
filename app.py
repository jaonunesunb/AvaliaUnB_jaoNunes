from flask import Flask
import os
from dotenv import load_dotenv
from db_connection.connection import create_tables
from controllers.comments.index import comments_blueprint
from controllers.students.index import users_blueprint

app = Flask(__name__)
load_dotenv()

app.config['DATABASE'] = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

app.register_blueprint(users_blueprint)
app.register_blueprint(comments_blueprint)

if __name__ == '__main__':
    create_tables() 
    app.run(debug=True)
