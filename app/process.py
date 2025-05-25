import os, json
from filelock import FileLock, Timeout
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class USER:
    """Classe base que representa um usuário do sistema.
    
    Attributes:
        ra (str): Registro Acadêmico do usuário (identificador único)
        nome (str): Nome completo do usuário
        senha (str): Senha de acesso do usuário
    """
    def __init__(self, user_id, nome, senha, tipo):
        self.user_id = user_id
        self.nome = nome
        self.senha = generate_password_hash(senha)
        self.tipo = tipo
    
    def verify_password(self, senha):
        return check_password_hash(self.senha, senha)

    def to_dict(self):
        """Converte o objeto USER para um dicionário.
        
        Returns:
            dict: Dicionário contendo todos os atributos do usuário
        """
        return{
            "user_id": self.user_id,
            "nome": self.nome,
            "senha": self.senha,
            "tipo": self.tipo
        }

class ALUNO(USER):
    """Classe que representa um aluno, herda de USER.
    
    Attributes:
        ra (str): Registro Acadêmico do aluno
        nome (str): Nome completo do aluno
        senha (str): Senha de acesso do aluno
        curso (str): Curso que o aluno está matriculado
        turno (str): Turno de estudo (Manhã, Tarde, Noite)
        semestre (str): Semestre atual do aluno
        equipe (str): Nome da equipe do aluno (opcional, default="Sem Equipe")
    """
    def __init__(self, user_id, nome, ra, senha, curso, turno, semestre, equipe="Sem Equipe", funcao="none"):
        super().__init__(user_id, nome, senha, tipo="aluno")
        self.ra = ra
        self.curso = curso
        self.turno = turno
        self.semestre = semestre
        self.equipe = equipe
        self.funcao = funcao
    
    def to_dict(self):
        """Converte o objeto ALUNO para um dicionário.
        
        Returns:
            dict: Dicionário contendo todos os atributos do aluno,
                  incluindo os atributos da classe USER e o tipo "aluno"
        """
        data =  super().to_dict()
        data.update({
            "ra": self.ra,
            "curso": self.curso,
            "turno": self.turno,
            "semestre": self.semestre,
            "equipe":  self.equipe,
            "funcao": self.funcao
        })
        return data

class ADM(USER):
    def __init__(self, user_id, username, nome, senha, nivel_acesso="3"):
        if nivel_acesso not in ["1", "2", "3"]:
            raise ValueError("Nível de acesso deve ser 1 (mais alto), 2 ou 3 (mais básico)")
        super().__init__(user_id, nome, senha, tipo="administrador")
        self.username = username
        self.nivel_acesso = nivel_acesso
class ATESTADO:
    def __init__(self, atestado_id, file_path, data_envio, ra_aluno, nome_aluno, inicio_periodo, fim_periodo, estado = "pendente"):
        self.atestado_id = atestado_id
        self.file_path = file_path
        self.data_envio = data_envio
        self.ra_aluno = ra_aluno
        self.nome_aluno = nome_aluno
        self.inicio_periodo = inicio_periodo
        self.fim_periodo = fim_periodo
        self.estado = estado
    
    def to_dict(self):
        return{
            "atestado_id": self.atestado_id,
            "ra": self.ra_aluno,
            "nome_aluno": self.nome_aluno,
            "file_path": self.file_path,
            "data_envio": self.data_envio,
            "inicio_periodo": self.inicio_periodo,
            "fim_periodo": self.fim_periodo,
            "estado": self.estado
        }

