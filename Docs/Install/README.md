# 📘 Guia de Instalação — Projeto Integrador 2025/1

Este documento descreve os passos necessários para instalar e executar o sistema desenvolvido com Flask para o Projeto Integrador 2025/1.

---

## ✅ Pré-requisitos

Antes de iniciar a instalação, certifique-se de que os seguintes requisitos estejam atendidos:

- **Python 3.8+** instalado no sistema.
- **Git** (opcional, apenas se for clonar o repositório via terminal).
- **Gerenciador de pacotes Pip** (já incluído por padrão nas instalações recentes do Python).

### 🔍 Verificando a instalação do Python

Abra o terminal e digite:

```sh
python --version
````

Se o comando não for reconhecido ou a versão estiver desatualizada, faça o download e instale o Python pelo site oficial:

🔗 [https://www.python.org/downloads/](https://www.python.org/downloads/)

---

## 📂 Download do projeto

Você pode obter o código-fonte do projeto de duas formas:

### 1. Clonando o repositório via Git:

```sh
git clone https://github.com/Y2K-Systems/Projeto-Integrador-2025-1.git
```

### 2. Baixando o arquivo ZIP:

* Acesse o repositório no GitHub.
* Clique no botão verde "Code" e depois em "Download ZIP".
* Extraia os arquivos em uma pasta de sua preferência.

---

## 📦 Instalando as dependências

Após extrair ou clonar o projeto, abra o terminal na raiz do repositório e execute:

```sh
pip install -r requirements.txt
```

Este comando instalará todas as bibliotecas necessárias para o funcionamento do sistema.

---

## ▶️ Executando a aplicação

Navegue até a pasta onde se encontra o arquivo principal da aplicação (geralmente chamado `App.py`) e utilize um dos seguintes comandos para iniciar o servidor Flask:

### Usando o Python diretamente:

```sh
python App.py
```

### Ou utilizando o comando Flask:

```sh
flask run
```

> **Nota:** Caso utilize `flask run`, você pode precisar configurar a variável de ambiente `FLASK_APP`. Exemplo no Windows (CMD):
>
> ```sh
> set FLASK_APP=App.py
> ```

---

## 🌐 Acessando a aplicação

Com o servidor em execução, abra o navegador e acesse:

```
http://127.0.0.1:5000/
```

Esse é o endereço local padrão onde a aplicação estará disponível.

---

## 🛠️ Ambiente Virtual (opcional, mas recomendado)

Para evitar conflitos com outras bibliotecas instaladas no seu sistema, recomenda-se o uso de um ambiente virtual:

```sh
python -m venv venv
```

Ative o ambiente virtual:

* **Windows:**

  ```sh
  venv\Scripts\activate
  ```

* **Linux/MacOS:**

  ```sh
  source venv/bin/activate
  ```

Depois, instale novamente os requisitos:

```sh
pip install -r requirements.txt
```

---

## 🧪 Testando a aplicação após a instalação

Depois que a aplicação estiver rodando no navegador, você pode testar os seguintes pontos:

* 🔐 Acesse a rota de login: [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)
* 📋 Verifique se os menus ou funcionalidades aparecem corretamente após o login.
* 📁 Tente subir um arquivo, adicionar um usuário ou realizar outras ações esperadas.
* 📦 Verifique o terminal para garantir que não há erros inesperados.

---

## 🔄 Atualizando as dependências

Se novas dependências forem adicionadas no futuro, você pode atualizá-las com:

```sh
pip install -r requirements.txt
```

Caso deseje recriar todo o ambiente do zero:

```sh
deactivate
rm -rf venv          # (ou 'rmdir /s venv' no Windows)
python -m venv venv
venv\Scripts\activate (ou source venv/bin/activate)
pip install -r requirements.txt
```

---

## 📁 Estrutura básica do projeto

```txt
Projeto-Integrador-2025-1/
│
├── app/
│   ├── data/                         # Armazenamento de Dados e arquivos
|   |   ├── atestados/                # Armazena pasta com ra de alunos
|   |   |   └── [RA ALUNO]/           # Armazena os atestados     
|   |   ├── db/
|   |   └── relatorios/               # Armazena o ultimo relatorio gerado  
|   |       ├── avaliacoes.csv
|   |       └── relatorio.pdf
│   ├── static/                       # Arquivos estáticos (CSS, JS, imagens)
│   ├── templates/                    # Templates HTML
│   └── App.py                        # Arquivo principal da aplicação
│
├── Docs/
└── README.md                         # Documentação (este arquivo)
```


---

## ♟️ Créditos

Projeto desenvolvido por alunos do curso Análise e Desenvolvimento de Sistemas, 1ºSemestre — **Projeto Integrador 2025/ 1**

| Professor M2 |
|:-------------:|
|   Prof. Jean Costa  |

| Professor P2 |
|:-------------:|
|   Prof. Antônio Egydio  |


| Desenvolvedores| GITHUB| LINKEDIN|
|:----:|:----:|:----:|
|Nicolas Anderson Ferreira Freitas|<a href="https://github.com/Slot148"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a>|<a href=""><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>|
|Heitor Guilherme Rezende Queiroz Silva|<a href="https://github.com/heitorsilva1337"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a>|<a href=""><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>|
|Davi Andrande Amancio dos Anjos|<a href="https://github.com/aandrade007"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a>|<a href=""><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>|
|Isabella Dombrowski Zanlorenzi|<a href="https://github.com/isadombrowski"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a>|<a href=""><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>|
|Igor Siqueira Prado|<a href="https://github.com/IgorSiqueira7"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a>|<a href=""><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>|
---



