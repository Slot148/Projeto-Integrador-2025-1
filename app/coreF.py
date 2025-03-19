from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

#Caaminho do JSON
dataFile = 'data/atestado.json'
scrumFile = 'data/scrum-team.json'
fileFolder = "atestados"

#Para definir o dia do upload(alterar futurramente)
diaAtual = datetime.today().strftime('%Y-%m-%d')

#Função para leitura do JSON
def readJSON():
    if os.path.exists(dataFile) :
        with open(dataFile, "r", encoding="utf-8") as f:
            try:
                 return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

#Função para escrever no JSON
def writeJSON(data):
    os.makedirs(os.path.dirname(dataFile), exist_ok=True)  
    with open(dataFile, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


#Função que recebe os valores dos campos do formulario
##Ela deve ser chamada imediatamente como resposta ao submit do formulario (especificamente o de scrum)
def processingScrum():
    nomeAlunoScrum = request.form.get("nomeAlunoScrum")
    nomeEquipeScrum = request.form.get("nomeEquipeScrum")
    teamFunction = request.form.get("teamFunction")

    # Pegando as notas do formulário
    try:
        nota1 = int(request.form.get("nota1"), 0)
        nota2 = int(request.form.get("nota2"), 0)
        nota3 = int(request.form.get("nota3"), 0)
        nota4 = int(request.form.get("nota4"), 0)
    except ValueError:
        return "Notas devem ser números válidos"

    if not nomeAlunoScrum or not nomeEquipeScrum or not teamFunction or not nota1 or not nota2 or not nota3 or not nota4:
        return "Preencha todos os campos corretamente"
    
    data = readJSON()
    novaInserção = ({"Nome": nomeAlunoScrum, "Equipe": nomeEquipeScrum, "Função": teamFunction, "Notas": [nota1, nota2, nota3, nota4]})
    data.append(novaInserção)
    writeJSON(data)

#Função que recebe os valores dos campos do formulario
##Ela deve ser chamada imediatamente como resposta ao submit do formulario (especificamente o de atestados)
def processingAtestados():
    nomeAluno = request.form.get('nomeAluno') #O campo input deve haver a string requisitada como id
    raAluno = request.form.get('raAluno') #O campo input deve haver a string requisitada como id
    dataUpload = diaAtual
    newFile = request.files.get('insertFile')
    
    if not nomeAluno or not raAluno or not newFile:
        return "preencha todos os campos"
    if not raAluno.isdigit():
       return "todos os caracteres devem ser numéricos"

    #verificando se as pastas existem
    os.makedirs(fileFolder, exist_ok=True)
    
    #Salva o caminho do arquivo
    fileName =f"{nomeAluno}_{diaAtual}.pdf"
    filePath = os.path.join(fileFolder, fileName)

    #salva o arquivo no diretorio atestados
    newFile.save(filePath)

    #adiciona uma nova sessão ao JSON
    data = readJSON()
    novaInserção = ({"Nome": nomeAluno, "R.A": int(raAluno), "Data de Upload": dataUpload, "Atestado": filePath})
    data.append(novaInserção)
    writeJSON(data)
    
    return "Atestado enviado"         


#função para consulta simples dos dados em json
def dataConsult():
    data = readJSON()
    return jsonify(data)

###chame-o da seguinte forma para debugar###
# @app.route("/consult", methods=['GET'])
# def consult():
#     data = readJSON()
#     return app.response_class(
#         response=json.dumps(data, ensure_ascii=False, indent=4),
#         mimetype='application/json'
#     )
