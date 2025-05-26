import process as pr
import flask as f
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


user_db = pr.JSON_MANAGER(os.path.join(BASE_DIR, "data/db/user.json"))
atestados_db = pr.JSON_MANAGER(os.path.join(BASE_DIR, "data/db/atestados.json"))
equipes_db = pr.JSON_MANAGER(os.path.join(BASE_DIR, "data/db/equipes.json"))
avaliacoes_db = pr.JSON_MANAGER(os.path.join(BASE_DIR, "data/db/avaliacoes.json"))
diaAtual = datetime.now().strftime('%Y-%m-%d')

def get_next_id(db, id_field):
    try:
        data = db.read()
        if not data:
            return "001"

        numeric_ids = []
        for item in data:
            try:
                if item.get(id_field):
                    numeric_ids.append(int(str(item[id_field]).strip()))
            except (ValueError, AttributeError):
                continue
        
        if not numeric_ids:
            return "001"
            
        max_id = max(numeric_ids)
        return f"{max_id + 1:03d}"
    except Exception as e:
        print(f"Erro ao gerar ID: {str(e)}")
        return None

def new_usuario():
    user_id = get_next_id(user_db, 'user_id')
    if not user_id:
        return {"status": "error", "message": "Falha ao gerar ID de usuário"}
    
    atual = user_db.read()
    tipo_usuario = f.request.form.get('tipo')

    def ajustar_nome(nome):
        return " ".join([palavra.capitalize() for palavra in nome.split()])

    if tipo_usuario == "administrador":
        if not all(f.request.form.get(field) for field in ['nome', 'username', 'senha', 'nivel_acesso']):
            f.flash('Preencha todos os campos obrigatórios', 'error')
            return {"status": "error", "message": "Campos obrigatórios faltando"}
            
        user = pr.ADM(
            user_id=user_id,
            nome=ajustar_nome(f.request.form["nome"].strip()),    
            username=f.request.form["username"],    
            senha=str(f.request.form["senha"]),
            nivel_acesso=f.request.form["nivel_acesso"]
        ).to_dict()
    else:
        if not all(f.request.form.get(field) for field in ['nome', 'ra', 'senha', 'curso', 'semestre', 'turno']):
            f.flash('Preencha todos os campos obrigatórios', 'error')
            return {"status": "error", "message": "Campos obrigatórios faltando"}
            
        user = pr.ALUNO(
            user_id=user_id,
            nome=ajustar_nome(f.request.form["nome"].strip()),
            ra=str(f.request.form["ra"]),
            senha=str(f.request.form["senha"]),
            curso=f.request.form["curso"].lower(),
            semestre=f.request.form["semestre"].lower(),
            turno=f.request.form["turno"].lower(),
            equipe=f.request.form.get("equipe", "Sem equipe").lower()
        ).to_dict()

        for x in atual:
            if x.get('tipo') == 'aluno' and x.get('ra') == user['ra']:
                f.flash(f"O RA: {user['ra']} já está registrado", 'error')
                return {"status": "error", "message": "RA já existe na base de dados"}

    if user_db.add(user):
        f.flash("Usuário criado com sucesso", 'success')
        return {"status": "success", "user_id": str(user_id)}
    else:
        f.flash("Falha ao criar usuário", 'error')
        return {"status": "error", "message": "Falha ao criar usuário"}

def new_atestado():
    atestados_folder = os.path.join(BASE_DIR, "data/atestados", f.session['ra'])
    os.makedirs(atestados_folder, exist_ok=True)

    nome_aluno = f.session["nome"].lower()
    ra_aluno = f.session["ra"]
    atestado_id = get_next_id(atestados_db, 'atestado_id')

    file = f.request.files["atestado_pdf"]
    if not file.filename.lower().endswith('.pdf'):
        f.flash("Apenas arquivos PDF são permitidos.", 'error')
        return {"status": "error", "message": "Formato inválido"}
    fileName =f"{atestado_id}_{nome_aluno.split()[0]}_{diaAtual}.pdf"
    filePath = os.path.join(atestados_folder, fileName)
    file.save(filePath)


    atestado = pr.ATESTADO(
        atestado_id=atestado_id,
        data_envio=diaAtual,
        file_path=filePath.replace("\\", "/"),
        ra_aluno=ra_aluno,
        nome_aluno=nome_aluno,
        inicio_periodo=f.request.form["data_inicio"],
        fim_periodo=f.request.form["data_fim"],
    ).to_dict()

    if atestados_db.add(atestado, identifier_key="atestado_id"):
        f.flash("Atestado enviado", 'success')
        return {"status": "success"}
    else:
        return {"status": "error", "message": "Falha ao enviar atestado"}
        f.flash("Falha ao enviar atestado", 'error')

