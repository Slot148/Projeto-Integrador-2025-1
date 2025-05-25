import os
import flask as f
import functions as fc
import functions2 as fc2
from werkzeug.security import check_password_hash, generate_password_hash
from decorators import login_required, admin_required, student_required
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = f.Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

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

#gerenciar equipes
@app.route('/gerenciar_equipe/criar', methods=['GET', 'POST'])
@admin_required(min_level=3)
def criar_equipe():
    if f.request.method == "GET":
        data = fc.user_db.read()
        return f.render_template("criar_equipe.html", data=data)
    if f.request.method == "POST":
        fc.equipe()
        return f.redirect(f.url_for('gerenciar_equipe'))
    
@app.route("/gerenciar_equipe/deletar/<equipe_id>", methods=['GET'])
@admin_required(min_level=3)
def deletar_equipes(equipe_id):
    equipe = fc.equipes_db.find(equipe_id, "equipe_id")
    if not equipe:
        f.flash('Equipe não encontrada', 'error')
        return f.redirect(f.url_for('gerenciar_equipe'))
    
    for ra_aluno in equipe['membros']:
        aluno = fc.user_db.find(ra_aluno, "ra")
        aluno['equipe'] = "sem equipe"
        aluno['funcao'] = 'none'
        fc.user_db.edit(ra_aluno, aluno, "ra")
    
    fc.equipes_db.delete(equipe_id, "equipe_id")
    f.flash('Equipe deletada com sucesso', 'success')
    return f.redirect(f.url_for('gerenciar_equipe'))

@app.route("/gerenciar_equipe/editar", methods=['GET', 'POST'])
@admin_required(min_level=3)
def editar_equipe():
    equipe_id = f.request.args.get('equipe_id') if f.request.method == "GET" else f.request.form.get('equipe_id')
    
    if not equipe_id:
        f.flash('ID da equipe não fornecido', 'error')
        return f.redirect(f.url_for('gerenciar_equipe'))
    
    if f.request.method == "GET":
        equipe = fc.equipes_db.find(equipe_id, "equipe_id")
        if not equipe:
            f.flash('Equipe não encontrada', 'error')
            return f.redirect(f.url_for('gerenciar_equipe'))
        
        alunos = {}
        for ra in equipe['membros']:
            aluno = fc.user_db.find(ra, "ra")
            alunos[aluno['ra']] = {
                'nome': aluno['nome'],
                'funcao': aluno.get('funcao', 'devteam')
            }
        
        return f.render_template("editar_equipe.html", equipe=equipe, alunos=alunos)
    
    if f.request.method == "POST":
        equipe = fc.equipes_db.find(equipe_id, "equipe_id")
        if not equipe:
            f.flash('Equipe não encontrada', 'error')
            return f.redirect(f.url_for('gerenciar_equipe'))
        
        membros_remover = f.request.form.getlist('remover_membro')
        for ra in membros_remover:
            if ra in equipe['membros']:
                equipe['membros'].remove(ra)
                aluno = fc.user_db.find(ra, "ra")
                if aluno:
                    aluno['equipe'] = "sem equipe"
                    fc.user_db.edit(ra, aluno, "ra")
        
        for ra in equipe['membros']:
            funcao = f.request.form.get(f'funcao_{ra}')
            if funcao:
                aluno = fc.user_db.find(ra, "ra")
                if aluno:
                    aluno['funcao'] = funcao
                    fc.user_db.edit(ra, aluno, "ra")
        
        if fc.equipes_db.edit(equipe_id, equipe, "equipe_id"):
            f.flash('Equipe atualizada com sucesso', 'success')
        else:
            f.flash('Erro ao atualizar equipe', 'error')
        
        return f.redirect(f.url_for('gerenciar_equipe'))

@app.route("/gerenciar_equipes", methods=['GET', 'POST'])
@admin_required(min_level=3)
def gerenciar_equipe():
    if f.request.method == "GET":
        equipes = fc.equipes_db.read()
        alunos = fc.user_db.read()
        ra_para_nome = {aluno['ra']: aluno['nome'] for aluno in alunos if aluno.get('ra')}

        for equipe in equipes:
            equipe['membros_nomes'] = [ra_para_nome.get(ra, f"RA {ra} (não encontrado)") for ra in equipe.get('membros', [])]
        return f.render_template("gerenciar_equipes.html", data=equipes, alunos=alunos)
    
#avaliação
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
            return f.redirect(f.url_for('index'))
        
        except Exception as e:
            print(f"Erro ao processar avaliações: {str(e)}")
            f.flash('Erro ao processar avaliações. Tente novamente.', 'error')
            return f.redirect(f.url_for('avaliar_equipe'))   

