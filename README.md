<p align='center'>
  <img src='assets\banner2.jpg'>
<br>
<hr>
<br>
<h4 align="center">
  <a href="https://www.figma.com" target="_blank"><img src="https://img.shields.io/badge/-Figma-%23E4405F?style=for-the-badge&logo=Figma&logoColor=white" target="_blank"></a>  <a href="https://www.python.org/downloads/release/python-370/" target="_blank"><img src="https://img.shields.io/badge/-Python-%2388CE?style=for-the-badge&logo=Python&logoColor=white" target="_blank"></a> <a href="https://code.visualstudio.com" target="_blank"><img src="https://img.shields.io/badge/-Visual Studio Code-%2384CE?style=for-the-badge&logo=Visual Studio Code&logoColor=white" target="_blank"></a>
</h4>

<br>
<p align="center">
    |
  <a href ="#objetivo-do-projeto">  Objetivo do Projeto </a>  |     
  <a href ="#metodologia"> Metodologia </a>  |
  <a href ="#mvp"> MVP </a>  |
  <a href ="#sprints"> Sprints </a>  |
  <a href ="#backlog-do-produto"> Backlog do Produto </a>  | 
  <a href ="#autores"> Autores </a>  |
</p>
</br>

## 📌Objetivo do Projeto
> **O sistema web tem como objetivo:**
>- *Registrar e gerir* atestados médicos de alunos, facilitando a comunicação entre estudantes, professores e direção.
>- *Avaliação continua de equipes ágeis*, permitindo análise de desempenho em projetos de desenvolvimento de software
>
> **Status do Projeto:**<br>
>Em andamento🔄️
<br> 

## 💡Visão do Produto
Para alunos, professores e coordenadores da Fatec SJC que precisam gerenciar atestados médicos e avaliar equipes ágeis, o Gestor Ágil Acadêmico é um sistema web que simplifica o registro e a análise desses dados.<br>
Diferente de planilhas manuais e sistemas desconectados, nossa solução oferece:<br>
- Registro digital de atestados médicos (com upload de PDF e prazos automáticos)<br>
- Avaliação contínua de equipes ágeis (Scrum Master, PO, Devs) com métricas claras<br>
- Relatórios inteligentes para acompanhamento acadêmico e gerencial

Tudo em uma interface intuitiva, com dados seguros e acessíveis de qualquer dispositivo.
<br>

## 📚Metodologia

O produto adotou o **Scrum** como metodologia ágil, um framework flexível, iterativo e adaptativo, focado em eficiência e entrega contínua de valor. Como parte desse processo, o projeto foi organizado em **Sprints**, ciclos de trabalho curtos e bem definidos.

Para determinar o escopo de cada Sprint, primeiro estabelecemos o **MVP (Produto Mínimo Viável)**, priorizando funcionalidades que oferecessem o maior impacto ao cliente. Em seguida, as tarefas selecionadas foram consolidados no **Backlog do Produto**, que, após validação do cliente, foi segmentado em **3 Backlogs de Sprint**.

Com as atividades definidas, estimamos o tempo necessário para cada uma delas e distribuímos as demandas de forma otimizada entre os membros do time de desenvolvimento, garantindo eficiência e alinhamento com os prazos estabelecidos.

<br>

## 🏆**MVP**

