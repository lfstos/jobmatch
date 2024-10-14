# JobMatch

JobMatch é uma aplicação Django para empresas criarem vagas de emprego e candidatos se candidatarem a essas vagas.

## Funcionalidades

- **Criação de Vagas**: Empresas podem criar várias vagas.
- **Candidatura a Vagas**: Candidatos podem se candidatar a múltiplas vagas.
- **Pontuação de Candidatos**: Candidatos são pontuados com base na faixa salarial e escolaridade.
- **Relatórios**: Geração de relatórios de vagas e candidaturas por mês.

## Instalação

1. **Clone o repositório**:
    ```bash
    git clone https://github.com/seu-usuario/jobmatch.git
    cd jobmatch
    ```

2. **Instale o Poetry**:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3. **Configure o Poetry no shell** (Adicione ao seu shell configuration file, como `.bashrc`, `.zshrc`, etc.):
    ```bash
    export PATH="$HOME/.poetry/bin:$PATH"
    ```

4. **Instale as dependências**:
    ```bash
    poetry install
    ```

5. **Inicie o ambiente virtual do Poetry**:
    ```bash
    poetry shell
    ```

6. **Configure o banco de dados**:
    O Banco de dados utilizado nesse projeto foi o SQLite que vem junto com o Framework Django.

7. **Aplique as migrações**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

8. **Crie um superusuário**:
    ```bash
    python manage.py createsuperuser
    ```

9. **Execute o servidor de desenvolvimento**:
    ```bash
    python manage.py runserver
    ```

## Testes

Para rodar os testes, execute:

```bash
pytest
```
### Estrutura do Projeto:

O diretório do projeto é o core, onde também criei os apps dentro.

A documentação do Django criam os apps ao lado do projeto, quando é um projeto pequeno não tem nenhum problema, mas 
quando o projeto começa a ficar maior com vários 

## Funciomanto do sistema

Para executar o sistema digitamos na barra de endereço localhost:8000

Na hora que for cadastrar um usuário no sistema, observe que ao clicar em Registrar você será redirecionado para o 
formulário que cadastra um Candidato, e se quiser registrar uma Empresa, selecione no menu superior Registrar Empresa.

### Candidato

Ao logar no sistema como candidato, o usuário terá as opçoes:
- **Ver Detalhe da Vaga** 
- **Candidatar-se**

Ao acessar o sistema como candidato, você automaticamente será redirecionado para a página de Vagas onde é listada todas
as vagas no sistema.

No menu superior, temos um link de navegação onde conseguimos acessar o Relatório de Vagas Criadas por Mês e logo abaixo
temos Candidatos Recebidos por Mês

### Empresa

Ao logar no sistema como empresa, o usuário terá as opçoes:
- **Ver Detalhe da Vaga** 
- **Editar Vaga** 
- **Deletar Vaga**
- **Criar Vaga**
