# Clone do Twitter - Django Monolítico

## Descrição
Projeto de rede social inspirado no Twitter, feito com Django (back-end e front-end monolítico). Usuários podem:
- Criar conta, fazer login/logout
- Alterar perfil (avatar, nome, senha)
- Seguir/desseguir outros usuários
- Curtir e comentar posts
- Ver feed com postagens de pessoas seguidas

## Tecnologias
- Python 3.13
- Django 5.2
- SQLite (pode trocar para PostgreSQL em produção)
- HTML, CSS

## Como rodar localmente
1. Criar virtualenv: `python -m venv venv`
2. Ativar virtualenv:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
3. Instalar dependências: `pip install -r requirements.txt`
4. Rodar migrações: `python manage.py migrate`
5. Criar superusuário: `python manage.py createsuperuser`
6. Rodar servidor: `python manage.py runserver`
7. Acessar: `http://127.0.0.1:8000/`

## Dependências principais
- Django
- django-extensions (opcional)

## Deploy
O projeto pode ser hospedado em PythonAnywhere ou Render.