#relatorio
@app.route('/relatorio_avaliacoes_csv', methods=['GET', 'POST'])
@admin_required(min_level=3)
def relatorio_avaliacoes_csv():

    equipes = fc.equipes_db.read()
    equipes_list = {equipe['equipe_id']: equipe['nome_equipe'] for equipe in equipes if equipe.get('nome_equipe')}
    
    if f.request.method == 'POST':
        filtros = {
            'equipe': f.request.form.get("equipe"),
            'periodo': f.request.form.get("periodo"),
            'curso': f.request.form.get("curso"),
            'semestre': f.request.form.get("semestre"),
            'sprint': f.request.form.get("sprint"),
            'data_inicio': f.request.form.get("data_inicio_avaliacao"),
            'data_fim': f.request.form.get("data_fim_avaliacao"),
            'min_media': f.request.form.get("min_media"), 
            'max_media': f.request.form.get("max_media")   
        }
        

        all_data = fc.avaliacoes_db.read()
        all_users = fc.user_db.read()
        
        users_by_ra = {user.get('ra'): user for user in all_users if user.get('ra')}
        
        filtered_data = []
        for item in all_data:
            aluno = users_by_ra.get(item.get("ra_aluno"))
            if not aluno:
                continue
                
            match = True

            if filtros['equipe'] and aluno.get('equipe', '').lower() != filtros['equipe'].lower():
                match = False

            if filtros['curso'] and aluno.get('curso', '').lower() != filtros['curso'].lower():
                match = False
            
            if filtros['periodo'] and aluno.get('turno', '').lower() != filtros['periodo'].lower():
                match = False

            if filtros['semestre'] and aluno.get('semestre', '').lower() != filtros['semestre'].lower():
                match = False

            data_avaliacao = item.get('data_avaliacao', '')
            if filtros['sprint'] and item.get('sprint', '').lower() != filtros['sprint'].lower():
                match =False
            if filtros['data_inicio'] and data_avaliacao < filtros['data_inicio']:
                match = False
            if filtros['data_fim'] and data_avaliacao > filtros['data_fim']:
                match = False

            if match and (filtros['min_media'] or filtros['max_media']):
                media = (item.get("produtividade", 0) + item.get("autonomia", 0) + 
                        item.get("colaboracao", 0) + item.get("entrega_resultados", 0)) / 4
                
                if filtros['min_media'] and media < float(filtros['min_media']):
                    match = False
                if filtros['max_media'] and media > float(filtros['max_media']):
                    match = False
            
            if match:

                avaliador = users_by_ra.get(item.get("avaliador_ra"))
                
                enriched_item = {
                    **item,
                    "sprint": item.get("sprint"),
                    "nome_aluno": aluno.get("nome", "N/A"),
                    "nome_avaliador": avaliador.get("nome", "N/A") if avaliador else "N/A",
                    "equipe": aluno.get("equipe", "N/A"),
                    "curso": aluno.get("curso", "N/A"),
                    "semestre": aluno.get("semestre", "N/A"),
                    "media": (item.get("produtividade", 0) + item.get("autonomia", 0) + 
                             item.get("colaboracao", 0) + item.get("entrega_resultados", 0)) / 4,
                    "feedback": item.get("feedback")
                }

                filtered_data.append(enriched_item)
        
        data = filtered_data
    else:
        data = fc.avaliacoes_db.read()
        enriched_data = []
        
        for item in data:
            aluno = fc.user_db.find(item.get("ra_aluno"), "ra")
            avaliador = fc.user_db.find(item.get("avaliador_ra"), "ra")
            
            enriched_data.append({
                **item,
                "sprint": item.get("sprint"),
                "nome_aluno": aluno.get("nome", "N/A") if aluno else "N/A",
                "nome_avaliador": avaliador.get("nome", "N/A") if avaliador else "N/A",
                "equipe": aluno.get("equipe", "N/A") if aluno else "N/A",
                "curso": aluno.get("curso", "N/A") if aluno else "N/A",
                "semestre": aluno.get("semestre", "N/A") if aluno else "N/A",
                "media": (item.get("produtividade", 0) + item.get("autonomia", 0) + 
                         item.get("colaboracao", 0) + item.get("entrega_resultados", 0)) / 4,
                "feedback": item.get("feedback")
                
            })
        
        data = enriched_data
        filtros = None
    
    output_dir = os.path.join(BASE_DIR, "data", "relatorios")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "avaliacoes.csv")
    
    success = fc2.gerar_csv_avaliacoes(data, output_path, filtros=filtros)
    
    if success:
        return f.send_file(output_path, as_attachment=True)
    else:
        return "Erro ao gerar relatório de avaliações", 500

