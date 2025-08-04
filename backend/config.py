import os
from pymongo import MongoClient

# Pega a string de conexão do MongoDB das variáveis de ambiente (.env ou Render)
MONGO_URI = os.getenv("MONGO_URI")

# Cria o client do MongoDB
client = MongoClient(MONGO_URI)

# Seleciona o banco de dados 'constroiverse'
db = client['constroiverse']