1. Wireframe: [Protótipo navegável](https://www.figma.com/proto/Ox8KcNvkylAJDsWbpvBEIQ/COVID-longa?node-id=7-18&scaling=min-zoom&page-id=0%3A1&starting-point-node-id=7%3A18)
2. Web Site: [Versão atual](Docs/video)



<br>

## 📅Sprints 

### Sprint - 1️⃣ 🎯 ([Clique aqui](/Docs/Sprints/Sprint1)):  Concluído✅

### Sprint - 2️⃣ 🎯 ([Clique aqui](/Docs/Sprints/Sprint2)):  Pendente✅

### Sprint - 3️⃣ 🎯 ([Clique aqui](/Docs/Sprints/Sprint3)):  Pendente⭕
<br>

## 🌱Backlog do Produto

| ID  | ITEM                | FUNCIONALIDADE         | DESCRIÇÃO                                         | USER STORY DETALHADA                                                                 | PRIORIDADE | SPRINT |
|:---:|:-------------------:|:-----------------------:|:-------------------------------------------------:|:------------------------------------------------------------------------------------:|:----------:|:------:|
| #01 | *Estruturação*      | Design Preview          | WireFrames para planejamento da estrutura         | "Como gestor do projeto, quero visualizar os wireframes para validar a estrutura antes do desenvolvimento, garantindo que atenda aos requisitos." | Baixa      | 1      |
| #02 | *Estruturação*      | Estrutura do HTML       | Estrutura básica das páginas HTML usadas          | "Como desenvolvedor, preciso criar a estrutura HTML base do sistema para que possamos começar a implementar as funcionalidades." | Alta       | 1      |
| #03 | *Atestados Médicos* | Upload de documentos    | Função para envio de PDF's (Até 5MB)              | "Como aluno, desejo enviar atestados médicos em PDF para justificar faltas, com limite de 5MB por arquivo." | Alta       | 1      |
| #04 | *Gestão de Usuários*| Cadastro de alunos      | Registro de dados básicos dos alunos              | "Como administrador, preciso cadastrar alunos no sistema com informações básicas (nome, matrícula, curso) para gerenciar seus acessos." | Alta       | 2      |
| #05 | *Gestão de Usuários*| Perfis de acesso        | Definição de níveis (aluno, professor e admin)    | "Como sistema, devo restringir funcionalidades conforme o perfil (aluno: visualizar, professor: aprovar, admin: gerenciar) para segurança." | Alta       | 2      |
| #06 | *Atestados Médicos* | Armazenamento           | Organização por pastas (Identificador do aluno)   | "Como sistema, devo armazenar atestados em pastas únicas por aluno (ID) para facilitar a recuperação e auditoria." | Média      | 2      |
| #07 | *Equipes Ágeis*     | Cadastro de equipes     | Criação de equipes e atribuição de funções        | "Como professor, desejo criar equipes de alunos e definir seus papéis (scrum master, dev) para organizar projetos ágeis." | Alta       | 3      |
| #08 | *Equipes Ágeis*     | Avaliação de desempenho | Formulários com avaliação (método P.A.C.E.R)      | "Como professor, quero avaliar equipes com critérios P.A.C.E.R (Produtividade, Adaptabilidade, etc) para medir evolução." | Alta       | 3      |
| #09 | *Atestados Médicos* | Consulta                | Filtragem (Aluno, tipo, período)                  | "Como administrador, preciso filtrar atestados por aluno, tipo ou período para emitir relatórios mensais." | Média      | 3      |
| #10 | *Equipes Ágeis*     | Histórico               | Comparativo temporal de avaliações                | "Como aluno, desejo visualizar meu desempenho em avaliações anteriores para identificar pontos de melhoria." | Baixa      | 3      |
| #11 | *Análise de Dados*  | Geração de relatórios   | Exportação em PDF/EXCEL/CSV                       | "Como gestor, quero exportar relatórios de avaliações em múltiplos formatos para análise externa." | Média      | 3      |
| #12 | *Interface*         | Design Responsivo       | Adaptação para Mobile e Desktop                   | "Como usuário, desejo acessar o sistema tanto no celular quanto no desktop com experiência adaptada a cada dispositivo." | Baixa      | 3      |
| #13 | *Interface*         | MicroInterações         | Animações para feedback (loading, success, etc)   | "Como usuário, quero receber feedback visual (ex: animação de sucesso) ao realizar ações para confirmar que foram processadas." | Baixa      | 3      |
| #14 | *Interface*         | Ícones Customizados     | Ícones temáticos para ações específicas           | "Como usuário, desejo identificar rapidamente funções (ex: ícone de upload) para melhor usabilidade." | Baixa      | 3      |

## 👨‍💻**Autores** 

| NOME| FUNÇÃO| GITHUB| LINKEDIN|
|:----:|:----:|:----:|:----:|
|Nicolas Anderson Ferreira Freitas|Scrum Master|<a href="https://github.com/Slot148"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a>|<a href=""><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>|
|Heitor Guilherme Rezende Queiroz Silva|Developer Team|<a href="https://github.com/heitorsilva1337"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a>|<a href=""><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>|
|Davi Andrande Amancio dos Anjos|Developer Team|<a href="https://github.com/aandrade007"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a>|<a href=""><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>|
|Isabella Dombrowski Zanlorenzi|Developer Team|<a href="https://github.com/isadombrowski"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a>|<a href=""><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>|
|Igor Siqueira Prado|Developer Team|<a href="https://github.com/IgorSiqueira7"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a>|<a href=""><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a>|
