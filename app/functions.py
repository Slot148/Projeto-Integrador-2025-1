import process as pr
import flask as f
from datetime import datetime
import os

user_db = pr.JSON_MANAGER("app/data/db/user.json")
atestados_db = pr.JSON_MANAGER("app/data/db/atestados.json")
diaAtual = datetime.now().strftime('%Y-%m-%d')
equipes_db = pr.JSON_MANAGER("app/data/db/equipes.json")
avaliacoes_db = pr.JSON_MANAGER("app/data/db/avaliacoes.json")



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
    atual = user_db.read()
    tipo_usuario = f.request.form.get('tipo')

    if tipo_usuario == "administrador":
        user = pr.ADM(
            user_id=user_id,
            nome=f.request.form["nome"].lower(),    
            username=f.request.form["username"],    
            senha=str(f.request.form["senha"]),
            nivel_acesso=f.request.form["nivel_acesso"]
        ).to_dict()
    else:
        user = pr.ALUNO(
            user_id=user_id,
            nome=f.request.form["nome"].lower(),
            ra=str(f.request.form["ra"]),
            senha=str(f.request.form["senha"]),
            curso=f.request.form["curso"].lower(),
            semestre=f.request.form["semestre"].lower(),
            turno=f.request.form["turno"].lower(),
            equipe=f.request.form.get("equipe", "Sem equipe").lower()
        ).to_dict()

        for x in atual:
            if x['tipo'] == 'aluno' and user['ra'] == x['ra']:
                f.flash(f"O ra: {user['ra']} ja esta registrado em outro usuario", 'error')
                return {"status": "error", "message": "o ra ja existe na base de dados"};   


    if user_db.add(user):
        f.flash(f"Usuario criado com Sucesso", 'message')
        return {"status": "success", "user_id": str(user_id)}
    else:
        return {"status": "error", "message": "Falha ao criar usuário"}
    
def new_atestado():
    atestados_folder = f"app/data/atestados/{f.session['ra']}"
    if not os.path.exists(atestados_folder):
        os.makedirs(atestados_folder)

    nome_aluno = f.session["nome"].lower()
    ra_aluno = f.session["ra"]
    atestado_id = get_next_id(atestados_db, 'atestado_id')

    file = f.request.files["atestado_pdf"]
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
        return {"status": "success"}
    else:
        return {"status": "error", "message": "Falha ao enviar atestado"}

def equipe():
    nome_equipe = f.request.form['nomeEquipe']
    list_members = f.request.form['members'].split()

    if not equipes_db.find(nome_equipe, "nome_equipe"):
        data = pr.Equipe(
            equipe_id = get_next_id(equipes_db, 'equipe_id'),
            nome_equipe=nome_equipe
        )

        for x in list_members:
            data.add_membro(x)
        
        data = data.to_dict()

        if equipes_db.add(data, identifier_key="equipe_id"):
            for ra in list_members:
                aluno = user_db.find(ra, "ra")
                aluno['equipe'] = data['nome_equipe']
                if aluno:
                    user_db.edit(ra, aluno, "ra")
            
            return {"status": "success"}
        else:
            return {"status": "error", "message": "Falha ao registrar equipe"}
    else:
        new_data = equipes_db.find(nome_equipe, "nome_equipe")
        for ra in list_members:
            new_data['membros'].append(ra)
            aluno = user_db.find(ra, "ra")
            aluno['equipe'] = new_data['nome_equipe']
            if aluno:
                user_db.edit(ra, aluno, "ra")
        
        if equipes_db.edit(nome_equipe, new_data, "nome_equipe"):
            return {"status": "success"}
        else:
            return {"status": "error", "message": "Falha ao registrar equipe"}

def avaliar_equipe_post():
    if not f.session.get('ra'):
        raise Exception("Avaliador não identificado")
    
    ra_alunos = f.request.form.getlist('ra_aluno')
    avaliacoes = []
    
    # Primeiro valida todos os dados ANTES de gerar IDs
    for ra in ra_alunos:
        if not all(f.request.form.get(f'{crit}_{ra}') for crit in ['planejamento', 'autonomia', 'colaboracao', 'entrega_resultados']):
            raise ValueError(f"Dados incompletos para o aluno {ra}")
    
    # Agora processa cada avaliação com ID único
    for ra in ra_alunos:
        try:
            # Gera um novo ID para CADA avaliação
            avaliacao_id = None
            attempts = 0
            while not avaliacao_id and attempts < 5:
                temp_id = get_next_id(avaliacoes_db, 'avaliacao_id')
                if temp_id and not avaliacoes_db.find(temp_id, 'avaliacao_id'):
                    avaliacao_id = temp_id
                attempts += 1
            
            if not avaliacao_id:
                avaliacao_id = f"temp_{datetime.now().strftime('%Y%m%d%H%M%S')}_{ra}"
                
            avaliacao = {
                "avaliacao_id": avaliacao_id,
                "ra_aluno": ra,
                "avaliador_ra": f.session['ra'],
                "planejamento": int(f.request.form.get(f'planejamento_{ra}')),
                "autonomia": int(f.request.form.get(f'autonomia_{ra}')),
                "colaboracao": int(f.request.form.get(f'colaboracao_{ra}')),
                "entrega_resultados": int(f.request.form.get(f'entrega_resultados_{ra}')),
                "data_avaliacao": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            if not avaliacoes_db.add(avaliacao):
                raise Exception(f"Falha ao persistir avaliação para RA {ra}")
                
        except Exception as e:
            print(f"Falha na avaliação do RA {ra}: {str(e)}")
            raise Exception(f"Erro ao avaliar {ra}: {str(e)}")
    
    return True
