# Copilot Instructions for Secretaria Escolar (Django)

## Visão Geral
Este projeto é um sistema de Secretaria Escolar desenvolvido em Python com Django. Ele gerencia autenticação, cadastro de alunos, professores, contratos, notas, presenças e outros dados escolares. O código está organizado em apps Django, seguindo boas práticas de modularização e reutilização.

## Estrutura Principal
- `SecretariaEscolar/` — Projeto Django principal (settings, urls, wsgi, asgi)
- `projeto/` — App central com views, models, serializers, urls e templates
- `media/` — Armazena arquivos enviados (imagens, contratos PDF)
- `static/` — Arquivos estáticos do frontend
- `templates/` — HTMLs para as principais telas (login, cadastro, listagens)
- `migrations/` — Controle de versões do banco de dados

## Convenções e Padrões
- Use autenticação Django (`@login_required`, grupos de usuários) para proteger rotas sensíveis
- Models, serializers e views seguem o padrão Django REST e MVC
- Templates HTML usam herança (`base.html`) e feedbacks claros ao usuário
- Arquivos enviados são salvos em subpastas de `media/` conforme o tipo (ex: `agenda_files/`, `signed_contracts/`)
- Migrations devem ser criadas e aplicadas para toda alteração de model

## Fluxos de Desenvolvimento
- Para rodar localmente: `python manage.py runserver` na pasta `SecretariaEscolar/`
- Para aplicar migrations: `python manage.py makemigrations` e `python manage.py migrate`
- Para criar superusuário: `python manage.py createsuperuser`
- Testes manuais são descritos em `guia.txt` (ex: cadastro de aluno, login, etc.)

## Integrações e Segurança
- Banco de dados SQLite3 por padrão (`db.sqlite3`)
- Use CSRF token em todos os formulários
- Valide dados em formulários e serializers
- Mensagens de sucesso/erro devem ser exibidas ao usuário

## Exemplos de Padrões
- Views e URLs estão em `projeto/views.py` e `projeto/urls.py`
- Templates para cada entidade em `projeto/homeUp/<Entidade>/<entidade>.html`
- Contratos e arquivos são manipulados em `media/signed_contracts/`

## Dicas para Agentes
- Consulte `projeto/guia.txt` para critérios de avaliação e exemplos de fluxos
- Siga a estrutura de pastas e padrões Django já estabelecidos
- Prefira reutilizar componentes existentes (models, serializers, templates)
- Documente funções críticas e fluxos não triviais

Seções incompletas ou dúvidas sobre fluxos específicos devem ser revisadas com o usuário.
