import os, json
from werkzeug.security import generate_password_hash, check_password_hash

class USER:
    """Classe base que representa um usuário do sistema.
    
    Attributes:
        ra (str): Registro Acadêmico do usuário (identificador único)
        nome (str): Nome completo do usuário
        senha (str): Senha de acesso do usuário
    """
    def __init__(self, user_id, nome, senha):
        self.user_id = user_id
        self.nome = nome
        self.senha = generate_password_hash(senha)
    
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
    def __init__(self, user_id, nome, ra, senha, curso, turno, semestre, equipe="Sem Equipe"):
        super().__init__(user_id, nome, senha)
        self.ra = ra
        self.curso = curso
        self.turno = turno
        self.semestre = semestre
        self.equipe = equipe
    
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
            "equipe":  self.equipe
        })
        return data

class ADM(USER):
    def __init__(self, user_id, nome, senha, nivel_acesso):
        super().__init__(user_id, nome, senha)
        self.nivel_acesso = nivel_acesso

    def to_dict(self):
        data = super().to_dict()
        data["nivel_acesso"] = self.nivel_acesso
        return data

class JSON_MANAGER:
    """Classe para gerenciar operações de CRUD em arquivos JSON.
    
    Attributes:
        file_path (str): Caminho completo para o arquivo JSON
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.lock_path = file_path + ".lock"
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
        except (IOError, json.JSONEncodeError) as e:
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
        
    def add(self, new_item, identifier_key = "user_id"):
        """
        Adiciona um novo item ao JSON com lock, evitando duplicatas e concorrência.
        
        Args:
            new_item (dict): Dados do novo registro.
            identifier_key (str): Chave de identificação única (padrão: "user_id").
        
        Returns:
            bool: True se adicionado, False se falhou ou se é duplicado.
        """
        lock = FileLock(self.lock_path)
        try:
            with lock:
                data = self.read()

                if any(str(item.get(identifier_key)) == str(new_item.get(identifier_key)) for item in data):
                    print(f"Erro: Já existe um registro com {identifier_key} = {new_item.get(identifier_key)}")
                    return False
                data.append(new_item)
                return self.write(data)
        except Timeout:
            print("Erro: Timeout ao acessar o arquivo (outro processo em uso).")
            return False
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return False
