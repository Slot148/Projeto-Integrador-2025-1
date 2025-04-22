import process as pr
import flask as f
from datetime import datetime
import os

user_db = pr.JSON_MANAGER("app/data/db/user.json")
atestados_db = pr.JSON_MANAGER("app/data/db/atestados.json")
atestados_folder = "app/data/atestados/"
diaAtual = datetime.today().strftime('%Y-%m-%d')
equipes_db = pr.JSON_MANAGER("app/data/db/equipes.json")
avaliacoes_db = pr.JSON_MANAGER("app/data/db/avaliacoes.json")
user_id = 1

def new_usuario():
    global user_id
    user_db.read()
    user = pr.ALUNO(
        user_id=str(user_id),
        nome=f.request.form["nome"].upper(),
        ra=str(f.request.form["ra"]),
        senha=str(f.request.form["senha"]),
        curso=f.request.form["curso"].upper(),
        semestre=f.request.form["semestre"].upper(),
        turno=f.request.form["turno"].upper(),
        equipe=f.request.form.get("equipe", "Sem equipe").upper()
    ).to_dict()

    user_id += 1

    if user_db.add(user):
        return {"status": "success", "user_id": str(user_id-1)}
    else:
        return {"status": "error", "message": "Falha ao criar usuário"}
    
def new_atestado():
    nome_aluno = f.session["nome"]
    ra_aluno = f.session["ra"]
    file = f.request.files["atestado_pdf"]
    fileName =f"{nome_aluno.replace(' ', '_')}_{ra_aluno}.pdf"
    filePath = os.path.join(atestados_folder, fileName)
    file.save(filePath)

    atestado = pr.ATESTADO(
        atestado_id=str(len(atestados_db.read()) + 1),
        data_envio=diaAtual,
        file_path=filePath.upper(),
        ra_aluno=ra_aluno,
        nome_aluno=nome_aluno,
        inicio_periodo=f.request.form["data_inicio"],
        fim_periodo=f.request.form["data_fim"]
    ).to_dict()

    if atestados_db.add(atestado):
        return {"status": "success"}
    else:
        return {"status": "error", "message": "Falha ao enviar atestado"}
    

