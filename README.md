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

### Backend Flask

```bash
python main.py
```

### Servidor Node (opcional)

```bash
node backend/server.js
```

## 🔐 Variáveis de ambiente

Antes de executar a aplicação, defina as seguintes variáveis de ambiente:

- `SECRET_KEY`: chave secreta usada pelo Flask para assinar tokens.
- `MONGO_URI`: string de conexão com o MongoDB.
- `OPENAI_API_KEY`: chave de acesso à API da OpenAI.
- `JWT_SECRET`: (se usar o servidor Node) segredo para assinar tokens JWT.
- `PORT`: porta utilizada pelo servidor Node.
