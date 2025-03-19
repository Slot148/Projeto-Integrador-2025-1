from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

#Caaminho do JSON
dataFile = 'data/atestado.json'

#Para definir o dia do upload(alterar futurramente)
diaAtual = datetime.today().strftime('%Y/%m/%d')

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
    with open(dataFile, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

#Função que recebe os valores dos campos do formulario
##Ela deve ser chamada imediatamente como resposta ao submit do formulario (especificamente o de atestados)
def processingJSON():
    nomeAluno = request.form.get('nomeAluno') #O campo input deve haver a string requisitada como id
    raAluno = request.form.get('raAluno') #O campo input deve haver a string requisitada como id
    dataUpload = diaAtual
    
    if not nomeAluno or not raAluno:
        return "preencha todos os campos"
    if not raAluno.isdigit():
       return "todos os caracteres devem ser numéricos"
    
    data = readJSON()
    novaInserção = ({"Nome": nomeAluno, "R.A": int(raAluno), "Data de Upload": dataUpload})
    data.append(novaInserção)
    writeJSON(data)
    
    return "Atestado enviado"         


#função para consulta simples dos dados em json
def dataConsult():
    data = readJSON()
    return jsonify (data)