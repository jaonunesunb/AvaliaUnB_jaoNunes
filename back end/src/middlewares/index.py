from functools import wraps
from flask import g, request, jsonify

from flask import  session, redirect, url_for, flash
from functools import wraps

def is_authenticated(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Para acessar essa página, é necessário estar logado.', category='error')
            return redirect('/login')

        return f(*args, **kwargs)
    return wrapper

def check_admin(permission):
    def inner_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if session['is_adm'] != permission:
                flash('Acesso negado. Este recurso requer privilégios de administrador.') 
                return redirect('/')

            return f(*args, **kwargs)
        return wrapper
    return inner_decorator