from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

#Caaminho do JSON
dataFile = 'data/atestado.json'
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
##Ela deve ser chamada imediatamente como resposta ao submit do formulario (especificamente o de atestados)
def processingJSON():
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