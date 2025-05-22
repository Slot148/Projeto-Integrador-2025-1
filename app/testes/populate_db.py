import json
from werkzeug.security import generate_password_hash

# Dados de usuários (alunos e administradores)
users = [
    {
        "user_id": "001",
        "nome": "João Silva",
        "ra": "123",
        "senha": generate_password_hash("senha123"),
        "tipo": "aluno",
        "curso": "Engenharia",
        "semestre": "3",
        "turno": "manhã",
        "equipe": "Nicolas inc"
    },
    {
        "user_id": "002",
        "nome": "Maria Souza",
        "ra": "678",
        "senha": generate_password_hash("senha678"),
        "tipo": "aluno",
        "curso": "Ciência da Computação",
        "semestre": "2",
        "turno": "tarde",
        "equipe": "Nicolas inc"
    },
    {
        "user_id": "003",
        "nome": "Carlos Oliveira",
        "ra": "234",
        "senha": generate_password_hash("senha234"),
        "tipo": "aluno",
        "curso": "Medicina",
        "semestre": "5",
        "turno": "noite",
        "equipe": "Y2K"
    },
    {
        "user_id": "004",
        "nome": "Administrador",
        "username": "admin",
        "senha": generate_password_hash("admin123"),
        "tipo": "administrador",
        "nivel_acesso": "1"
    }
]

# Dados de equipes
equipes = [
    {
        "equipe_id": "001",
        "nome_equipe": "Nicolas inc",
        "membros": ["123", "678"]
    },
    {
        "equipe_id": "002",
        "nome_equipe": "Y2K",
        "membros": ["234"]
    },
    {
        "equipe_id": "003",
        "nome_equipe": "404",
        "membros": ["456"]  # RA que não existe em users (para teste)
    }
]

# Salvar no user.json
with open('app/data/db/user.json', 'w', encoding='utf-8') as f:
    json.dump(users, f, indent=4, ensure_ascii=False)

# Salvar no equipes.json
with open('app/data/db/equipes.json', 'w', encoding='utf-8') as f:
    json.dump(equipes, f, indent=4, ensure_ascii=False)

print("Bancos de dados populados com sucesso!")