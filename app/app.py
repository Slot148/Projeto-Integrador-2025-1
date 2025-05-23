import os
import flask as f
import functions as fc
# from secret_key import key
from werkzeug.security import check_password_hash, generate_password_hash
from decorators import login_required, admin_required, student_required

key = "jgndglnfgnlfgnfdngkfn"

app = f.Flask(__name__)
app.secret_key = key

#INDEX
@app.route('/')
def index():
        return f.render_template("index.html")

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if f.session.get('logged_in'):
        return f.redirect(f.url_for('index'))
        
    if f.request.method == 'POST':
        username = f.request.form.get('user')
        password = f.request.form.get('senha')
        
        if not username or not password:
            f.flash('Por favor, preencha todos os campos', 'error')
            return f.redirect(f.url_for('login'))
    
        user = None
        user = fc.user_db.find(username, identifier_key="username")
        if not user:
            user = fc.user_db.find(username, identifier_key="ra")
        
        if not user or not check_password_hash(user.get('senha', ''), password):
            f.flash('Credenciais inválidas', 'error')
            return f.redirect(f.url_for('login'))
        
        f.session['user_id'] = user['user_id']
        f.session['nome'] = user['nome']
        f.session['tipo'] = user['tipo']
        f.session['logged_in'] = True
        
        if user['tipo'] == 'aluno':
            f.session['ra'] = user['ra']
            f.session['equipe'] = user['equipe']
            f.session['curso'] = user['curso']
        else:
            if 'username' in user:
                f.session['username'] = user['username']
            if 'nivel_acesso' in user:
                f.session['nivel_acesso'] = user['nivel_acesso']
        
        return f.redirect(f.url_for('index'))
    
    return f.render_template('login.html')

@app.route("/logout")
def logout(): 
    f.session.clear()
    f.session.pop('_flashes', None)
    f.flash('Desconectado com sucesso')
    return f.redirect(f.url_for('index'))

#usuarios
@app.route("/cadastro_usuarios", methods=["GET", "POST"])
@admin_required(min_level=3)
def cadastro_usuarios():
    if f.request.method == "GET":
        data = fc.user_db.read()
        return f.render_template("Cadastros de alunos.html", data=data)
    if f.request.method == "POST":
            fc.new_usuario()
            return f.redirect(f.url_for('cadastro_usuarios'))
            
@app.route("/consulta_usuarios", methods=["GET", "POST"])
@admin_required(min_level=3)
def consulta_usuarios():
    data = fc.user_db.read()
    return f.render_template("consulta_usuarios.html", data=data)

@app.route("/delete_usuario", methods=["POST"])
@admin_required(min_level=3)
def delete_usuario():
    user_id = f.request.form["user_id"]
    fc.user_db.delete(user_id)
    return f.redirect(f.url_for('consulta_usuarios'))

#atestados
@app.route("/cadastro_atestados", methods=["GET", "POST"])
@login_required
def cadastro_atestados():
    if f.request.method == "GET":
        return f.render_template("Envio de atestados.html")
    if f.request.method == "POST":
            fc.new_atestado()
            return f.redirect(f.url_for('cadastro_atestados'))

@app.route("/aluno/consulta_atestados", methods=['GET', 'POST'])
@login_required
def consulta_atestados_aluno():
    if not f.session.get('logged_in'):
        return f.redirect(f.url_for('login'))
    todos_atestados = fc.atestados_db.read()
    atestados_aluno = [atestado for atestado in todos_atestados 
                      if str(atestado.get('ra')) == str(f.session.get('ra'))]
    return f.render_template('atestado_aluno.html', data=atestados_aluno)

@app.route('/consulta_atestado/remover/<atestado_id>', methods=["POST"])
@login_required
def remover_atestado(atestado_id):
    try:
        atestado = fc.atestados_db.find(atestado_id, identifier_key="atestado_id")
        file_path = os.path.abspath(atestado['file_path'].replace('/', os.sep))
        if os.path.exists(file_path):
            os.remove(file_path)
        if fc.atestados_db.delete(atestado_id, identifier_key="atestado_id"):
            return f.redirect(f.url_for('consulta_atestados_aluno'))
        else:
            return "Erro ao remover atestado", 500
            
    except Exception as e:
        print(f"Erro ao remover atestado: {str(e)}")
        return "Erro ao remover atestado", 500
    

@app.route("/consulta_atestados", methods=["GET", "POST"])
@admin_required(min_level=3)
def consulta_atestados():
    data = fc.atestados_db.read()
    return f.render_template("aprovar_atestado.html", data=data)

@app.route('/consulta_atestado/aprovar/<id>', methods=["POST"])
@admin_required(min_level=3)
def aprovar_atestado(id):
    new_data = fc.atestados_db.find(id, identifier_key="atestado_id")
    new_data['estado'] = "aprovado"
    fc.atestados_db.edit(id, new_data, identifier_key="atestado_id")
    return f.redirect(f.url_for("consulta_atestados")) 

