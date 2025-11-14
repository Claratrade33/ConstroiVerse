from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os


# Carrega as variáveis de ambiente do arquivo .env
# from dotenv import load_dotenv
# load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "construiverse_db")

client = None
db = None

def connect_to_mongodb():
    global client, db
    if client is None or not client.admin.command("ping"):
        try:
            client = MongoClient(MONGO_URI)
            db = client[DB_NAME]
            # O comando ping é enviado para confirmar uma conexão bem-sucedida
            client.admin.command("ping")
            print("Conectado ao MongoDB Atlas!")
        except ConnectionFailure as e:
            print(f"Erro de conexão ao MongoDB Atlas: {e}")
            client = None
            db = None
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao conectar ao MongoDB: {e}")
            client = None
            db = None
    return db

def get_db():
    if db is None:
        connect_to_mongodb()
    return db

def get_collection(collection_name):
    _db = get_db()
    if _db:
        return _db[collection_name]
    return None

def close_mongodb_connection():
    global client, db
    if client:
        client.close()
        client = None
        db = None
        print("Conexão com MongoDB fechada.")



