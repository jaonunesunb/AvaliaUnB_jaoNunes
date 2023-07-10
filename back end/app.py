from flask import Flask, redirect, request, session
import os
from dotenv import load_dotenv
from src.db_connection.connection import create_tables
from src.controllers.avaliacoes.index import avaliacoes_blueprint
from src.controllers.students.index import users_blueprint
from src.controllers.reports.index import denuncias_bp
from src.controllers.professors.index import professors_blueprint

app = Flask(__name__)
load_dotenv()

app.config['DATABASE'] = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

app.secret_key = os.getenv('SECRET_KEY')  

app.register_blueprint(users_blueprint)
app.register_blueprint(avaliacoes_blueprint)
app.register_blueprint(denuncias_bp)
app.register_blueprint(professors_blueprint)

if __name__ == '__main__':
    create_tables() 
    app.run(debug=True)
