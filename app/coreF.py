from flask import Flask, request, jsonify
import json
import os

#Caaminho do JSON
dataFile = 'data/atestado.json'

#Função para leitura do JSON
def readJSON():
    if os.path.exists(dataFile) :
        with open(dataFile, "r", encoding="utf-8") as f:
            try:
                 return json.load(f)
            except json.JSONDecodeError:
                return []
    return []
