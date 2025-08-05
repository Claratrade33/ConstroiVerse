# Esqueleto da Arquitetura do Projeto

## Backend (API Flask)
- `backend/app.py` – ponto de entrada da aplicação
- `backend/controllers/` – controladores agrupados por domínio (ex.: `auth_controller.py` para autenticação JWT)
- `backend/models/` – esquemas de dados e lógica de banco
- `backend/services/` – regras de negócio e integrações
- `backend/utils/` – utilitários compartilhados
- `backend/tests/` – testes unitários do backend

## Frontend (Cliente Web)
- `frontend/` – raiz dos ativos web
  - `frontend/src/` – módulos e componentes JavaScript
  - `frontend/public/` – arquivos estáticos
  - `frontend/tests/` – testes do frontend

## Compartilhado
- `docs/` – documentação e planejamento do projeto
- `requirements.txt` – dependências Python
- `package.json` – dependências do frontend
- `render.yaml` / `Procfile` – configuração de deploy