def equipe():
    nome_equipe = f.request.form['nomeEquipe']
    list_members = f.request.form['members'].split()
    
    ra_scrum_master = None
    ra_product_owner = None
    dev_team_members = []
    
    for x in list_members:
        funcao = f.request.form.get(f'funcao_{x}')
        if funcao == "scrum":
            ra_scrum_master = x
        elif funcao == "po":
            ra_product_owner = x
        else:
            dev_team_members.append(x)

    if not equipes_db.find(nome_equipe, "nome_equipe"):
        data = pr.Equipe(
            equipe_id=get_next_id(equipes_db, 'equipe_id'),
            nome_equipe=nome_equipe,
            ra_product_owner=ra_product_owner,
            ra_scrum_master=ra_scrum_master
        )
       
        for x in list_members:
            if x in dev_team_members:
                data.add_to_team(x)
            data.add_membro(x)
        
        data = data.to_dict()

        if equipes_db.add(data, identifier_key="equipe_id"):
            f.flash("Equipe criada com sucesso", 'success')

            for ra in list_members:
                aluno = user_db.find(ra, "ra")
                if aluno:
                    aluno['equipe'] = data['nome_equipe']
                    if ra == ra_scrum_master:
                        aluno['funcao'] = 'scrum'
                    elif ra == ra_product_owner:
                        aluno['funcao'] = 'po'
                    else:
                        aluno['funcao'] = 'devteam'
                    user_db.edit(ra, aluno, "ra")
            
            return {"status": "success"}
        else:
            return {"status": "error", "message": "Falha ao registrar equipe"}
    else:
        new_data = equipes_db.find(nome_equipe, "nome_equipe")
        
        for ra in list_members:
            if ra not in new_data['membros']:
                new_data['membros'].append(ra)
            
            aluno = user_db.find(ra, "ra")
            if aluno:
                aluno['equipe'] = new_data['nome_equipe']
                funcao = f.request.form.get(f'funcao_{ra}')
                if funcao == 'scrum':
                    aluno['funcao'] = 'scrum'
                    new_data['ra_scrum_master'] = ra
                elif funcao == 'po':
                    aluno['funcao'] = 'po'
                    new_data['ra_product_owner'] = ra
                else:
                    aluno['funcao'] = 'devteam'
                    if 'devteam' not in new_data:
                        new_data['devteam'] = []
                    if ra not in new_data['devteam']:
                        new_data['devteam'].append(ra)
                user_db.edit(ra, aluno, "ra")
        
        if equipes_db.edit(nome_equipe, new_data, "nome_equipe"):
            return {"status": "success"}
        else:
            return {"status": "error", "message": "Falha ao atualizar equipe"}
        

def avaliar_equipe_post():
    if not f.session.get('ra'):
        raise Exception("Avaliador não identificado")
    
    ra_alunos = f.request.form.getlist('ra_aluno')
    avaliacoes = []

    for ra in ra_alunos:
        if not all(f.request.form.get(f'{crit}_{ra}') for crit in ['produtividade', 'autonomia', 'colaboracao', 'entrega_resultados']):
            f.flash(f"Dados incompletos para o aluno {ra}", 'error')
            raise ValueError(f"Dados incompletos para o aluno {ra}")
    
    for ra in ra_alunos:
        try:
            avaliacao_id = None
            attempts = 0
            while not avaliacao_id and attempts < 5:
                temp_id = get_next_id(avaliacoes_db, 'avaliacao_id')
                if temp_id and not avaliacoes_db.find(temp_id, 'avaliacao_id'):
                    avaliacao_id = temp_id
                attempts += 1
            
            if not avaliacao_id:
                avaliacao_id = f"temp_{datetime.now().strftime('%Y%m%d%H%M%S')}_{ra}"

            avaliacao = pr.AVALIACAO(
                avaliacao_id=avaliacao_id,
                ra_aluno= ra,
                sprint=f.request.form.get(f"sprint"),
                avaliador_ra=f.session['ra'],
                produtividade=int(f.request.form.get(f'produtividade_{ra}')),
                autonomia=int(f.request.form.get(f'autonomia_{ra}')),
                colaboracao=int(f.request.form.get(f'colaboracao_{ra}')),
                entrega_resultados=int(f.request.form.get(f'entrega_resultados_{ra}')),
                feedback=f.request.form.get(f'feedback_{ra}')
            ).to_dict()

            if not avaliacoes_db.add(avaliacao):
                raise Exception(f"Falha ao persistir avaliação para RA {ra}")
                
        except Exception as e:
            print(f"Falha na avaliação do RA {ra}: {str(e)}")
            raise Exception(f"Erro ao avaliar {ra}: {str(e)}")
    
    f.flash('Avaliações registradas com sucesso!', 'success')
    return True
