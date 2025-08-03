from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import jwt
import datetime

app = Flask(__name__)
CORS(app)

# 🔐 JWT config
SECRET_KEY = "constroiverse_super_secreta"

# 🌐 MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.constroiverse

# 🛠 Util
def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return None

# ✅ LOGIN SIMPLES
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    usuario = db.usuarios.find_one({"email": data["email"], "senha": data["senha"]})
    if usuario:
        payload = {
            "id": str(usuario["_id"]),
            "perfil": usuario["perfil"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})
    return jsonify({"erro": "Credenciais inválidas"}), 401

# 🚧 ROTAS DE OBRAS
@app.route("/api/obras", methods=["GET", "POST"])
def obras():
    token = decode_token(request.headers.get("Authorization"))
    if not token: return jsonify({"erro": "Não autorizado"}), 403

    if request.method == "GET":
        obras = list(db.obras.find({"dono_id": token["id"]}))
        for o in obras:
            o["_id"] = str(o["_id"])
        return jsonify(obras)

    if request.method == "POST":
        data = request.json
        data["dono_id"] = token["id"]
        db.obras.insert_one(data)
        return jsonify({"msg": "Obra cadastrada com sucesso"})

# ✅ TAREFAS POR OBRA
@app.route("/api/tarefas", methods=["POST"])
def criar_tarefa():
    token = decode_token(request.headers.get("Authorization"))
    if not token: return jsonify({"erro": "Não autorizado"}), 403
    data = request.json
    db.tarefas.insert_one({
        "obra_id": data["obra_id"],
        "profissional": data["profissional"],
        "descricao": data["descricao"],
        "status": "pendente"
    })
    return jsonify({"msg": "Tarefa atribuída"})

@app.route("/api/tarefas/<id>/status", methods=["PUT"])
def atualizar_tarefa(id):
    data = request.json
    db.tarefas.update_one({"_id": ObjectId(id)}, {"$set": {"status": data["status"]}})
    return jsonify({"msg": f"Tarefa marcada como {data['status']}"})

# ⭐️ AVALIAÇÕES
@app.route("/api/avaliacoes", methods=["POST"])
def avaliar():
    data = request.json
    db.avaliacoes.insert_one(data)
    return jsonify({"msg": "Avaliação registrada com sucesso"})

# 👥 VITRINE DE PROFISSIONAIS
@app.route("/api/vitrine", methods=["GET"])
def vitrine():
    categoria = request.args.get("categoria")
    regiao = request.args.get("regiao")
    query = {}
    if categoria: query["categoria"] = categoria
    if regiao: query["regiao"] = {"$regex": regiao, "$options": "i"}
    resultados = list(db.profissionais.find(query))
    for p in resultados:
        p["_id"] = str(p["_id"])
    return jsonify(resultados)

# 💼 OPORTUNIDADES PARA PROFISSIONAIS
@app.route("/api/oportunidades", methods=["GET"])
def oportunidades():
    categoria = request.args.get("categoria")
    cidade = request.args.get("cidade")
    query = {}
    if categoria: query["vaga"] = categoria
    if cidade: query["cidade"] = {"$regex": cidade, "$options": "i"}
    vagas = list(db.vagas.find(query))
    for v in vagas:
        v["_id"] = str(v["_id"])
    return jsonify(vagas)

# 📨 CORRETOR SOLICITA HABILITAÇÃO
@app.route("/api/solicitar-habilitacao", methods=["POST"])
def habilitar():
    data = request.json
    db.habilitacoes.insert_one(data)
    return jsonify({"msg": "Solicitação enviada para construtora"})

# 🔄 RESET INICIAL (opcional)
@app.route("/api/reset", methods=["POST"])
def reset():
    db.obras.delete_many({})
    db.tarefas.delete_many({})
    db.profissionais.delete_many({})
    db.vagas.delete_many({})
    db.habilitacoes.delete_many({})
    db.avaliacoes.delete_many({})
    return jsonify({"msg": "Sistema resetado!"})

if __name__ == "__main__":
    app.run(debug=True)