import process as pr
import flask as f

user_db = pr.JSON_MANAGER("app/data/db/user.json")
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
