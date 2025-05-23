import json
import random
from werkzeug.security import generate_password_hash

# Listas de dados aleatórios
NOMES = ['João', 'Maria', 'Carlos', 'Ana', 'Pedro', 'Lucia', 'Marcos', 'Fernanda']
SOBRENOMES = ['Silva', 'Souza', 'Oliveira', 'Santos', 'Ferreira', 'Almeida', 'Lima', 'Costa']
CURSOS = ['Engenharia', 'Ciência da Computação', 'Medicina', 'Direito', 'Administração', 'Arquitetura']
TURNOS = ['manhã', 'tarde', 'noite']

def gerar_ra():
    return str(random.randint(10000, 99999))

def gerar_senha():
    return f"senha{random.randint(100, 999)}"

def gerar_aluno(sem_equipe=False):
    aluno = {
        "user_id": str(random.randint(100, 999)),
        "nome": f"{random.choice(NOMES)} {random.choice(SOBRENOMES)}",
        "ra": gerar_ra(),
        "senha": generate_password_hash(gerar_senha()),
        "tipo": "aluno",
        "curso": random.choice(CURSOS),
        "semestre": str(random.randint(1, 10)),
        "turno": random.choice(TURNOS),
    }
    aluno["equipe"] = "sem equipe" if sem_equipe else f"Equipe {random.choice(['A', 'B', 'C', 'D'])}"
    return aluno

def gerar_admin():
    return {
        "user_id": str(random.randint(100, 999)),
        "nome": f"Admin {random.choice(NOMES)}",
        "username": f"admin{random.randint(1, 100)}",
        "senha": generate_password_hash(gerar_senha()),
        "tipo": "administrador",
        "nivel_acesso": str(random.randint(1, 3))
    }

def gerar_equipe(membros_ras):
    # Garante que cada equipe tenha entre 2 e 5 membros
    num_membros = random.randint(2, min(5, len(membros_ras)))
    membros = random.sample(membros_ras, num_membros)
    
    return {
        "equipe_id": str(random.randint(100, 999)),
        "nome_equipe": f"Equipe {random.choice(['Alpha', 'Beta', 'Gamma', 'Delta'])}",
        "membros": membros
    }

def main():
    print("==== Gerador de Banco de Dados ====")
    
    num_alunos = int(input("Quantos alunos deseja criar? "))
    num_admins = int(input("Quantos administradores deseja criar? "))
    num_equipes = int(input("Quantas equipes deseja criar? "))
    
    users = []
    ras_disponiveis = []
    
    # 1. Gerar alunos (todos inicialmente sem equipe)
    for _ in range(num_alunos):
        aluno = gerar_aluno(sem_equipe=(num_equipes == 0))
        users.append(aluno)
        ras_disponiveis.append(aluno['ra'])
    
    # 2. Gerar admins
    for _ in range(num_admins):
        users.append(gerar_admin())
    
    # 3. Gerar equipes (se solicitado e houver alunos suficientes)
    equipes = []
    if num_equipes > 0 and len(ras_disponiveis) >= 2:
        # Criar equipes
        for _ in range(min(num_equipes, len(ras_disponiveis) // 2)):
            equipe = gerar_equipe(ras_disponiveis)
            equipes.append(equipe)
            
            # Atualizar alunos para refletir a equipe
            for ra in equipe['membros']:
                for user in users:
                    if user.get('ra') == ra:
                        user['equipe'] = equipe['nome_equipe']
                        break
    
    # 4. Salvar arquivos
    with open('app/data/db/user.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)
    
    with open('app/data/db/equipes.json', 'w', encoding='utf-8') as f:
        json.dump(equipes, f, indent=4, ensure_ascii=False)
    
    print(f"\nBanco de dados populado com sucesso!")
    print(f"- Total de usuários: {len(users)} ({num_alunos} alunos e {num_admins} admins)")
    print(f"- Equipes criadas: {len(equipes)}")
    print(f"- Alunos sem equipe: {sum(1 for u in users if u.get('tipo') == 'aluno' and u.get('equipe') == 'sem equipe')}")

if __name__ == "__main__":
    main()