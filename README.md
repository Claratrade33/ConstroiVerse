# 🏗️ ConstroiVerse — O Universo Real da Construção Inteligente

A maior plataforma conectada da construção civil: profissionais, clientes, lojas, representantes, engenheiros e IA trabalhando juntos em tempo real.

---

## 🚀 Tecnologias

- **Backend:** Flask + PyMongo (MongoDB)
- **Frontend:** HTML + JS (100% responsivo)
- **Autenticação:** JWT
- **IA:** OpenAI GPT (Clarice IA)
- **Banco:** MongoDB Atlas
- **Deploy:** Render.com ou Railway.app

---

## ⚙️ Instalação

```bash
git clone https://github.com/Claratrade33/ConstroiVerse.git
cd ConstroiVerse
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Execução

```bash
python main.py
```

## 🔐 Autenticação

Endpoints disponíveis:

- `POST /auth/register` — cria novo usuário com um dos perfis: engenheiro, representante, corretor ou usuario
- `POST /auth/login` — retorna um token JWT válido por 12h
- `GET /perfil/<email>` — informa a rota do painel conforme o perfil principal do usuário

Exemplo de registro:

```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "teste@example.com", "password": "123456", "main_profile": "engenheiro"}'
```

Exemplo de login:

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "teste@example.com", "password": "123456"}'
```

## 📚 Documentação

- [Arquitetura](docs/ARCHITECTURE.md)
- [Roadmap por etapas](docs/ROADMAP.md)