@app.route('/relatorio_pdf', methods=['GET','POST'])
@admin_required(min_level=3)
def relatorio_pdf():
    if f.request.method == "GET":
        equipes = fc.equipes_db.read()
        equipes_list = {equipe['equipe_id']: equipe['nome_equipe'] for equipe in equipes if equipe.get('nome_equipe')}
        return f.render_template("relatorio_pdf.html", equipes=equipes_list)
    
    if f.request.method == "POST":
        periodo = f.request.form.get("periodo")
        turma = f.request.form.get("turma")
        semestre = f.request.form.get("Semestre")
        estado = f.request.form.get("estado")
        
        all_atestados = fc.atestados_db.read()
        all_users = fc.user_db.read()
        
        users_by_ra = {user.get('ra'): user for user in all_users if user.get('ra')}

        filtered_data = []
        for atestado in all_atestados:
            ra = atestado.get('ra')
            if not ra:
                continue
                
            user = users_by_ra.get(ra)
            if not user:
                continue
                
            match = True
            if periodo and user.get('turno', '').lower() != periodo.lower():
                match = False
            if turma and user.get('curso', '').lower() != turma.lower():
                match = False
            if semestre and user.get('semestre', '').lower() != semestre.lower():
                match = False
            if estado and atestado.get('estado', '').lower() != estado.lower():
                match = False
            
            if match:
                filtered_atestado = {
                    'ra': ra,
                    'nome_aluno': atestado.get('nome_aluno', user.get('nome', 'N/A')),
                    'data_envio': atestado.get('data_envio', ''),
                    'inicio_periodo': atestado.get('inicio_periodo', ''),
                    'fim_periodo': atestado.get('fim_periodo', ''),
                    'estado': atestado.get('estado', '')
                }
                filtered_data.append(filtered_atestado)
        
        filtros = {
            'periodo': periodo,
            'turma': turma,
            'semestre': semestre,
            'estado': estado
        }
        
        output_path = os.path.join(BASE_DIR, 'data/relatorios/relatorio.pdf')
        success = fc2.gerar_pdf_simples(filtered_data, filtros=filtros, output_path=output_path)

        if success:
            return f.send_file(output_path, as_attachment=True)
        else:
            return "Erro ao gerar PDF", 500

@app.route('/relatorio_medias_csv', methods=['GET', 'POST'])
@admin_required(min_level=3)
def relatorio_medias_csv():
    all_data = fc.avaliacoes_db.read()
    all_users = fc.user_db.read()

    enriched_data = []
    users_by_ra = {user.get('ra'): user for user in all_users if user.get('ra')}
    
    if f.request.method == 'POST':
        filtros = {
            'equipe': f.request.form.get("equipe"),
            'curso': f.request.form.get("curso"),
            'semestre': f.request.form.get("semestre"),
            'periodo': f.request.form.get("periodo"),
            'sprint': f.request.form.get("sprint")
        }
    else:
        filtros = None
    
    for item in all_data:
        aluno = users_by_ra.get(item.get("ra_aluno"))
        if not aluno:
            continue
            
        match = True
        if filtros:
            if filtros['equipe'] and aluno.get('equipe', '').lower() != filtros['equipe'].lower():
                match = False
            if filtros['curso'] and aluno.get('curso', '').lower() != filtros['curso'].lower():
                match = False
            if filtros['semestre'] and aluno.get('semestre', '').lower() != filtros['semestre'].lower():
                match = False
            if filtros['periodo'] and aluno.get('turno', '').lower() != filtros['periodo'].lower():
                match = False
            if filtros['sprint'] and item.get('sprint', '').lower() != filtros['sprint'].lower():
                match = False
        
        if match:
            enriched_data.append({
                **item,
                "nome_aluno": aluno.get("nome", "N/A"),
                "curso": aluno.get("curso", "N/A"),
                "semestre": aluno.get("semestre", "N/A"),
                "equipe": aluno.get("equipe", "N/A"),
                "turno": aluno.get("turno", "N/A")
            })
    
    output_dir = os.path.join(BASE_DIR, "data", "relatorios")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "medias.csv")
    success = fc2.gerar_csv_medias(enriched_data, output_path, filtros=filtros)
    
    if success:
        return f.send_file(output_path, as_attachment=True)
    else:
        return "Erro ao gerar relatório de médias", 500


