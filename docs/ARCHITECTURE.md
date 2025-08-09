# Esqueleto da Arquitetura do Projeto

## Backend (API Flask)
- `backend/app.py` – ponto de entrada da aplicação
- `backend/controllers/` – controladores agrupados por domínio
- `backend/models/` – esquemas de dados e lógica de banco
- `backend/services/` – regras de negócio e integrações
- `backend/utils/` – utilitários compartilhados
- `tests/` – testes unitários do backend

## Frontend (Cliente Web)
- `frontend/` – arquivos HTML e assets estáticos

## Compartilhado
- `docs/` – documentação e planejamento do projeto
- `requirements.txt` – dependências Python
- `render.yaml` / `Procfile` – configuração de deploy
