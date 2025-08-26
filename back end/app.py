import os
from flask import Flask, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from src.db_connection.connection import create_tables, get_db_connection, execute_query
from src.controllers.avaliacoes.index import avaliacoes_blueprint
from src.controllers.students.index import users_blueprint
from src.controllers.reports.index import reports_bp
from src.controllers.professors.index import professors_blueprint
from src.controllers.classes.index import classes_blueprint, get_classes_controller
from src.controllers.departamentos.index import departamento_blueprint
from src.controllers.disciplines.index import disciplinas_blueprint
from views import create_denuncias_views, views_denuncias
from views import create_views, views_bp
from procedures import create_procedures, procedures_bp

app = Flask(__name__, static_folder='src/static')
load_dotenv()
CORS(app)

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
app.register_blueprint(reports_bp)
app.register_blueprint(professors_blueprint)
app.register_blueprint(classes_blueprint)
app.register_blueprint(departamento_blueprint)
app.register_blueprint(views_bp)
app.register_blueprint(views_denuncias)
app.register_blueprint(procedures_bp)
app.register_blueprint(disciplinas_blueprint)

app.jinja_loader.searchpath.insert(0, os.path.join(os.path.dirname(__file__), 'src/templates'))

def add_turmas_indexes():
    sql_file = os.path.join(os.path.dirname(__file__), 'src', 'SQL', 'add_turmas_indexes.sql')
    with open(sql_file, 'r') as file:
        query = file.read()
    execute_query(query)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login')
def login_template():
    return render_template('login.html')

@app.route('/users/register')
def register():
    return render_template('register.html')

@app.route('/turmas')
def turmas():
    classes = get_classes_controller()
    return render_template('turmas.html', turmas=classes)

if __name__ == '__main__':
    create_procedures()
    create_tables()
    create_views()
    add_turmas_indexes()
    create_denuncias_views()
    create_procedures()
    conn = get_db_connection()
    cursor = conn.cursor()
    create_procedures()
    cursor.close()
    conn.close()
    
    app.run(debug=True)