class JSON_MANAGER:
    """Classe para gerenciar operações de CRUD em arquivos JSON.
    
    Attributes:
        file_path (str): Caminho completo para o arquivo JSON
    """
    def __init__(self, file_path):
        self.file_path = os.path.abspath(file_path)
        self.lock_path = self.file_path + ".lock"
        self.check()

    def check(self):
        """Verifica se o arquivo e diretório existem, criando-os se necessário.
        
        Raises:
            OSError: Se não for possível criar o diretório
            TypeError: Se o caminho do arquivo for inválido
        """
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            if not os.path.exists(self.file_path):
                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump([], f)
        except (OSError, TypeError) as e:
            print(f"Ocorreu um erro ao verificar/criar o arquivo: {e}")


    def write(self, data):
        """Escreve dados no arquivo JSON.
        
        Args:
            data (list): Lista de dicionários contendo os dados a serem escritos
            
        Returns:
            bool: True se a escrita foi bem sucedida, False caso contrário
        """
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except IOError as e:
            print(f"Erro ao escrever no arquivo: {e}")
            return False

    def read(self):
        """Lê todos os dados do arquivo JSON.
        
        Returns:
            list: Lista contendo todos os registros do arquivo.
                  Retorna lista vazia se o arquivo estiver vazio ou inválido.
        """
        self.check()
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def edit(self, identifier, new_data, identifier_key = "user_id"):
        """Edita um registro existente no arquivo JSON.
        
        Args:
            identifier (str): Valor identificador do registro a ser editado
            new_data (dict): Dicionário com os novos dados do registro
            identifier_key (str, optional): Chave do identificador.
                                          Defaults to "ra".
        
        Returns:
            bool: True se a edição foi bem sucedida, False caso contrário
        """
        data = self.read()
        for i, item in enumerate(data):
            if str(item.get(identifier_key)) == str(identifier):
                data[i] = new_data
                return self.write(data)
        return False
    
    def delete(self, identifier, identifier_key = "user_id"):
        """Remove um registro do arquivo JSON.
        
        Args:
            identifier (str): Valor identificador do registro a ser removido
            identifier_key (str, optional): Chave do identificador.
                                          Defaults to "user_id".
        
        Returns:
            bool: True se a remoção foi bem sucedida, False caso contrário
        """
        data = self.read()
        new_data = [item for item in data if str(item.get(identifier_key)) != str(identifier)]
        if len(new_data) < len(data):  
            return self.write(new_data)
        return False
    
    def find(self, identifier, identifier_key="user_id"):
        """Busca um registro específico no arquivo JSON.
        
        Args:
            identifier (str): Valor a ser buscado (ex: RA do aluno)
            identifier_key (str, optional): Chave do dicionário onde buscar.
                                          Defaults to "user_id".

        Returns:
            dict or None: Dicionário com os dados do registro se encontrado,
                         ou None se não encontrado.
        """
        data = self.read()
        for item in data:
            if str(item.get(identifier_key)) == str(identifier):
                return item
        return None
        
    def add(self, new_item, identifier_key="user_id"):
        lock = FileLock(self.lock_path)
        try:
            with lock.acquire(timeout=3):
                data = self.read()
                
                existing_ids = [str(item.get(identifier_key)) for item in data if item.get(identifier_key)]
                
                if str(new_item.get(identifier_key)) in existing_ids:
                    print(f"ID {new_item.get(identifier_key)} já existe")
                    return False
                    
                data.append(new_item)
                return self.write(data)
        except Timeout:
            print("Timeout ao acessar o arquivo bloqueado")
            return False
        except Exception as e:
            print(f"Erro inesperado: {str(e)}")
            return False

#Equipes Scrum
class Equipe:
    def __init__(self, nome_equipe, equipe_id, ra_scrum_master, ra_product_owner):
        self.equipe_id = equipe_id
        self.nome_equipe = nome_equipe
        self.ra_scrum_master = ra_scrum_master
        self.ra_product_owner = ra_product_owner
        self.devteam = []
        self.membros = []
    
    def add_membro(self, member_ra):
        if len(self.membros) < 9:
            self.membros.append(member_ra)
            return 'membros adicionados'
        else:
            return "Numero maximo de integrantes atingido"
        
    def add_to_team(self, member_ra):
        if self.devteam.append(member_ra):
            return 'membros adicionados'
        else:
            return 'não foi possivel adicionar o membro'

    def remove_membro(self, member_ra):
        if member_ra in self.membros:
            self.membros.remove(member_ra)
            return "Membro removido"
        else:
            return "Membro não encontrado"

    def has_member(self, member_ra):
        return member_ra in self.membros
    
    def to_dict(self):
        return{
            "equipe_id":self.equipe_id,
            "nome_equipe": self.nome_equipe,
            "membros": self.membros
        }
        
class AVALIACAO:
    def __init__(self, avaliacao_id, sprint, ra_aluno, avaliador_ra, produtividade, autonomia, 
                 colaboracao, entrega_resultados, feedback=None, data_avaliacao=None):
        self.avaliacao_id = avaliacao_id
        self.sprint = sprint
        self.ra_aluno = ra_aluno
        self.avaliador_ra = avaliador_ra
        self.produtividade = produtividade
        self.autonomia = autonomia
        self.colaboracao = colaboracao
        self.entrega_resultados = entrega_resultados
        self.feedback = feedback
        self.data_avaliacao = data_avaliacao or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def calcular_media(self):
        return (self.produtividade + self.autonomia + self.colaboracao + self.entrega_resultados) / 4
    
    def to_dict(self):
        return {
            "avaliacao_id": self.avaliacao_id,
            "sprint": self.sprint,
            "ra_aluno": self.ra_aluno,
            "avaliador_ra": self.avaliador_ra,
            "produtividade": self.produtividade,
            "autonomia": self.autonomia,
            "colaboracao": self.colaboracao,
            "entrega_resultados": self.entrega_resultados,
            "data_avaliacao": self.data_avaliacao,
            "media": self.calcular_media(),
            "feedback": self.feedback
        }