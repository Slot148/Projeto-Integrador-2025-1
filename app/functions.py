import process as pr
import flask as f
from datetime import datetime
import os

user_db = pr.JSON_MANAGER("app/data/db/user.json")
atestados_db = pr.JSON_MANAGER("app/data/db/atestados.json")
diaAtual = datetime.now().strftime('%Y-%m-%d')
# equipes_db = pr.JSON_MANAGER("app/data/db/equipes.json")
# avaliacoes_db = pr.JSON_MANAGER("app/data/db/avaliacoes.json")

def get_next_id(db, id_field):
    data = db.read()
    if not data:
        return "001"
    max_id = max(int(item.get(id_field, 0)) for item in data)
    return f"{max_id + 1:03d}"

def new_usuario():
    user_id = get_next_id(user_db, 'user_id')
    atual = user_db.read()
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
        if user['ra'] == x['ra']:
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