@app.route('/consulta_atestado/reprovar/<id>', methods=["POST"])
@admin_required(min_level=3)
def reprovar_atestado(id):
    new_data = fc.atestados_db.find(id, identifier_key="atestado_id")
    new_data['estado'] = "reprovado"
    fc.atestados_db.edit(id, new_data, identifier_key="atestado_id")
    return f.redirect(f.url_for("consulta_atestados")) 

@app.route('/consulta_atestado/view/<atestado_id>')
@login_required
def visualizar_atestado(atestado_id):
    try:
        atestado = fc.atestados_db.find(atestado_id, identifier_key="atestado_id")
        if not atestado:
            return "Atestado não encontrado", 404
        file_path = os.path.abspath(atestado['file_path'].replace('/', os.sep))
        if not file_path.startswith(os.path.abspath("app/data/atestados")):
            return "Localização do arquivo inválida", 403
        if not os.path.exists(file_path):
            return "Arquivo do atestado não encontrado", 404
        return f.send_file(file_path, mimetype='application/pdf')
    except Exception as e:
        print(f"Erro: {str(e)}")
        return "Erro ao visualizar atestado", 500

@app.route('/criar_equipe', methods=['GET', 'POST'])
@admin_required(min_level=3)
def criar_equipe():
    if f.request.method == "GET":
        data = fc.user_db.read()
        return f.render_template("criar_equipe.html", data=data)
    if f.request.method == "POST":
        fc.equipe()
        return f.redirect(f.url_for('criar_equipe'))

@app.route('/avaliar_equipe', methods=['GET', 'POST'])
@login_required
def avaliar_equipe():
    if f.request.method == "GET":
        
        if not f.session.get('equipe'):
            f.flash('Você não está em nenhuma equipe cadastrada', 'error')
            return f.redirect(f.url_for('index'))
        
        equipe = fc.equipes_db.find(f.session['equipe'], "nome_equipe")
        if not equipe:
            f.flash('Equipe não encontrada', 'error')
            return f.redirect(f.url_for('index'))
        
        todos_alunos = fc.user_db.read()
        
        membros_equipe = []
        for aluno in todos_alunos:
            if aluno.get('ra') and aluno['ra'] in equipe.get('membros', []):
                membros_equipe.append({
                    'ra': aluno['ra'],
                    'nome': aluno['nome']
                })

        data = {
            'nome_equipe': equipe['nome_equipe'],
            'membros_completos': membros_equipe
        }
        return f.render_template("Avaliação SCRUM 2.0.html", data=data)
    
    if f.request.method == "POST":
        try:
            fc.avaliar_equipe_post()
            f.flash('Avaliações registradas com sucesso!', 'success')
            return f.redirect(f.url_for('avaliar_equipe'))
        
        except Exception as e:
            print(f"Erro ao processar avaliações: {str(e)}")
            f.flash('Erro ao processar avaliações. Tente novamente.', 'error')
            return f.redirect(f.url_for('avaliar_equipe'))   

@app.route("/gerenciar_equipes", methods=['GET', 'POST'])
@admin_required(min_level=3)
def editar_equipe():
    if f.request.method == "GET":
        equipes = fc.equipes_db.read()
        alunos = fc.user_db.read()
        ra_para_nome = {aluno['ra']: aluno['nome'] for aluno in alunos if aluno.get('ra')}

        for equipe in equipes:
            equipe['membros_nomes'] = [ra_para_nome.get(ra, f"RA {ra} (não encontrado)") for ra in equipe.get('membros', [])]
        return f.render_template("gerenciar_equipes.html", data=equipes, alunos=alunos)

@app.route("/gerar_relatorio", methods=['GET', 'POST'])
@admin_required(min_level=3)
def gerar_relatorio():
    return f.render_template('relatórios_pdf.html')



#PELO AMOR DE DEUS!!! LEMBRAR DE REMOVER O TRECHO ABAIXO ANTES DE PUBLICAR!!!#

def check_default_admin():
    existing_admin = fc.user_db.find("admin", identifier_key="user_id")
    if not existing_admin:
        admin_data = {
            "user_id": "001",
            "username": "admin",
            "nome": "Administrador Padrão",
            "senha": generate_password_hash("admin123"),
            "tipo": "administrador",
            "nivel_acesso": "3"
        }
        fc.user_db.add(admin_data, identifier_key="user_id")
        print("Admin padrão criado com credenciais temporárias")

#PELO AMOR DE DEUS!!! LEMBRAR DE REMOVER O TRECHO ACIMA ANTES DE PUBLICAR!!!#


if __name__ =="__main__":
    #PELO AMOR DE DEUS!!! LEMBRAR DE REMOVER O TRECHO ABAIXO ANTES DE PUBLICAR - (Manter apenas 'app.run()')!!!#
    check_default_admin()
    app.run(debug=True, host="0.0.0.0")