from flask import Blueprint, request, jsonify
from src.database import get_collection
from models.mongodb_models import Projeto, PerfilProfissional, Usuario, Material
from bson import ObjectId
from datetime import datetime

projetos_bp = Blueprint('projetos', __name__)

@projetos_bp.route('/projetos', methods=['GET'])
def listar_projetos():
    """Lista todos os projetos"""
    try:
        # projetos_collection = get_collection("projetos")
        # usuarios_collection = get_collection("usuarios")
        # perfis_profissionais_collection = get_collection("perfis_profissionais")
        
        # projetos = list(projetos_collection.find({}))
        # resultado = []
        
        # for projeto in projetos:
        #     profissional_id = projeto.get("profissional_id")
        #     cliente_id = projeto.get("cliente_id")
            
        #     profissional_perfil = perfis_profissionais_collection.find_one({"id": profissional_id})
        #     profissional_usuario = usuarios_collection.find_one({"id": profissional_perfil["usuario_id"]}) if profissional_perfil else None
        #     cliente_usuario = usuarios_collection.find_one({"id": cliente_id})
            
        #     projeto["_id"] = str(projeto["_id"])
        #     if "created_at" in projeto and isinstance(projeto["created_at"], datetime):
        #         projeto["created_at"] = projeto["created_at"].isoformat()
        #     if "updated_at" in projeto and isinstance(projeto["updated_at"], datetime):
        #         projeto["updated_at"] = projeto["updated_at"].isoformat()
            
        #     proj_info = {
        #         'id': projeto["id"],
        #         'nome_projeto': projeto["nome_projeto"],
        #         'descricao': projeto.get("descricao", ""),
        #         'status': projeto.get("status", ""),
        #         'data_criacao': projeto.get("created_at", ""),
        #         'profissional': {
        #             'id': profissional_id,
        #             'nome': profissional_usuario["nome"] if profissional_usuario else "Desconhecido",
        #             'profissao': profissional_perfil["profissao"] if profissional_perfil else "Desconhecida"
        #         } if profissional_id else None,
        #         'cliente': {
        #             'id': cliente_id,
        #             'nome': cliente_usuario["nome"] if cliente_usuario else "Desconhecido"
        #         } if cliente_id else None
        #     }
        #     resultado.append(proj_info)
        
        return jsonify([
            {
                "id": "simulated_proj_1",
                "nome_projeto": "Reforma da Cozinha",
                "descricao": "Projeto de reforma completa da cozinha.",
                "status": "em andamento",
                "data_criacao": "2025-11-11T10:00:00",
                "profissional": {"id": "prof_1", "nome": "João Pedreiro", "profissao": "Pedreiro"},
                "cliente": {"id": "cli_1", "nome": "Maria Cliente"}
            },
            {
                "id": "simulated_proj_2",
                "nome_projeto": "Construção de Casa",
                "descricao": "Construção de casa de 2 andares.",
                "status": "planejamento",
                "data_criacao": "2025-11-01T15:30:00",
                "profissional": {"id": "prof_2", "nome": "Ana Arquiteta", "profissao": "Arquiteto"},
                "cliente": {"id": "cli_2", "nome": "Pedro Cliente"}
            }
        ]), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@projetos_bp.route('/projetos', methods=['POST'])
def criar_projeto():
    """Cria um novo projeto"""
    try:
        dados = request.get_json()
        
        # Validação básica
        if not dados.get("nome_projeto") or not dados.get("profissional_id") or not dados.get("cliente_id"):
            return jsonify({"erro": "Campos obrigatórios: nome_projeto, profissional_id, cliente_id"}), 400
        
        # projetos_collection = get_collection("projetos")
        
        # novo_projeto = Projeto(
        #     nome_projeto=dados["nome_projeto"],
        #     descricao=dados.get("descricao", ""),
        #     profissional_id=dados["profissional_id"],
        #     cliente_id=dados["cliente_id"],
        #     tipo_projeto=dados.get("tipo_projeto", "residencial"),
        #     area_construida=dados.get("area_construida", 0.0),
        #     orcamento_estimado=dados.get("orcamento_estimado", 0.0),
        #     status=dados.get("status", "planejamento"),
        #     data_inicio=datetime.fromisoformat(dados["data_inicio"]) if "data_inicio" in dados else None,
        #     data_fim_prevista=datetime.fromisoformat(dados["data_fim_prevista"]) if "data_fim_prevista" in dados else None
        # )
        
        # result = projetos_collection.insert_one(novo_projeto.to_dict())
        # novo_projeto_dict = novo_projeto.to_dict()
        # novo_projeto_dict["_id"] = str(result.inserted_id)
        
        return jsonify({
            "id": "simulated_new_proj_id",
            "nome_projeto": dados["nome_projeto"],
            "status": dados.get("status", "planejamento"),
            "data_criacao": datetime.utcnow().isoformat()
        }), 201
        
    except Exception as e:

        return jsonify({"erro": str(e)}), 500

@projetos_bp.route('/projetos/<projeto_id>', methods=['GET'])
def obter_projeto(projeto_id):
    """Obtém detalhes de um projeto específico"""
    try:
        # projetos_collection = get_collection("projetos")
        # # usuarios_collection = get_collection("usuarios")
        # # perfis_profissionais_collection = get_collection("perfis_profissionais")
        # # materiais_collection = get_collection("materiais")
        
        # projeto = projetos_collection.find_one({"id": projeto_id})
        # if not projeto:
        #     return jsonify({"erro": "Projeto não encontrado"}), 404
        
        # # Lógica de obtenção de detalhes (simulada)
        
        # projeto["_id"] = str(projeto["_id"])
        # if "created_at" in projeto and isinstance(projeto["created_at"], datetime):
        #     projeto["created_at"] = projeto["created_at"].isoformat()
        # if "updated_at" in projeto and isinstance(projeto["updated_at"], datetime):
        #     projeto["updated_at"] = projeto["updated_at"].isoformat()
        
        resultado = {
            "id": projeto_id,
            "nome_projeto": f"Projeto {projeto_id} (Simulado)",
            "descricao": "Detalhes do projeto simulado.",
            "status": "concluído",
            "data_criacao": "2025-11-01T15:30:00",
            "data_atualizacao": datetime.utcnow().isoformat(),
            "profissional": {"id": "prof_1"},
            "cliente": {"id": "cli_1"},
            "materiais": []
        }
        
        return jsonify(resultado), 200
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@projetos_bp.route('/projetos/<projeto_id>/materiais', methods=['POST'])
def adicionar_material_projeto(projeto_id):
    """Adiciona um material à lista do projeto (simulando análise da IA)"""
    try:
        # Lógica de adição de material (simulada)
        return jsonify({'mensagem': 'Material adicionado com sucesso'}), 201
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@projetos_bp.route('/projetos/<projeto_id>/analisar-ia', methods=['POST'])
def analisar_projeto_ia(projeto_id):
    """Simula análise de projeto pela IA para extrair lista de materiais"""
    try:
        # Lógica de análise da IA (simulada)
        return jsonify({
            'mensagem': 'Análise da IA concluída com sucesso',
            'materiais_identificados': 5,
            'materiais': []
        }), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@projetos_bp.route('/projetos/<projeto_id>', methods=['PUT'])
def atualizar_projeto(projeto_id):
    """Atualiza um projeto existente"""
    try:
        # Lógica de atualização de projeto (simulada)
        return jsonify({'mensagem': 'Projeto atualizado com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
