import flask as f
import functions as fc
from werkzeug.security import check_password_hash

app = f.Flask(__name__)
app.secret_key = "!yd7fzaJN3Cuj22!%t5Atx&qt2n9vAGHsxa7QU%zwxB!H$N#W&"

#INDEX
@app.route('/')
def index():
    return f.render_template("index.html")

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if f.request.method == 'POST':
        ra = f.request.form['ra']
        senha = f.request.form['senha']
        
        aluno = fc.user_db.find(ra, identifier_key="ra")
        if aluno and check_password_hash(aluno['senha'], senha):
            f.session['user_id'] = aluno['user_id']
            f.session['ra'] = aluno['ra']
            f.session['nome'] = aluno['nome']
            f.session['logged_in'] = True
            return f.redirect(f.url_for('index'))
        return "RA ou senha inválidos", 401
    
    return f.render_template('login.html')

@app.route("/logout")
def logout():
    f.session.clear() 
    return f.redirect(f.url_for('login'))

#usuarios
@app.route("/cadastro_usuarios", methods=["GET", "POST"])
def cadastro_usuarios():
    if f.request.method == "GET":
        return f.render_template("Cadastros de alunos.html")
    if f.request.method == "POST":
            fc.new_usuario()
            return f.redirect(f.url_for('cadastro_usuarios'))
            
@app.route("/consulta_usuarios", methods=["GET", "POST"])
def consulta_usuarios():
    data = fc.user_db.read()
    return f.render_template("consulta_usuarios.html", data=data)

@app.route("/delete_usuario", methods=["POST"])
def delete_usuario():
    user_id = f.request.form["user_id"]
    fc.user_db.delete(user_id)
    return f.redirect(f.url_for('consulta_usuarios'))

#atestados
@app.route("/cadastro_atestados", methods=["GET", "POST"])
def cadastro_atestados():
    if f.request.method == "GET":
        return f.render_template("Envio de atestados.html")
    if f.request.method == "POST":
            fc.new_atestado()
            return f.redirect(f.url_for('cadastro_atestados'))

@app.route("/consulta_atestados", methods=["GET", "POST"])
def consulta_atestados():
    data = fc.atestados_db.read()
    return f.render_template("cadastro_atestados.html", data=data)


if __name__ =="__main__":
    app.run(debug=True)