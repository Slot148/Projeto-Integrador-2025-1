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
def readJSON(files):
    if os.path.exists(files) :
        with open(files, "r", encoding="utf-8") as f:
            try:
                 return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


#Função para escrever no JSON
def writeJSON(data, files):
    os.makedirs(os.path.dirname(files), exist_ok=True)  
    with open(files, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


#Função que recebe os valores dos campos do formulario
##Ela deve ser chamada imediatamente como resposta ao submit do formulario (especificamente o de scrum)
def processingScrum():
    try:
        nomeAlunoScrum = request.form['nomeAlunoScrum']
        nomeEquipeScrum = request.form['nomeEquipeScrum']
        teamFunction = request.form['teamFunction']

        # Pegando as notas do formulário
        try:
            nota1 = int(request.form['nota1'])
            nota2 = int(request.form['nota2'])
            nota3 = int(request.form['nota3'])
            nota4 = int(request.form['nota4'])
            
        except ValueError:
            return "Notas devem ser números válidos"

    except:
        return "Preencha todos os campos corretamente"
    
    nomeAlunoScrum = nomeAlunoScrum.lower()

    data = readJSON(scrumFile)
    novaInserção = ({"Nome": nomeAlunoScrum, "Equipe": nomeEquipeScrum, "Função": teamFunction, "Notas": [nota1, nota2, nota3, nota4]})
    data.append(novaInserção)
    writeJSON(data, scrumFile)

#Função que recebe os valores dos campos do formulario
##Ela deve ser chamada imediatamente como resposta ao submit do formulario (especificamente o de atestados)
def processingAtestados():
    try:
        nomeAluno = request.form['nomeAluno'] #O campo input deve haver a string requisitada como name
        raAluno = request.form['raAluno'] #O campo input deve haver a string requisitada como name
        dataUpload = diaAtual
        dataInicio = request.form['initDate']
        dataFim = request.form['endDate']
        newFile = request.files['insertFile']

    except:
        return "preencha todos os campos"
    
    if not raAluno.isdigit():
       return "todos os caracteres devem ser numéricos"

    #padronizando os nomes
    nomeAluno = nomeAluno.lower()
    periodoValido = f"{dataInicio}_a_{dataFim}"

    #verificando se as pastas existem
    os.makedirs(fileFolder, exist_ok=True)
    
    #Salva o caminho do arquivo
    fileName =f"{nomeAluno.replace(' ', '_')}_{diaAtual}.pdf"
    filePath = os.path.join(fileFolder, fileName)

    #salva o arquivo no diretorio atestados
    newFile.save(filePath)

    #adiciona uma nova sessão ao JSON
    data = readJSON(dataFile)
    novaInserção = ({"Nome": nomeAluno, "R.A": int(raAluno), "Periodo de Validade": periodoValido, "Atestado": filePath, "Data de Upload": dataUpload})
    data.append(novaInserção)
    writeJSON(data, dataFile)
    
    return "Atestado enviado"         
