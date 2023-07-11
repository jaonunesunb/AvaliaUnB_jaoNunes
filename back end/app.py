import os
from flask import Flask
from dotenv import load_dotenv
from src.db_connection.connection import create_tables, get_db_connection
from src.controllers.avaliacoes.index import avaliacoes_blueprint
from src.controllers.students.index import users_blueprint
from src.controllers.reports.index import reports_bp
from src.controllers.professors.index import professors_blueprint
from src.controllers.classes.index import classes_blueprint
from src.controllers.departamentos.index import departamento_blueprint
from views import create_views, views_bp
from src.procedures.index import procedures_bp

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
app.register_blueprint(reports_bp)
app.register_blueprint(professors_blueprint)
app.register_blueprint(classes_blueprint)
app.register_blueprint(departamento_blueprint)
app.register_blueprint(views_bp)
app.register_blueprint(procedures_bp)

if __name__ == '__main__':
    create_tables()
    create_views()
    app.run(debug=True)