@app.route('/relatorio_avaliacoes_pdf', methods=['GET', 'POST'])
@admin_required(min_level=3)
def relatorio_avaliacoes_pdf():
    if f.request.method == 'POST':
        filtros = {
            'equipe': f.request.form.get("equipe"),
            'periodo': f.request.form.get("periodo"),
            'curso': f.request.form.get("curso"),
            'semestre': f.request.form.get("semestre"),
            'sprint': f.request.form.get("sprint")
        }
        
        all_data = fc.avaliacoes_db.read()
        all_users = fc.user_db.read()
        users_by_ra = {user.get('ra'): user for user in all_users if user.get('ra')}
        
        filtered_data = []
        for item in all_data:
            aluno = users_by_ra.get(item.get("ra_aluno"))
            if not aluno:
                continue
                
            match = True
            if filtros['equipe'] and aluno.get('equipe', '').lower() != filtros['equipe'].lower():
                match = False
            if filtros['curso'] and aluno.get('curso', '').lower() != filtros['curso'].lower():
                match = False
            if filtros['semestre'] and aluno.get('semestre', '').lower() != filtros['semestre'].lower():
                match = False
            if filtros['periodo'] and aluno.get('turno', '').lower() != filtros['periodo'].lower():
                match = False
            if filtros['sprint'] and item.get('sprint', '').lower() != filtros['sprint'].lower():
                match = False
            
            if match:
                avaliador = users_by_ra.get(item.get("avaliador_ra"))
                enriched_item = {
                    **item,
                    "nome_aluno": aluno.get("nome", "N/A"),
                    "nome_avaliador": avaliador.get("nome", "N/A") if avaliador else "N/A",
                    "equipe": aluno.get("equipe", "N/A"),
                    "curso": aluno.get("curso", "N/A"),
                    "semestre": aluno.get("semestre", "N/A")
                }
                filtered_data.append(enriched_item)
        
        data = filtered_data
    else:
        data = fc.avaliacoes_db.read()
        filtros = None
    
    output_path = os.path.join(BASE_DIR, 'data/relatorios/avaliacoes.pdf')
    success = fc2.gerar_pdf_avaliacoes(data, filtros=filtros, output_path=output_path)

    if success:
        return f.send_file(output_path, as_attachment=True)
    else:
        return "Erro ao gerar PDF de avaliações", 500

