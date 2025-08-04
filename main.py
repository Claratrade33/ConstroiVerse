import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime

# Carregar variáveis de ambiente
load_dotenv()

# Diretórios para HTML/CSS/JS
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'frontend', 'painel')
STATIC_DIR = os.path.join(BASE_DIR, 'frontend', 'static')

# Inicializa o app Flask
app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)
CORS(app)

# Configurações
SECRET_KEY = os.getenv('SECRET_KEY', 'CHAVESECRETA')
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

# Conexão com MongoDB
client = MongoClient(MONGO_URI)
db = client['constroiverse']

# Coleções
usuarios_collection = db['usuarios']
obras_collection = db['obras']
profissionais_collection = db['profissionais']
documentos_collection = db['documentos']
licitacoes_collection = db['licitacoes']
materiais_collection = db['materiais']
fabricantes_collection = db['fabricantes']

### --- Dados de EXEMPLO (cadastra só se não existir nada) ---
def inserir_exemplos():
    if obras_collection.count_documents({}) == 0:
        obras_collection.insert_many([
            {
                "nome": "Edifício Jardim Europa",
                "status": "Em execução",
                "roi": "18%",
                "profissionais": ["Eng. Fulano de Tal", "Arq. Maria Silva"],
                "documentos": ["Planta Baixa.pdf", "ART.pdf"],
                "materiais": ["Concreto Usinado", "Tinta Suvinil Premium"],
                "licitacoes": ["Licitação 001"],
                "fabricantes": ["Suvinil", "Votorantim"]
            },
            {
                "nome": "Residencial Solar",
                "status": "Em licitação",
                "roi": "22%",
                "profissionais": ["Eng. Pedro Gomes"],
                "documentos": ["Memorial Descritivo.pdf"],
                "materiais": ["Bloco Estrutural", "Cimento Votoran"],
                "licitacoes": ["Licitação 002"],
                "fabricantes": ["Votorantim"]
            }
        ])
    if profissionais_collection.count_documents({}) == 0:
        profissionais_collection.insert_many([
            {"nome": "Eng. Fulano de Tal", "especialidade": "Engenheiro Civil"},
            {"nome": "Arq. Maria Silva", "especialidade": "Arquiteta"},
            {"nome": "Eng. Pedro Gomes", "especialidade": "Engenheiro de Obras"}
        ])
    if documentos_collection.count_documents({}) == 0:
        documentos_collection.insert_many([
            {"nome": "Planta Baixa.pdf", "obra": "Edifício Jardim Europa"},
            {"nome": "ART.pdf", "obra": "Edifício Jardim Europa"},
            {"nome": "Memorial Descritivo.pdf", "obra": "Residencial Solar"}
        ])
    if licitacoes_collection.count_documents({}) == 0:
        licitacoes_collection.insert_many([
            {"nome": "Licitação 001", "status": "Aberta", "obra": "Edifício Jardim Europa"},
            {"nome": "Licitação 002", "status": "Aberta", "obra": "Residencial Solar"}
        ])
    if materiais_collection.count_documents({}) == 0:
        materiais_collection.insert_many([
            {"nome": "Concreto Usinado", "quantidade": 120, "obra": "Edifício Jardim Europa", "fabricante": "Votorantim"},
            {"nome": "Tinta Suvinil Premium", "quantidade": 80, "obra": "Edifício Jardim Europa", "fabricante": "Suvinil"},
            {"nome": "Bloco Estrutural", "quantidade": 1000, "obra": "Residencial Solar", "fabricante": "Votorantim"},
            {"nome": "Cimento Votoran", "quantidade": 200, "obra": "Residencial Solar", "fabricante": "Votorantim"}
        ])
    if fabricantes_collection.count_documents({}) == 0:
        fabricantes_collection.insert_many([
            {"nome": "Votorantim", "produtos": ["Concreto Usinado", "Cimento Votoran"]},
            {"nome": "Suvinil", "produtos": ["Tinta Suvinil Premium"]}
        ])
inserir_exemplos()

# --- ROTAS DE PAINEL ---
@app.route('/')
def painel_construtora():
    return render_template('painel_construtora.html')

# --- API DE DADOS ---
@app.route('/api/obras')
def api_obras():
    obras = list(obras_collection.find({}, {'_id': 0}))
    return jsonify(obras)

@app.route('/api/profissionais')
def api_profissionais():
    profissionais = list(profissionais_collection.find({}, {'_id': 0}))
    return jsonify(profissionais)

@app.route('/api/documentos')
def api_documentos():
    documentos = list(documentos_collection.find({}, {'_id': 0}))
    return jsonify(documentos)

@app.route('/api/licitacoes')
def api_licitacoes():
    licitacoes = list(licitacoes_collection.find({}, {'_id': 0}))
    return jsonify(licitacoes)

@app.route('/api/materiais')
def api_materiais():
    materiais = list(materiais_collection.find({}, {'_id': 0}))
    return jsonify(materiais)

@app.route('/api/fabricantes')
def api_fabricantes():
    fabricantes = list(fabricantes_collection.find({}, {'_id': 0}))
    return jsonify(fabricantes)

# --- API STATUS ---
@app.route('/api')
def api_status():
    return jsonify({"status": "ConstroiVerse API ativa"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)