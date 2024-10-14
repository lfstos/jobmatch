# jobmatch


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

2. **Crie um ambiente virtual**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure o banco de dados**:
    Crie um banco de dados PostgreSQL e atualize as configurações em `settings.py`.

5. **Aplique as migrações**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Crie um superusuário**:
    ```bash
    python manage.py createsuperuser
    ```

7. **Execute o servidor de desenvolvimento**:
    ```bash
    python manage.py runserver
    ```

## Testes

Para rodar os testes, execute:

```bash
pytest