@app.route('/relatorio_medias_pdf', methods=['GET', 'POST'])
@admin_required(min_level=3)
def relatorio_medias_pdf():
    all_data = fc.avaliacoes_db.read()
    all_users = fc.user_db.read()
    users_by_ra = {user.get('ra'): user for user in all_users if user.get('ra')}
    
    if f.request.method == 'POST':
        filtros = {
            'equipe': f.request.form.get("equipe"),
            'curso': f.request.form.get("curso"),
            'semestre': f.request.form.get("semestre"),
            'periodo': f.request.form.get("periodo"),
            'sprint': f.request.form.get("sprint")
        }
    else:
        filtros = None
    
    alunos = {}
    for item in all_data:
        ra = item.get("ra_aluno")
        if not ra:
            continue
            
        aluno = users_by_ra.get(ra)
        if not aluno:
            continue
            
        if filtros:
            if filtros['equipe'] and aluno.get('equipe', '').lower() != filtros['equipe'].lower():
                continue
            if filtros['curso'] and aluno.get('curso', '').lower() != filtros['curso'].lower():
                continue
            if filtros['semestre'] and aluno.get('semestre', '').lower() != filtros['semestre'].lower():
                continue
            if filtros['periodo'] and aluno.get('turno', '').lower() != filtros['periodo'].lower():
                continue
            if filtros['sprint'] and item.get('sprint', '').lower() != filtros['sprint'].lower():
                continue
        
        sprint = item.get("sprint", "Geral")
        
        if ra not in alunos:
            alunos[ra] = {
                "ra": ra,
                "nome": aluno.get("nome", "N/A"),
                "equipe": aluno.get("equipe", "N/A"),
                "sprints": {},
                "total_avaliacoes": 0,
                "soma_produtividade": 0,
                "soma_autonomia": 0,
                "soma_colaboracao": 0,
                "soma_entrega": 0,
                "contador": 0
            }
        
        if sprint not in alunos[ra]["sprints"]:
            alunos[ra]["sprints"][sprint] = {
                "soma_produtividade": 0,
                "soma_autonomia": 0,
                "soma_colaboracao": 0,
                "soma_entrega": 0,
                "contador": 0
            }
        
        alunos[ra]["sprints"][sprint]["soma_produtividade"] += item.get("produtividade", 0)
        alunos[ra]["sprints"][sprint]["soma_autonomia"] += item.get("autonomia", 0)
        alunos[ra]["sprints"][sprint]["soma_colaboracao"] += item.get("colaboracao", 0)
        alunos[ra]["sprints"][sprint]["soma_entrega"] += item.get("entrega_resultados", 0)
        alunos[ra]["sprints"][sprint]["contador"] += 1
        
        alunos[ra]["soma_produtividade"] += item.get("produtividade", 0)
        alunos[ra]["soma_autonomia"] += item.get("autonomia", 0)
        alunos[ra]["soma_colaboracao"] += item.get("colaboracao", 0)
        alunos[ra]["soma_entrega"] += item.get("entrega_resultados", 0)
        alunos[ra]["contador"] += 1
        alunos[ra]["total_avaliacoes"] += 1

    processed_data = []
    for ra, aluno in alunos.items():
        if aluno["contador"] > 0:
            media_geral_prod = aluno["soma_produtividade"] / aluno["contador"]
            media_geral_auto = aluno["soma_autonomia"] / aluno["contador"]
            media_geral_colab = aluno["soma_colaboracao"] / aluno["contador"]
            media_geral_entrega = aluno["soma_entrega"] / aluno["contador"]
            media_geral_total = (media_geral_prod + media_geral_auto + 
                               media_geral_colab + media_geral_entrega) / 4
            
            processed_data.append({
                "ra": ra,
                "nome": aluno["nome"],
                "equipe": aluno["equipe"],
                "sprint": "Geral",
                "media_produtividade": media_geral_prod,
                "media_autonomia": media_geral_auto,
                "media_colaboracao": media_geral_colab,
                "media_entrega": media_geral_entrega,
                "media_total": media_geral_total,
                "total_avaliacoes": aluno["total_avaliacoes"]
            })
        
        for sprint, dados in aluno["sprints"].items():
            if dados["contador"] > 0:
                media_prod = dados["soma_produtividade"] / dados["contador"]
                media_auto = dados["soma_autonomia"] / dados["contador"]
                media_colab = dados["soma_colaboracao"] / dados["contador"]
                media_entrega = dados["soma_entrega"] / dados["contador"]
                media_total = (media_prod + media_auto + media_colab + media_entrega) / 4
                
                processed_data.append({
                    "ra": ra,
                    "nome": aluno["nome"],
                    "equipe": aluno["equipe"],
                    "sprint": sprint,
                    "media_produtividade": media_prod,
                    "media_autonomia": media_auto,
                    "media_colaboracao": media_colab,
                    "media_entrega": media_entrega,
                    "media_total": media_total,
                    "total_avaliacoes": dados["contador"]
                })
    
    output_path = os.path.join(BASE_DIR, 'data/relatorios/medias.pdf')
    success = fc2.gerar_pdf_medias(processed_data, filtros=filtros, output_path=output_path)

    if success:
        return f.send_file(output_path, as_attachment=True)
    else:
        return "Erro ao gerar PDF de médias", 500

@app.route('/relatorio_atestados_csv', methods=['GET', 'POST'])
@admin_required(min_level=3)
def relatorio_atestados_csv():
    if f.request.method == "POST":
        periodo = f.request.form.get("periodo")
        turma = f.request.form.get("turma")
        semestre = f.request.form.get("Semestre")
        estado = f.request.form.get("estado")
        
        filtros = {
            'periodo': periodo,
            'turma': turma,
            'semestre': semestre,
            'estado': estado
        }
        
        all_atestados = fc.atestados_db.read()
        all_users = fc.user_db.read()
        users_by_ra = {user.get('ra'): user for user in all_users if user.get('ra')}

        filtered_data = []
        for atestado in all_atestados:
            ra = atestado.get('ra')
            if not ra:
                continue
                
            user = users_by_ra.get(ra)
            if not user:
                continue
                
            match = True
            if periodo and user.get('turno', '').lower() != periodo.lower():
                match = False
            if turma and user.get('curso', '').lower() != turma.lower():
                match = False
            if semestre and user.get('semestre', '').lower() != semestre.lower():
                match = False
            if estado and atestado.get('estado', '').lower() != estado.lower():
                match = False
            
            if match:
                filtered_atestado = {
                    **atestado,
                    'nome_aluno': atestado.get('nome_aluno', user.get('nome', 'N/A'))
                }
                filtered_data.append(filtered_atestado)
        
        data = filtered_data
    else:
        data = fc.atestados_db.read()
        filtros = None
    
    output_path = os.path.join(BASE_DIR, 'data/relatorios/atestados.csv')
    success = fc2.gerar_csv_atestados(data, filtros=filtros, output_path=output_path)

    if success:
        return f.send_file(output_path, as_attachment=True)
    else:
        return "Erro ao gerar CSV de atestados", 500


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