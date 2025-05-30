from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(min_level=3):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('logged_in'):
                flash('Por favor, faça login para acessar esta página.', 'warning')
                return redirect(url_for('login'))
            
            if session.get('tipo') != 'administrador':
                flash('Acesso restrito a administradores.', 'danger')
                return redirect(url_for('index'))
            
            user_level = int(session.get('nivel_acesso', 3))
            if user_level > min_level:
                flash('Você não tem permissão suficiente para acessar esta página.', 'danger')
                return redirect(url_for('index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        if session.get('tipo') != 'aluno':
            flash('Acesso restrito a alunos.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function